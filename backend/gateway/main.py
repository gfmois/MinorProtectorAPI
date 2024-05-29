from datetime import datetime
import json

from flask import Flask, request, jsonify
from flask_caching import Cache
import socketio

from src.controllers.image_controller import ImageController
from src.utils import get_health_check, get_health_from_container


app = Flask(f"{__name__}_gateway")
cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache'})
face_detector_client = socketio.Client()
age_detector_client = socketio.Client()

face_detector_client.connect('http://localhost:5000')
age_detector_client.connect('http://localhost:5002')

GATEWAY_INIT = datetime.now()
img_controller = ImageController()

@app.route("/image", methods=["POST"])
def send_image():
    try:
        processed_image = img_controller.process_images_handler(request.files)
        response, status = img_controller.identify_faces(*processed_image)
        boxes = response["faces"]["faces"]
        
        if status != 200:
            return jsonify(msg=response["faces"], status=response["status"])
        
        response, status = img_controller.classificate_faces(faces=boxes, original_image=processed_image[0])
        return jsonify(response=response.json(), status=status), status
    except Exception as e:
        return jsonify(error=f"Internal Server Error: {str(e)}", status=500), 500

@app.route("/health")
@cache.cached(timeout=50)
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