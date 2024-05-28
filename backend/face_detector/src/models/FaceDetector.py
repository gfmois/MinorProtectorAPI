import os
from ultralytics import YOLO
import numpy as np
from io import BytesIO
import cv2

# FIXME: Type all methods
class FaceDetector():
    def __init__(self) -> None:
        self.model = YOLO(os.path.join(
            os.getcwd(), "./src/data/YOLOv8_face_detection.pt"), 
            task="detect"
        )
    
    def identify_faces(self, img_buffer: BytesIO):
        img_buffer.seek(0)
        img_array = np.frombuffer(img_buffer.read(), np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        results = self.model(img)
        return results[0]
    
    def get_boxes(self, results):
        return results.boxes
    
    def pixelate(self, face: np.ndarray, pixel_size=(20, 20)):
        height, width = face.shape[:2]
        small_image = cv2.resize(face, (width // pixel_size[0], height // pixel_size[1]))
        pixelated_image = cv2.resize(small_image, (width, height), interpolation=cv2.INTER_NEAREST)

        return pixelated_image
    
    def pixelate_faces(self, original_img: BytesIO, face_boxes):
        try:
            original_img.seek(0)
            file_bytes = np.asarray(bytearray(original_img.read()), dtype=np.uint8)
            _img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        
            for box in face_boxes:
                x_min, y_min, x_max, y_max = map(int, box.xyxy.tolist()[0])
                
                face = _img[y_min:y_max, x_min:x_max]
                blur_face = self.pixelate(face)
                
                _img[y_min:y_max, x_min:x_max] = blur_face
                
            cv2.imwrite("./blur_image.png", _img)
            return _img
        except Exception as e:
            raise ValueError(f"Error while trying to pixelate the faces: {e}")