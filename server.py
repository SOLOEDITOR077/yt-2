from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import yt_dlp
import uuid
import os

app = Flask(__name__)
CORS(app)  # Enable CORS so frontend can talk to backend

@app.route('/')
def home():
    return '✅ Server is running'

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    file_name = f"{uuid.uuid4()}.mp4"

    ydl_opts = {
        'outtmpl': file_name,
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'quiet': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return send_file(file_name, as_attachment=True)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        if os.path.exists(file_name):
            os.remove(file_name)

if __name__ == '__main__':
    app.run(debug=True)
