from io import BytesIO
import logging
from typing import Tuple, List
import numpy as np
from PIL import Image
from PIL.Image import Image as ImageType
import cv2

from werkzeug.datastructures import ImmutableMultiDict, FileStorage
from flask import jsonify, Response

from src.service.age_classifier_service import AgeClassifierService

class InvalidImageError(Exception):
    """Custom exception for invalid image errors."""
    def __init__(self, message: str, status_code: int):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class AgeClassifierController:
    def __init__(self) -> None:
        self.VALID_EXTENSIONS = (".jpg", ".jpeg", ".png")
        self.classifier_service = AgeClassifierService("./src/data/modelo_ajustado_2020.h5")
        logging.basicConfig(level=logging.INFO)

    def validate_image_file(self, files: ImmutableMultiDict[str, FileStorage]) -> Tuple[Response, int]:
        """
        Validates the image file from the request form-data.

        Args:
            files (ImmutableMultiDict[str, FileStorage]): Files from the request form-data

        Returns:
            Tuple[Response, int]: First value is the result of the image identification, 
                             second value is the status code.
        """
        if "image" not in files:
            return jsonify(msg="No file found in request", status=400), 400
        
        image = files["image"]
        
        if image.filename == "":
            return jsonify(msg="No selected file", status=400), 400
        
        if not image.filename.lower().endswith(self.VALID_EXTENSIONS):
            return jsonify(msg="Not a valid image file", status=400), 400
        
        return jsonify(msg="File is valid", status=200), 200
    
    def preprocess_image(self, img: np.ndarray, img_width = 200, img_height = 200, save_path=None):
        if not isinstance(img, np.ndarray):
            raise TypeError("img debe ser un np.ndarray")
        
        _, buffer = cv2.imencode('.jpg', img)
        imagen_cargada = cv2.imdecode(buffer, cv2.IMREAD_COLOR)
        imagen_cargada_rgb = cv2.cvtColor(imagen_cargada, cv2.COLOR_BGR2RGB)  # Convert to RGB
        img_resized = cv2.resize(imagen_cargada_rgb, (img_width, img_height))
        img_normalized = img_resized.astype('float32') / 255.0
        
        img_expanded = np.expand_dims(img_normalized, axis=0)

        if save_path:
            cv2.imwrite(save_path, (img_normalized * 255).astype('uint8'))

        return img_expanded

    def predict_is_minor_adult(self, images: List[List[List[int]]]):
        try:
            # Resize the image if necessary
            nparrays = [np.array(image) for image in images]
            resized_images = [self.preprocess_image(img=img) for img in nparrays]
             
            # Pass the numpy array (resized image) directly to the classifier
            predictions = [self.classifier_service.make_prediction(image) for image in resized_images]
            umbral_predictions = [1 if prediction[0][0] > 0.4 else 0 for prediction in predictions]
            
            predictions_serialized = [str(pred[0][0]) for pred in predictions]
            
            to_return = list(zip(umbral_predictions, predictions_serialized))
            
            return jsonify(predictions=to_return), 200
        except Exception as e:
            logging.error(f"Error during prediction: {str(e)}")
            return jsonify(msg="Error processing the image", status=500), 500