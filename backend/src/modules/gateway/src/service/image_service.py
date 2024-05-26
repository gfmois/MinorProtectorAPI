from src.utils.http import HttpClient

class ImageService():
    def __init__(self) -> None:
        self.http_client = HttpClient()
        
    def detect_face(self):
        return 0