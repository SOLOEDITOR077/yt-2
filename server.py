from flask import Flask, request, jsonify, send_file
from yt_dlp import YoutubeDL
import os
from uuid import uuid4

app = Flask(__name__)

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.route("/download", methods=["POST"])
def download_video():
    data = request.get_json()
    url = data.get("url")
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    uid = str(uuid4())
    output_path = os.path.join(DOWNLOAD_DIR, f"{uid}.%(ext)s")

    try:
        ydl_opts = {
            "format": "mp4",
            "outtmpl": output_path,
            "noplaylist": True,
            "quiet": True,
            "progress_hooks": [progress_hook],
        }
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        return jsonify({
            "title": info.get("title"),
            "filename": filename,
            "download_url": f"/video/{os.path.basename(filename)}",
            "thumbnail": info.get("thumbnail"),
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def progress_hook(d):
    if d['status'] == 'downloading':
        print(f"Downloading: {d['_percent_str']} of {d['_total_bytes_str']}")

@app.route("/video/<filename>")
def serve_video(filename):
    path = os.path.join(DOWNLOAD_DIR, filename)
    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    return jsonify({"error": "File not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
