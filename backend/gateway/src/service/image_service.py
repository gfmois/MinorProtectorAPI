import os
import requests
from io import BytesIO

from PIL.Image import Image
from dotenv import load_dotenv

class ImageService():
    def __init__(self) -> None:
        load_dotenv()
        pass
        
    def detect_face(self, image: Image):
        buffer = BytesIO()
        image.save(buffer, format="JPEG")
        buffer.seek(0)
        
        files = {'image': ('image.jpg', buffer, 'image/jpeg')}
        
        response = requests.post(os.environ["FACE_DETECTOR_HOST"], files=files)
        
        # FIXME: Tratar mejor los errores, etc.. meter en try catch
        if response.status_code == 200:
            return response.json()
        else:
            return 0