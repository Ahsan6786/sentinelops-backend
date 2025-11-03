from flask import Flask, jsonify, Response
from flask_cors import CORS
import psutil
import os
import mysql.connector

app = Flask(__name__)
CORS(app)

# ----------- AWS RDS Connection Setup -----------
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            database=os.getenv("DB_NAME"),
            port=int(os.getenv("DB_PORT", 3306))
        )
        return conn
    except Exception as e:
        print("Database connection failed:", e)
        return None


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

    metrics_text = (
        f"cpu_usage {cpu}\n"
        f"memory_usage {memory}\n"
        f"disk_usage {disk}\n"
    )
    response = app.response_class(
        response=metrics_text,
        status=200,
        mimetype='text/plain'
    )
    return response


# ----------- TEST RDS CONNECTION ENDPOINT -----------
@app.route('/test-db')
def test_db():
    conn = get_db_connection()
    if not conn:
        return jsonify({"status": "failed", "message": "Database connection failed!"}), 500
    cur = conn.cursor()
    cur.execute("SELECT NOW();")  # Simple query to test connection
    result = cur.fetchone()
    cur.close()
    conn.close()
    return jsonify({"status": "success", "current_time": str(result[0])})


# ----------- APP ENTRY POINT (Render + Local dono ke liye) -----------
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5050))
    app.run(host='0.0.0.0', port=port)
