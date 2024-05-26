from datetime import datetime

from flask import request, jsonify, Flask

from src.controllers.face_detector_controller import FaceDetectorController

FACE_DETECTOR_INIT = datetime.now()
face_controller = FaceDetectorController()

app = Flask(f"{__name__}_face_detector")
    
@app.route("/detect", methods=["POST"])
def face_detector():
    return face_controller

@app.route("/health")
def get_server_init():
    return jsonify({"server_init": FACE_DETECTOR_INIT.strftime("%Y-%m-%d %H:%M:%S")})