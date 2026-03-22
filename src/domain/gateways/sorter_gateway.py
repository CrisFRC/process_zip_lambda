from abc import ABC, abstractmethod
from typing import List
from src.domain.models.file_metadata import FileMetadata

class SorterGateway(ABC):
    """
    interfaz para el servicio de ordenamiento.
    """
    
    @abstractmethod
    def sort(self, files: List[FileMetadata]) -> List[FileMetadata]:
        """
        Toma una lista de metadatos de archivos y retorna una nueva lista ordenada 
        según el criterio de la estrategia implementada.
        """
        pass
