from src.domain.usecase.process_zip_usecase import ProcessZipUseCase
from src.infrastructure.driven_adapters.gdrive.gdrive_repository import GDriveRepository
from src.infrastructure.storage.zip_extractor import ZipExtractor
from src.infrastructure.driven_adapters.sorters.basic_sorters import SizeSorter, AlphabeticalSorter, DateSorter

class DependencyContainer:
    
    @staticmethod
    def get_process_zip_usecase(sort_type: str) -> ProcessZipUseCase:
        drive_repo = GDriveRepository()
        storage_repo = ZipExtractor()
        
        if sort_type == "size":
            sorter = SizeSorter()
        elif sort_type == "alphabetical":
            sorter = AlphabeticalSorter()
        elif sort_type in ("date", "creation_date"):
            sorter = DateSorter()
        else:
            raise ValueError(f"Criterio de ordenamiento no soportado: '{sort_type}'")
            
        usecase = ProcessZipUseCase(
            drive_repo=drive_repo,
            storage_repo=storage_repo,
            sorter=sorter
        )
        
        return usecase
