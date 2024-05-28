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
        img = cv2.imdecode(np.frombuffer(img_buffer.read(), np.uint8), 1)
        results = self.model(img)
        return results[0]
    
    def get_boxes(self, results):
        return results.boxes
    
    def pixelate(self, img, pixel_size = (20, 20)):
        height, width = img.shape[:2]
        small_image = cv2.resize(img, (width // pixel_size, height // pixel_size))
        pixelated_image = cv2.resize(small_image, (width, height), interpolation=cv2.INTER_NEAREST)
        
        return pixelated_image
    
    def pixelate_faces(self, img: BytesIO):
        results = self.identify_faces(img_buffer=img)
        boxes = self.get_boxes(results)
        
        # NOTE: test this
        _img = cv2.imread(img)
        
        for box in boxes:
            x_min, y_min, x_max, y_max = map(int, box.xyxy.tolist()[0])
            
            face = _img[y_min:y_max, x_min:x_max]
            blur_face = self.pixelate(_img)
            
            _img[y_min:y_max, x_min:x_max] = blur_face
            
            cv2.imwrite("./blur_image.png", _img)
            
            return _img