from src.modules.gateway.main import health_check as gateway_health_check, app as gateway
from src.modules.face_detector.main import health_check as face_detector_health_check, app as face_detector

from flask import Flask

app = Flask(f"{__name__}_entrypoint")

@app.route("/health")
def health_check():
    return {
        "gateway": gateway_health_check(),
        "face_detector": face_detector_health_check()
    }

if __name__ == "__main__":
    app.run()    
    gateway.run()
    face_detector.run()