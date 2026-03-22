from abc import ABC, abstractmethod
from typing import List
from src.domain.models.file_metadata import FileMetadata

class StorageRepository(ABC):
    """
    interfaz para la manipulacion de archivos en el entorno de ejecucion
    """
    
    @abstractmethod
    def extract_zip(self, zip_local_path: str, extract_dir: str) -> List[FileMetadata]:
        """
        Descomprime un archivo ZIP alojado localmente y retorna una lista de objetos FileMetadata
        que representan exclusivamente el contenido a procesar.
        """
        pass
    
    @abstractmethod
    def clean_up(self, file_or_directory: str) -> None:
        """
        Limpia y elimina directorios o archivos residuales después del procesamiento
        """
        pass
