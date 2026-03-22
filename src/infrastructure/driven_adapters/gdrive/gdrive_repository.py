import os
from typing import Optional
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from src.domain.gateways.drive_repository import DriveRepository
from src.infrastructure.driven_adapters.gdrive.gdrive_connection import DriveConnection

class GDriveRepository(DriveRepository):
    def __init__(self):
        self.service = DriveConnection.get_service()
        
    def download_file(self, source_drive_path: str, local_dest_path: str) -> None:
        """
        Descarga un archivo desde Drive.
        En este contexto MVP, asumimos que source_drive_path es el file_id directo en Google Drive.
        """
        file_id = source_drive_path
        request = self.service.files().get_media(fileId=file_id)
        
        with open(local_dest_path, "wb") as f:
            downloader = MediaIoBaseDownload(f, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
                
    def upload_file(self, local_source_path: str, dest_drive_folder: str, new_filename: Optional[str] = None) -> None:
        """
        Sube un archivo a Google Drive en el folder destino.
        """
        filename = new_filename if new_filename else os.path.basename(local_source_path)
        
        file_metadata = {
            'name': filename,
            'parents': [dest_drive_folder]
        }
        
        media = MediaFileUpload(local_source_path, resumable=True)
        self.service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
