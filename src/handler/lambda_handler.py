import json
import logging
from src.application.container.dependency_container import DependencyContainer

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Caché en memoria global (Fuera del handler) para retener IDs procesados
# entre ejecuciones consecutivas si el contenedor de AWS Lambda se mantiene "caliente" (Warm).
processed_events = set()

def lambda_handler(event, context):
    """
    Punto de entrada de la Lambda.
    Recibe el evento de invocación (ej. desde n8n directo, o SQS).
    """
    # 1. Intentar obtener un ID único del evento para la idempotencia.
    # Si viene de SQS, usaríamos el messageId. Aquí usamos un fallback genérico.
    event_id = event.get('request_id', getattr(context, 'aws_request_id', 'unknown_id'))
    
    # === MITIGACIÓN DE DUPLICADOS SIN BASE DE DATOS ===
    # Solo funciona para concurrencia en el *mismo* entorno de ejecución (Warm Start).
    if event_id in processed_events and event_id != 'unknown_id':
        logger.info(f"Evento {event_id} ya procesado en este contenedor. Evitando ejecución duplicada.")
        return {
            "statusCode": 200, 
            "body": json.dumps({"message": "Se esta procesando el evento, por favor espere"})
        }
        
    try:
        # 2. Parseo del payload (Asumiendo invocación HTTP plana desde n8n)
        source_drive_path = event.get("source_drive_path")
        dest_drive_folder = event.get("dest_drive_folder")
        sort_criteria = event.get("sort_criteria", "alphabetical")
        
        if not source_drive_path or not dest_drive_folder:
            return {"statusCode": 400, "body": json.dumps({"error": "Parámetros 'source_drive_path' y 'dest_drive_folder' son obligatorios"})}
            
        logger.info(f"Iniciando procesamiento: Origen={source_drive_path}, Destino={dest_drive_folder}, Orden={sort_criteria}")
        
        # 3. Solicitamos el Caso de Uso a nuestro Application Context / Container
        usecase = DependencyContainer.get_process_zip_usecase(sort_type=sort_criteria)
        
        # 4. Ejecutamos nuestra Lógica de Negocio Pura
        result = usecase.execute(source_drive_path, dest_drive_folder)
        
        # 5. Registrar el ID como procesado exitosamente en este contenedor
        if event_id != 'unknown_id':
            # Mantenemos el set limpio limitando su tamaño a 1000 para no agotar la memoria de Lambda
            if len(processed_events) > 1000:
                processed_events.clear()
            processed_events.add(event_id)
            
        return {
            "statusCode": 200,
            "body": json.dumps(result)
        }
        
    except ValueError as ve:
        logger.error(f"Error de validación: {str(ve)}")
        return {"statusCode": 400, "body": json.dumps({"error": str(ve)})}
    except Exception as e:
        logger.exception("Error interno procesando el archivo ZIP")
        return {"statusCode": 500, "body": json.dumps({"error": "Error interno del servidor", "details": str(e)})}
