from datetime import datetime

from flask import Blueprint, request, jsonify

from .src.controllers.face_detector_controller import FaceDetectorController

app = Blueprint("face_detector", f"{__name__}_face_detector")
face_controller = FaceDetectorController()

server_started_at = datetime.now()
    
@app.route("/detect", methods=["POST"])
def face_detector():
    return face_controller

def health_check():
    now = datetime.now()
    time_alive = (now - server_started_at)
    
    return {
        "started_at": server_started_at,
        "now": now,
        "time_alive": str(time_alive)
    }