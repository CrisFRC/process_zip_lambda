from typing import List
from src.domain.gateways.sorter_gateway import SorterGateway
from src.domain.models.file_metadata import FileMetadata

class SizeSorter(SorterGateway):
    """Estrategia pura en memoria para ordenar por tamaño de archivo (menor a mayor)"""
    def sort(self, files: List[FileMetadata]) -> List[FileMetadata]:
        return sorted(files, key=lambda f: f.size_bytes)


class AlphabeticalSorter(SorterGateway):
    """Estrategia pura en memoria para ordenar por nombre de archivo alfabéticamente"""
    def sort(self, files: List[FileMetadata]) -> List[FileMetadata]:
        return sorted(files, key=lambda f: f.filename.lower())


class DateSorter(SorterGateway):
    """Estrategia pura en memoria para ordenar por fecha de modificación (más antiguos primero)"""
    def sort(self, files: List[FileMetadata]) -> List[FileMetadata]:
        return sorted(files, key=lambda f: f.last_modified_date)
