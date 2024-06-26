from io import BytesIO
from string import punctuation
from typing import Tuple, Any
from scipy.datasets import face
from sympy import true

from werkzeug.datastructures import ImmutableMultiDict, FileStorage
from flask import jsonify, Response
from PIL import Image, ImageDraw
from PIL.Image import Image as ImageType
import numpy as np
import cv2

from ..service.image_service import ImageService

class InvalidImageError(Exception):
    """Custom exception for invalid image errors."""
    def __init__(self, message: str, status_code: int):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class ImageController:
    
    def __init__(self) -> None:
        self.VALID_EXTENSIONS = (".jpg", ".jpeg", ".png")
        self.image_service = ImageService()

    def __is_valid_image(self, files: ImmutableMultiDict[str, FileStorage]) -> Tuple[Response, int]:
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
            
    def process_images_handler(self, files: ImmutableMultiDict[str, FileStorage]) -> Tuple[ImageType, Tuple[int, int]] | Tuple[Response, int]:
        """
        Handler for the POST route that processes the image.

        Args:
            files (ImmutableMultiDict[str, FileStorage]): Files from the request form-data

        Returns: Image preprocessed to identify number of faces.
        """
    
        try:
            # Validate image 
            json_msg, status = self.__is_valid_image(files=files)
            if status != 200:
                return json_msg, status
            
            # Get Image from form-data
            image = files["image"]
            
            # Read image bytes
            image_bytes = BytesIO(image.stream.read())
            
            # Open image using PIL Library
            image = Image.open(image_bytes)
            img_shape = image.size # Get dimensions
            
            return image, img_shape
        except InvalidImageError as e:
            return jsonify(
                msg=e.message,
                status=e.status_code
            ), e.status_code
        except Exception as e:
            return jsonify(
                msg=str(e),
                status=500
            ), 500
            
    def identify_faces(self, image: ImageType, image_shape: Tuple[int, int]) -> Tuple[Response, int]:
        try:
            response = self.image_service.detect_face(image)
            
            response = {
                "faces": response,
                "status": 200,
                "img_shape": image_shape
            }
            
            return response, 200
        except Exception as e:
            raise ValueError(f"Error while trying to identify_faces: {e}")
    
    def classificate_faces(self, faces = Any, boxes = None, original_image: ImageType = None):
        try:
            classificated_faces, status = self.image_service.identify_age(faces=faces)
            predictions = classificated_faces.json()
            isMinor, score = zip(*predictions["predictions"])
            pil_image = original_image.convert("RGB")
            
            for i, box in enumerate(boxes):
                x_min, y_min, x_max, y_max = box
                w, h = x_max - x_min, y_max - y_min

                if isMinor[i] == 1:
                    # Si es menor, pixela la cara
                    face_region = pil_image.crop((x_min, y_min, x_max, y_max))
                    face_region = face_region.resize((w // 10, h // 10), resample=Image.BILINEAR)
                    face_region = face_region.resize((w, h), Image.NEAREST)
                    pil_image.paste(face_region, (x_min, y_min))
                      
            print(score)
            print(isMinor)
                        
            if status == 200:
                return pil_image, 200

            else:
                return jsonify(
                    msg=f"Error while trying to classificate_faces: {classificated_faces}",
                    status=status
                )
        except Exception as e:
            return f"Error while trying to classificate faces: {e}", 500