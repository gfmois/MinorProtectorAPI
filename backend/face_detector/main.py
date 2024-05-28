from datetime import datetime

from flask import request, jsonify, Flask
from flask_socketio import SocketIO, emit
from flask_cors import CORS

from src.controllers.face_detector_controller import FaceDetectorController

FACE_DETECTOR_INIT = datetime.now()
face_controller = FaceDetectorController()

app = Flask(f"{__name__}_face_detector")
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")
    
@app.route("/detect", methods=["POST"])
def face_detector():
    # FIXME: Llamar al modelo YOLOv8-facedetector
    return face_controller.detect_face(request.files)

@socketio.on("connect")
def connection():
    print(f"Client Connected")
    
@socketio.on("disconnect")
def disconnect():
    print(f"Client disconnected")

@socketio.event
def health_request():
    server_init_time = FACE_DETECTOR_INIT.strftime("%Y-%m-%d %H:%M:%S")
    return str(server_init_time)
    
if __name__ == "__main__":
    socketio.run(app, debug=True)