from flask import Flask, jsonify
import random

app = Flask(__name__)

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

@app.route('/threat')
def threat():
    status = "SAFE ✅" if random.random() < 0.8 else "⚠️ THREAT DETECTED"
    return jsonify({"status": status})

@app.route('/reports')
def reports():
    return jsonify({"message": "Report downloaded successfully!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
