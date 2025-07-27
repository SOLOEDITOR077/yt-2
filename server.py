from flask import Flask, request, jsonify
import subprocess
import os
import uuid

app = Flask(__name__)

# Home route to prevent 404 on root path
@app.route("/", methods=["GET"])
def home():
    return "✅ Flask YouTube Downloader Backend is Live!"

# Download video route
@app.route('/')
def home():
    return "Flask YouTube Downloader Backend is Live!"
    try:
        data = request.get_json()
        url = data.get("url")

        if not url:
            return jsonify({"error": "❌ No URL provided."}), 400

        # Create a unique filename using UUID
        filename = f"{uuid.uuid4()}.mp4"
        output_path = os.path.join("downloads", filename)

        # Create 'downloads' folder if not exists
        os.makedirs("downloads", exist_ok=True)

        # Use yt-dlp to download the video
        result = subprocess.run([
            "yt-dlp",
            "-f", "best",
            "-o", output_path,
            url
        ], capture_output=True, text=True)

        if result.returncode != 0:
            return jsonify({"error": "❌ Failed to fetch video.", "details": result.stderr}), 500

        # Return the filename to the frontend
        return jsonify({"success": True, "filename": filename})

    except Exception as e:
        return jsonify({"error": f"❌ An error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
