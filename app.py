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
    
    # GET request - show logs with @ highlighting
    if os.path.exists('logs.txt'):
        with open('logs.txt', 'r') as f:
            raw_content = f.read()
        
        # Escape HTML special chars first for safety
        safe_content = raw_content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        
        # Highlight every @ symbol in yellow
        highlighted = safe_content.replace('@', '<span style="background-color: #ffff00; color: #000; font-weight: bold; padding: 0 2px; border-radius: 2px;">@</span>')
        
        # Return as HTML page instead of plain text
        html_page = f"""<!DOCTYPE html>
<html>
<head>
    <title>C2 Logs</title>
    <style>
        body {{ background: #1a1a1a; color: #e0e0e0; font-family: 'Courier New', monospace; 
               padding: 20px; margin: 0; line-height: 1.6; word-wrap: break-word; }}
        pre {{ white-space: pre-wrap; margin: 0; }}
        .header {{ color: #888; font-size: 0.9em; margin-bottom: 5px; }}
    </style>
</head>
<body>
<pre>{highlighted}</pre>
</body>
</html>"""
        return html_page, 200
    
    return '<!DOCTYPE html><html><body style="background:#1a1a1a;color:#e0e0e0;font-family:monospace;padding:20px;">No logs yet</body></html>', 200

@app.route('/reset', methods=['GET'])
def reset_logs():
    from flask import request as req
    key = req.args.get('key', '')
    if key != 'byebye':
        return 'Unauthorized', 403
    if os.path.exists('logs.txt'):
        open('logs.txt', 'w').close()
        return 'Logs cleared successfully', 200
    return 'No logs to clear', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
