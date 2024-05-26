import sys
sys.path.append("..")

import requests
from datetime import datetime

from flask import Flask, request, jsonify

from src.controllers.image_controller import ImageController
from src.utils import get_health_check

GATEWAY_INIT = datetime.now()
img_controller = ImageController()

app = Flask(f"{__name__}_gateway")

@app.route("/image", methods=["POST"])
def send_image():
    try:
        return img_controller.process_images_handler(request.files)
    except Exception as e:
        return jsonify(error=f"Internal Server Error: {str(e)}", status=500), 500

# FIXME: Rendimiento muy bajo
@app.route("/health")
def health_check():
    try:
        response = requests.get("http://localhost:5000/health")
    
        if response.status_code == 200:
            data = response.json()
            face_detector_init = data["server_init"]
            face_detector_datetime = datetime.strptime(face_detector_init, "%Y-%m-%d %H:%M:%S")
        else:
            raise ValueError("Error while trying to recover face_detector server init")

        
        return {
            "gateway": get_health_check(server_started_at=GATEWAY_INIT),
            "face_detector": get_health_check(server_started_at=face_detector_datetime)
        }
    except Exception as e:
        return jsonify(msg=str(e), status=500)