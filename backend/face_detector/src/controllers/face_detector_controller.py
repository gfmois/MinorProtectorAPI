from io import BytesIO
from typing import Tuple

import cv2
from flask import jsonify
from werkzeug.datastructures import ImmutableMultiDict, FileStorage
from PIL import Image
import numpy as np

from src.models.FaceDetector import FaceDetector

class InvalidImageError(Exception):
    """Custom exception for invalid image errors."""
    def __init__(self, message: str, status_code: int):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class FaceDetectorController():
    def __init__(self) -> None:
        self.VALID_EXTENSIONS = (".jpg", ".jpeg", ".png")
        self.face_detector_model = FaceDetector()
        
    def __is_valid_image(self, files: ImmutableMultiDict[str, FileStorage]) -> Tuple[any, int]:
        """
        Private method that checks if the file exists and is valid.
        
        Args:
            files (ImmutableMultiDict[str, FileStorage]): Files from the request form-data

        Returns:
            Tuple[Any, int]: First value is the result of the image identification, 
                             second value is the status code.
        """
        
        try:
            if "image" not in files:
                raise InvalidImageError("No file found in request", 400)
            
            image = files["image"]
            
            if image.filename == "":
                raise InvalidImageError("No selected file", 400)
            
            if not image.filename.lower().endswith(self.VALID_EXTENSIONS):
                raise InvalidImageError("Not a valid image file", 400)
            
            return jsonify(msg="File is valid", status=200), 200
        except InvalidImageError as e:
            return jsonify(msg=e.message, status=e.status_code), e.status_code
        
    def detect_face(self, files: ImmutableMultiDict[str, FileStorage]):
        try:
            # Validate image 
            json_msg, status = self.__is_valid_image(files=files)
            if status != 200:
                return json_msg, status
            
            image = files["image"]
            image_bytes = BytesIO(image.stream.read())
            image_bytes.seek(0)
            
            img = Image.open(image_bytes)
            img_arr = np.array(img)
            
            image_bytes.seek(0)
            identified_faces = self.face_detector_model.identify_faces(image_bytes)
            face_boxes = identified_faces.boxes
            faces = []
            boxes = []
            
            for box in face_boxes:
                x_min, y_min, x_max, y_max = map(int, box.xyxy.tolist()[0])
                face: np.ndarray = img_arr[y_min:y_max, x_min:x_max]
                faces.append(face.tolist())
                boxes.append(list(map(int, box.xyxy.tolist()[0])))
                
            return jsonify(faces=faces, boxes=boxes)
        except InvalidImageError as e:
            print("Image error")
            return jsonify(
                msg=e.message,
                status=e.status_code
            ), e.status_code
        except Exception as e:
            print("Exception Error")
            print(e)
            return jsonify(
                msg=str(e),
                status=500
            ), 500