from nudenet import NudeDetector
from flask import Flask, request, jsonify
from pathlib import Path
from PIL import Image
import display
import uuid

app = Flask(__name__)
detector = NudeDetector()

blocked_catagories = ["BUTTOCKS_EXPOSED", "FEMALE_BREAST_EXPOSED", "FEMALE_GENITALIA_EXPOSED", "MALE_GENITALIA_EXPOSED", "ANUS_EXPOSED"]

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.post("/upload")
def upload_photo():
    if "photo" not in request.files:
        return jsonify({"error": "No photo provided"}), 400

    photo = request.files["photo"]

    if not photo.filename:
        return jsonify({"error": "No filename provided"}), 40

    filename = f"{photo.filename}"
    filepath = UPLOAD_DIR / filename

    photo.save(filepath)
    scan_result = detector.detect(str(filepath))
    flagged = False
    for result in scan_result:
        if result["class"] in blocked_catagories and result["score"] >= .5:
            flagged = True

    if flagged:
        filepath.unlink(missing_ok=True)
        return jsonify({"error": "Image blocked"}), 403

    try:
        display.display_image(str(filepath))
        filepath.unlink(missing_ok=True)
    except Exception:
        filepath.unlink(missing_ok=True)
        return jsonify({"error": "Invalid image"}), 400

    return jsonify({
        "success": True,
        "filename": filename
    })

@app.get("/")
def index():
    return "Photo API is running"

app.run(host="0.0.0.0", port=5050)