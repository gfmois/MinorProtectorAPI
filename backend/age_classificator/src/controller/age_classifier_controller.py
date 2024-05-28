from io import BytesIO
import logging
from typing import Tuple, List
import numpy as np
from PIL import Image
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
    
    def preprocess_image(self, img, img_width = 200, img_height = 200, save_path=None):
        if not isinstance(img, np.ndarray):
            raise TypeError("img debe ser un np.ndarray")
        
        print(img.shape)
        
        img_resized = cv2.resize(img, (img_width, img_height))
        img_normalized = img_resized.astype('float32') / 255.0
        img_expanded = np.expand_dims(img_normalized, axis=0)

        if save_path:
            cv2.imwrite(save_path, (img_normalized * 255).astype('uint8'))

        return img_expanded

    def resize_image(self, img_bytes: np.ndarray, img_width = 200, img_height = 200, save_path = False) -> np.ndarray:
        """
        Resizes the image to 200x200 pixels if it is not already this size.

        Args:
            image_file (FileStorage): The image file to resize.

        Returns:
            np.ndarray: The resized image as a numpy array.
        """
         # Convertimos BytesIO a una imagen PIL
        img_pil = Image.open(img_bytes)
        # Convertimos la imagen PIL a una matriz numpy
        img_np = np.array(img_pil)
        
        # Redimensionamos la imagen
        img_resized = cv2.resize(img_np, (img_width, img_height))
        # Normalizamos la imagen
        img_normalized = img_resized.astype('float32') / 255.0
        # Expandimos las dimensiones de la imagen para que sea compatible con el modelo
        img_expanded = np.expand_dims(img_normalized, axis=0)

        if save_path:
            # Guardamos la imagen preprocesada si se especifica una ruta de guardado
            cv2.imwrite(save_path, (img_normalized * 255).astype('uint8'))

        return img_expanded

    def predict_is_minor_adult(self, images: List[List[List[int]]]):
        try:
            # Resize the image if necessary
            print(images[0])
            # resized_images = [self.resize_image(np.ndarray(image)) for image in images]
            # expanded_images = [np.expand_dims(img, axis=0) for img in resized_images]
            
            # Pass the numpy array (resized image) directly to the classifier
            # predictions = [self.classifier_service.make_prediction(image) for image in expanded_images]
            # umbral_predictions = [1 if prediction[0][0] > 0.5 else 0 for prediction in predictions]
            
            # print(umbral_predictions)
            return jsonify(predictions=[]), 200
        except Exception as e:
            logging.error(f"Error during prediction: {str(e)}")
            return jsonify(msg="Error processing the image", status=500), 500