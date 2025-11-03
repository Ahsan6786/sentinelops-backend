from flask import Flask, jsonify, Response, request
from flask_cors import CORS
import psutil
import os
from prometheus_client import Counter

app = Flask(__name__)
CORS(app)

# ----------- Prometheus Counters (New) -----------
REQUEST_COUNT = Counter('total_requests', 'Total requests handled')
ERROR_COUNT = Counter('error_requests', 'Total errors logged')

# ----------- Count Every Request -----------
@app.before_request
def before_request():
    REQUEST_COUNT.inc()

# ----------- Handle Errors (Increase error counter) -----------
@app.errorhandler(Exception)
def handle_exception(e):
    ERROR_COUNT.inc()
    return jsonify({"status": "error", "message": str(e)}), 500


# ----------- METRICS JSON (Firebase Dashboard ke liye) -----------
@app.route('/metrics-json')
def metrics_json():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    total_requests = REQUEST_COUNT._value.get()
    total_errors = ERROR_COUNT._value.get()

    return jsonify({
        "cpu": cpu,
        "memory": memory,
        "disk": disk,
        "requests": total_requests,
        "errors": total_errors
    })


# ----------- METRICS TEXT (Prometheus ke liye) -----------
@app.route('/metrics')
def metrics():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent

    # Prometheus-friendly format (extra 2 metrics added)
    metrics_text = (
        f"cpu_usage {cpu}\n"
        f"memory_usage {memory}\n"
        f"disk_usage {disk}\n"
        f"total_requests {REQUEST_COUNT._value.get()}\n"
        f"error_requests {ERROR_COUNT._value.get()}\n"
    )

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
