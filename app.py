from flask import Flask, jsonify, Response
from flask_cors import CORS
import psutil
import os

app = Flask(__name__)
CORS(app)

# ----------- METRICS JSON (Firebase Dashboard ke liye) -----------
@app.route('/metrics-json')
def metrics_json():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    return jsonify({
        "cpu": cpu,
        "memory": memory,
        "disk": disk
    })


# ----------- METRICS TEXT (Prometheus ke liye) -----------
@app.route('/metrics')
def metrics():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent

    # Prometheus-friendly format
    metrics_text = f"cpu_usage {cpu}\nmemory_usage {memory}\ndisk_usage {disk}\n"

    # Flask response with explicit headers
    response = app.response_class(
        response=metrics_text,
        status=200,
        mimetype='text/plain'
    )
    return response


# ----------- APP ENTRY POINT (Render & Local dono ke liye) -----------
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5050))
    app.run(host='0.0.0.0', port=port)
