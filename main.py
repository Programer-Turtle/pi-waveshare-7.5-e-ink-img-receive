from nudenet import NudeDetector
from flask import Flask, request, jsonify
from pathlib import Path
from PIL import Image, ImageOps
from pillow_heif import register_heif_opener
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
        return jsonify({"error": "No filename provided"}), 400

    filename = f"{photo.filename}"
    filepath = UPLOAD_DIR / filename

    photo.save(filepath)

    try:
        image = Image.open(filepath)
        image = ImageOps.exif_transpose(image)
        image = image.convert("RGB")

        converted_path = filepath.with_suffix(".jpg")
        image.save(converted_path, "JPEG", quality=100)

    except Exception as e:
        filepath.unlink(missing_ok=True)
        return jsonify({"error": f"Invalid image: {e}"}), 400

    scan_result = detector.detect(str(converted_path))
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