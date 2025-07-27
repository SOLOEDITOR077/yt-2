from flask import Flask, request, jsonify, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return "✅ YouTube Downloader is running."

@app.route("/download", methods=["POST"])
def download_video():
    data = request.get_json()
    url = data.get("url")

    if not url or "youtube.com" not in url:
        return jsonify({"error": "❌ Invalid YouTube URL"}), 400

    try:
        video_id = str(uuid.uuid4())
        output_path = os.path.join(DOWNLOAD_FOLDER, f"{video_id}.mp4")

        ydl_opts = {
            'format': '18',  # medium quality mp4
            'outtmpl': output_path,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return send_file(output_path, as_attachment=True)

    except Exception as e:
        print("Download error:", e)
        return jsonify({"error": "❌ Failed to download video. Try another link."}), 500

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
