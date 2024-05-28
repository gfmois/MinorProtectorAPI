from datetime import datetime

from flask import jsonify, Flask, request
from flask_socketio import SocketIO
from flask_cors import CORS

from src.controller.age_classifier_controller import AgeClassifierController

AGE_CLASSIFICATION_INIT = datetime.now()

app = Flask(f"{__name__}_age_classificator")
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

classifier_controller = AgeClassifierController()

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
        faces = request.json
        faces = faces["faces"]
        predictions, status = classifier_controller.predict_is_minor_adult(images=faces)
        
        # print(predictions)
        
        # if status != 200:
        #     return jsonify(msg=predictions.json(), status=status)
        
        # print(predictions)
        return jsonify(
            detections=[True, False, False, False, False, False, False, False, False, False],
            status=200
        )
    except Exception as e:
        return jsonify(error=f"Internal Server Error on idenify: {str(e)}", status=500), 500