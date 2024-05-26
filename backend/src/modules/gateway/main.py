from datetime import datetime

from flask import Flask, request, jsonify

from .src.controllers.image_controller import ImageController

app = Flask(__name__)

img_controller = ImageController()

server_started_at = datetime.now()

@app.route("/image", methods=["POST"])
def send_image():
    try:
        return img_controller.process_images_handler(request.files)
    except Exception as e:
        return jsonify(error=f"Internal Server Error: {str(e)}", status=500), 500

@app.route("/health")
def health_check():
    now = datetime.now()
    time_alive = (now - server_started_at)
    
    return {
        "started_at": server_started_at,
        "now": now,
        "time_alive": str(time_alive)
    }