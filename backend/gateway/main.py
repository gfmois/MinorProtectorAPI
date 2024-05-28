from datetime import datetime

from flask import Flask, request, jsonify
from flask_caching import Cache
import socketio

from src.controllers.image_controller import ImageController
from src.utils import get_health_check, get_health_from_container


app = Flask(f"{__name__}_gateway")
cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache'})
sio_client = socketio.Client()
sio_client.connect('http://localhost:5000')

GATEWAY_INIT = datetime.now()
img_controller = ImageController()

@app.route("/image", methods=["POST"])
def send_image():
    try:
        return img_controller.process_images_handler(request.files)
    except Exception as e:
        return jsonify(error=f"Internal Server Error: {str(e)}", status=500), 500

@app.route("/health")
@cache.cached(timeout=50)
def health_check():
    try:
        # Retrieve health data from face_detector
        face_detector_health_data = sio_client.call('health_request', timeout=60)
        face_detector_health_data = datetime.strptime(face_detector_health_data, "%Y-%m-%d %H:%M:%S")
    except Exception as e:
        return jsonify(error=f"Error connecting to socket server: {str(e)}"), 500
    
    gateway_health = get_health_check(server_started_at=GATEWAY_INIT)

    health_info = {
        "gateway": gateway_health,
        "face_detector": get_health_check(server_started_at=face_detector_health_data)
    }

    return jsonify(health_info)