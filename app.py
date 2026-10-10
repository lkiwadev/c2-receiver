from flask import Flask, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)
LOG_FILE = "logs.txt"

@app.route('/log', methods=['POST'])
def receive_log():
    data = request.get_data(as_text=True)
    if data:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] {data}\n")
        return 'OK', 200
    return 'No data', 400

@app.route('/logs', methods=['GET'])
def view_logs():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            return f.read(), 200
    return 'No logs yet', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)