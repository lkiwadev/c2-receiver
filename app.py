from flask import Flask, request
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/logs', methods=['GET', 'POST'])
def handle_logs():
    if request.method == 'POST':
        data = request.get_data(as_text=True)
        if data:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with open('logs.txt', 'a') as f:
                f.write(f'[{timestamp}] {data}\n')
            return 'OK', 200
        return 'Empty', 400
    
    # GET request - show logs
    if os.path.exists('logs.txt'):
        with open('logs.txt', 'r') as f:
            return f.read(), 200
    return 'No logs yet', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
