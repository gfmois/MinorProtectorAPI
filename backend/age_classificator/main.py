from datetime import datetime

from flask import request, jsonify, Flask
from flask_socketio import SocketIO, emit
from flask_cors import CORS

AGE_CLASSIFICATION_INIT = datetime.now()

app = Flask(f"{__name__}_age_classificator")
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on("connect")
def connection():
    print("Client Connected")

@socketio.on("disconnect")
def disconnected():
    print("Client Disconnected")
    
@socketio.event
def health_request():
    server_init_time = AGE_CLASSIFICATION_INIT.strftime("%Y-%m-%d %H:%M:%S")
    return str(server_init_time)

@app.route("/identify", methods=["POST"])
def identify_age():
    try:
        return jsonify(
            detections=[True, False, False, False, False, False, False, False, False, False],
            status=200
        )
    except Exception as e:
        return jsonify(error=f"Internal Server Error: {str(e)}", status=500), 500