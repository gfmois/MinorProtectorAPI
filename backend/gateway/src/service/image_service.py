import os
import requests
from typing import List
from numpy import ndarray
from io import BytesIO

from PIL.Image import Image
from dotenv import load_dotenv

from requests import Response

class ImageService():
    def __init__(self) -> None:
        load_dotenv()
        pass
        
    def detect_face(self, image: Image):
        buffer = BytesIO()
        image.save(buffer, format="JPEG")
        buffer.seek(0)
        
        files = {'image': ('image.jpg', buffer, 'image/jpeg')}
        
        response: Response = requests.post(os.environ["FACE_DETECTOR_HOST"], files=files)
        
        # FIXME: Tratar mejor los errores, etc.. meter en try catch
        if response.status_code == 200:
            return response.json()
        else:
            return 0
        
    def identify_age(self, faces: List[ndarray]):
        response: Response = requests.post(os.environ["AGE_CLASSIFICATOR_HOST"], json={"faces": faces})
        classifications: List[bool] = response.json()["classifications"]
        
        # FIXME: Classifications items are string not bool, parse it
        if response.status_code == 200:
            return {
                "n_minors": classifications.count(True),
                "n_adults": classifications.count(False)
            }
        else:
            print("Not Working")
            return 0