import base64
from io import BytesIO
from datetime import datetime

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from PIL.Image import Image as ImageType
import socketio

from src.controllers.image_controller import ImageController
from src.utils import get_health_check, get_health_from_container

app = Flask(f"{__name__}_gateway")
CORS(app, resources={r"/*": {"origins": "*"}})  # Permite CORS para todos los dominios en todas las rutasCORS(app)
face_detector_client = socketio.Client()
age_detector_client = socketio.Client()

face_detector_client.connect('http://face_detector:5000')
age_detector_client.connect('http://age_classificator:5002')

GATEWAY_INIT = datetime.now()
img_controller = ImageController()

@app.route("/image", methods=["POST"])
def send_image():
    try:
        processed_image = img_controller.process_images_handler(request.files)
        response, status = img_controller.identify_faces(*processed_image)
        faces = response["faces"]["faces"]
        boxes = response["faces"]["boxes"]
        
        if status != 200:
            return jsonify(msg=response["faces"], status=response["status"])
        
        response, status = img_controller.classificate_faces(faces=faces, boxes=boxes, original_image=processed_image[0])
        
        if isinstance(response, ImageType):
            img_io = BytesIO()
            response.save(img_io, "JPEG")
            img_io.seek(0)
            img_data = img_io.getvalue()
            img_base64 = base64.b64encode(img_data).decode('utf-8')
            return jsonify(image=f"data:image/jpeg;base64,{img_base64}")
        
        return jsonify(response=response.json(), status=status), status
    except Exception as e:
        return jsonify(error=f"Internal Server Error: {str(e)}", status=500), 500

@app.route("/health")
def health_check():
    try:
        # Retrieve health data from face_detector
        face_detector_health_data = face_detector_client.call('health_request', timeout=60)
        face_detector_health_data = datetime.strptime(face_detector_health_data, "%Y-%m-%d %H:%M:%S")
        
        # Retrieve health data from age_classificator
        age_detector_health_data = age_detector_client.call('health_request', timeout=60)
        age_detector_health_data = datetime.strptime(age_detector_health_data, "%Y-%m-%d %H:%M:%S")
    except Exception as e:
        return jsonify(error=f"Error connecting to socket server: {str(e)}"), 500
    
    gateway_health = get_health_check(server_started_at=GATEWAY_INIT)

    health_info = {
        "gateway": gateway_health,
        "face_detector": get_health_check(server_started_at=face_detector_health_data),
        "age_classificator": get_health_check(server_started_at=age_detector_health_data)
    }

    return jsonify(health_info)
    return jsonify(health_info)