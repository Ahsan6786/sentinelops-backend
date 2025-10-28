from flask import Flask, jsonify
from flask_cors import CORS
import psutil
import os
import time

app = Flask(__name__)
CORS(app)

# ----------- REAL METRICS (LIVE DATA) -----------
@app.route('/metrics')
def metrics():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    requests = int(time.time()) % 500  # demo request counter for now
    errors = int(time.time()) % 10     # demo error count for now
    
    return jsonify({
        "cpu": cpu,
        "memory": memory,
        "requests": requests,
        "errors": errors
    })

# ----------- THREAT DETECTION -----------
@app.route('/threat')
def threat():
    status = "SAFE ✅" if psutil.cpu_percent(interval=0.5) < 80 else "⚠️ HIGH CPU LOAD DETECTED"
    return jsonify({"status": status})

# ----------- REPORTS -----------
@app.route('/reports')
def reports():
    return jsonify({"message": "Report downloaded successfully!"})

# ----------- MAIN SERVER RUN -----------
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5050))
    app.run(host='0.0.0.0', port=port)
