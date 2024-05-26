from datetime import datetime

from flask import Flask

app = Flask(__name__)

server_started_at = datetime.now()

@app.route("/")
def image_receiver():
    return ""

@app.route("/health")
def health_check():
    now = datetime.now()
    time_alive = (now - server_started_at)
    
    return {
        "started_at": server_started_at,
        "now": now,
        "time_alive": str(time_alive)
    }