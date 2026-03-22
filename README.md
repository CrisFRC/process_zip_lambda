# Autor
- [Cristian Roa](https://github.com/CrisFRC)`
version 1.0.0

# Process Zip Lambda

Proyecto para proceso asíncrono que extrae y organiza el contenido de un `.zip` desde una carpeta de origen en Google Drive hacia otra de destino, parametrizable.

## Estructura del proyecto

```
process_zip_lambda/
├── src/
│   ├── domain/
│   │   ├── models/
│   │   │   └── file_metadata.py
│   │   ├── gateways/
│   │   │   ├── drive_repository.py
│   │   │   ├── storage_repository.py
│   │   │   └── sorter_gateway.py
│   │   └── usecase/
│   │       └── process_zip_usecase.py
│   ├── infrastructure/
│   │   ├── driven-adapters/
│   │   │   ├── drive/
│   │   │   │   └── google_drive_adapter.py
│   │   │   ├── storage/
│   │   │   │   └── local_storage_adapter.py
│   │   │   └── sorters/
│   │   │       └── basic_sorters.py
│   │   └── lambda_handler.py
│   └── utils/
│       └── logger.py
├── tests/
│   ├── unit/
│   │   ├── test_process_zip_usecase.py
│   │   ├── test_google_drive_adapter.py
│   │   ├── test_local_storage_adapter.py
│   │   └── test_basic_sorters.py
│   └── integration/
│       └── test_end_to_end.py
├── .gitignore
├── README.md
├── requirements.txt
└── template.yaml
```

## Tecnologias

- Python 3.12
- AWS Lambda
- Google Drive API
- Local Storage
