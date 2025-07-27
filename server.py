from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import subprocess
import os
import uuid

app = Flask(__name__)
CORS(app)

# Directory to save downloaded videos
DOWNLOAD_DIR = os.path.join(os.getcwd(), "downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.route('/')
def home():
    return "✅ Flask YouTube Downloader Backend is Live!"

@app.route('/download', methods=['POST'])
def download_video():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "❌ No URL provided."}), 400

    video_id = str(uuid.uuid4())
    output_path = os.path.join(DOWNLOAD_DIR, f"{video_id}.%(ext)s")
    cookies_path = os.path.join(os.getcwd(), "cookies.txt")

    command = [
        "yt-dlp",
        "--cookies", cookies_path,
        "-f", "best",
        "-o", output_path,
        url
    ]

    try:
        subprocess.run(command, check=True)

        # Find the downloaded file (with actual extension)
        downloaded_file = None
        for file in os.listdir(DOWNLOAD_DIR):
            if file.startswith(video_id):
                downloaded_file = os.path.join(DOWNLOAD_DIR, file)
                break

        if not downloaded_file:
            return jsonify({"error": "❌ Download failed or file not found."}), 500

        return send_file(downloaded_file, as_attachment=True)

    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"❌ Failed to fetch video.\n{e}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
