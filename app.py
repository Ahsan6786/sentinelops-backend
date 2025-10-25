from flask import Flask, jsonify, Response
from flask_cors import CORS
import random
import os

# ----------- APP INITIALIZE -----------
app = Flask(__name__)
CORS(app)

# ----------- METRICS API -----------
@app.route('/metrics')
def metrics():
    # Generate random metrics
    cpu = random.randint(10, 95)
    memory = random.randint(10, 90)
    requests = random.randint(100, 500)
    errors = random.randint(0, 10)

    # Return in Prometheus text format
    metrics_text = (
        f'cpu_usage {cpu}\n'
        f'memory_usage {memory}\n'
        f'requests_total {requests}\n'
        f'errors_total {errors}\n'
    )
    return Response(metrics_text, mimetype="text/plain")

# ----------- THREAT DETECTION API -----------
@app.route('/threat')
def threat():
    status = "SAFE ✅" if random.random() < 0.8 else "⚠️ THREAT DETECTED"
    return jsonify({"status": status})

# ----------- REPORTS API -----------
@app.route('/reports')
def reports():
    return jsonify({"message": "Report downloaded successfully!"})

# ----------- MAIN SERVER RUN -----------
if __name__ == '__main__':
    # Automatically detect Render environment port, fallback to 5050 locally
    port = int(os.environ.get("PORT", 5050))
    app.run(host='0.0.0.0', port=port)
