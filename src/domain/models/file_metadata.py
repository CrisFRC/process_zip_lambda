from dataclasses import dataclass
from datetime import datetime

@dataclass
class FileMetadata:
    filename: str
    relative_path: str
    extension: str
    size_bytes: int
    last_modified_date: datetime
