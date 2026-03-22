import os

class Settings:
    # Configuración de Directorios
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    TEMP_DIR = os.path.join(BASE_DIR, "temp")
    
    # Configuración de Google Drive (Hardcodeado para MVP, idealmente vendría de Secrets Manager)
    DRIVE_SERVICE_ACCOUNT_JSON = os.environ.get("DRIVE_SERVICE_ACCOUNT_JSON", "service_account.json")
    
    # Configuración de Idempotencia (Memoria Volátil)
    MAX_PROCESSED_EVENTS = 1000
    