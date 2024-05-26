from flask import Flask

from src.modules.gateway.main import health_check as gateway_health_check, app as gateway
from src.modules.face_detector.main import (
    health_check as face_detector_health_check, 
    app as face_detector
)

app = Flask(f"{__name__}_entrypoint")

app.register_blueprint(gateway)
app.register_blueprint(face_detector)

@app.route("/health")
def health_check():
    return {
        "gateway": gateway_health_check(),
        "face_detector": face_detector_health_check()
    }

# FIXME: Juntar todas las apps de Flask en una
if __name__ == "__main__":
    app.run()