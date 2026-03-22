from abc import ABC, abstractmethod
from typing import Optional

class DriveRepository(ABC):
    """
    interfaz para la interaccion con el almacenamiento externo
    """
    
    @abstractmethod
    def download_file(self, source_drive_path: str, local_dest_path: str) -> None:
        """
        Descarga un archivo desde la ruta de origen y lo guarda en una ruta temporal local.
        """
        pass
    
    @abstractmethod
    def upload_file(self, local_source_path: str, dest_drive_folder: str, new_filename: Optional[str] = None) -> None:
        """
        Sube un archivo local a una carpeta de destino. 
        """
        pass
