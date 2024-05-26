import requests
from datetime import datetime
from flask import jsonify

def get_health_check(server_started_at: int):
    now = datetime.now()
    time_alive = (now - server_started_at)
    
    return {
        "started_at": server_started_at,
        "now": now,
        "time_alive": str(time_alive)
    }
    
def get_health_from_container(container_name: str):
    try:
        response = requests.get(container_name)
    
        if response.status_code == 200:
            data = response.json()
            face_detector_init = data["server_init"]
            face_detector_datetime = datetime.strptime(face_detector_init, "%Y-%m-%d %H:%M:%S")
        else:
            raise ValueError("Error while trying to recover face_detector server init")
        
        return get_health_check(server_started_at=face_detector_datetime)
    except Exception as e:
        return jsonify(msg=str(e), status=500)