import os
import shutil
import zipfile
from datetime import datetime
from typing import List
from src.domain.gateways.storage_repository import StorageRepository
from src.domain.models.file_metadata import FileMetadata

class ZipExtractor(StorageRepository):
    def extract_zip(self, zip_local_path: str, extract_dir: str) -> List[FileMetadata]:
        files_metadata = []
        os.makedirs(extract_dir, exist_ok=True)
        
        with zipfile.ZipFile(zip_local_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
            
            for zip_info in zip_ref.infolist():
                if zip_info.is_dir():
                    continue
                    
                try:
                    # zip_info.date_time es una tupla: (year, month, day, hour, minute, second)
                    dt = datetime(*zip_info.date_time)
                except ValueError:
                    dt = datetime.now()
                    
                meta = FileMetadata(
                    filename=os.path.basename(zip_info.filename),
                    relative_path=zip_info.filename,
                    extension=os.path.splitext(zip_info.filename)[1],
                    size_bytes=zip_info.file_size,
                    last_modified_date=dt
                )
                files_metadata.append(meta)
                
        return files_metadata
        
    def clean_up(self, file_or_directory: str) -> None:
        if os.path.isfile(file_or_directory):
            try:
                os.remove(file_or_directory)
            except OSError:
                pass
        elif os.path.isdir(file_or_directory):
            try:
                shutil.rmtree(file_or_directory)
            except OSError:
                pass
