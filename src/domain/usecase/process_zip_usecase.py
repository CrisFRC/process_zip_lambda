import uuid
from typing import Dict, Any
from src.domain.gateways.drive_repository import DriveRepository
from src.domain.gateways.storage_repository import StorageRepository
from src.domain.gateways.sorter_gateway import SorterGateway

class ProcessZipUseCase:
    
    def __init__(self, drive_repo: DriveRepository, storage_repo: StorageRepository, sorter: SorterGateway):
        self.drive_repo = drive_repo
        self.storage_repo = storage_repo
        self.sorter = sorter
        
    def execute(self, source_drive_path: str, dest_drive_folder: str) -> Dict[str, Any]:
        """
        Orquesta la descarga, extracción, ordenamiento y subida.
        """
        exec_id = str(uuid.uuid4())
        local_zip_path = f"/tmp/{exec_id}_source.zip"
        extract_dir = f"/tmp/{exec_id}_extracted"
        
        try:
            # 1. Bajar el archivo zip
            self.drive_repo.download_file(source_drive_path, local_zip_path)
            
            # 2. Extraer el zip
            files_metadata = self.storage_repo.extract_zip(local_zip_path, extract_dir)
            if not files_metadata:
                return {"status": "success", "message": "El archivo zip estaba vacío."}
            
            # 3. Ordenar (Patrón Estrategia usando el puerto inyectado)
            sorted_files = self.sorter.sort(files_metadata)
            
            # 4. Subir archivos
            # Usamos un prefijo numérico para garantizar el orden visual en Drive
            total_files = len(sorted_files)
            padding = len(str(total_files))
            
            uploaded_count = 0
            for idx, file_meta in enumerate(sorted_files, start=1):
                prefix = str(idx).zfill(padding) + "_"
                new_filename = f"{prefix}{file_meta.filename}"
                self.drive_repo.upload_file(file_meta.relative_path if hasattr(file_meta, 'relative_path') else file_meta.local_path, dest_drive_folder, new_filename)
                uploaded_count += 1
                
            return {
                "status": "success", 
                "message": f"Se procesaron y subieron {uploaded_count} archivos correctamente."
            }
            
        finally:
            # 5. Limpiar temporales
            self.storage_repo.clean_up(local_zip_path)
            self.storage_repo.clean_up(extract_dir)
