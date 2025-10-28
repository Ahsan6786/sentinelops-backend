from flask import Flask, jsonify
from flask_cors import CORS
import random
import os

# ----------- APP INITIALIZE -----------
app = Flask(__name__)
CORS(app)

# ----------- METRICS API (JSON Format for Firebase) -----------
@app.route('/metrics')
def metrics():
    cpu = random.randint(10, 95)
    memory = random.randint(10, 90)
    requests = random.randint(100, 500)
    errors = random.randint(0, 10)
    return jsonify({
        "cpu": cpu,
        "memory": memory,
        "requests": requests,
        "errors": errors
    })

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
    # Render (Cloud) port auto-detect, local default = 5050
    port = int(os.environ.get("PORT", 5050))
    app.run(host='0.0.0.0', port=port)
