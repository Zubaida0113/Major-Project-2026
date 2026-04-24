from flask import Flask, request, jsonify
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# folder to save audio
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/analyze-audio", methods=["POST"])
def analyze_audio():
    print("🔥 API HIT")
    try:
        audio = request.files["audio"]

        file_path = os.path.join(UPLOAD_FOLDER, audio.filename)
        audio.save(file_path)

        # 🔥 FOR NOW (FAKE MODEL OUTPUT)
        result = {
            "transcript": "Water pipe burst near sector 4",
            "category": "Water Supply",
            "priority": "Critical",
            "score": 92
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)