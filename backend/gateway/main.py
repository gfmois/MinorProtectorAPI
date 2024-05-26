from datetime import datetime

from flask import Flask, request, jsonify

from src.controllers.image_controller import ImageController
from src.utils import get_health_check, get_health_from_container

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
    return {
        "gateway": get_health_check(server_started_at=GATEWAY_INIT),
        "face_detector": get_health_check(server_started_at=get_health_from_container(container_name="http://localhost:5000/health"))
    }