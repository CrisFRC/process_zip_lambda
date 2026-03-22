import google.auth
from googleapiclient.discovery import build

class DriveConnection:
    @staticmethod
    def get_service():
        """
        Inicializa y retorna la conexión (Resource) de la API de Google Drive.
        Asume que las credenciales están configuradas en el entorno (ej. IAM Role de AWS Lambda).
        """
        credentials, project = google.auth.default(
            scopes=['https://www.googleapis.com/auth/drive']
        )
        service = build('drive', 'v3', credentials=credentials)
        return service
