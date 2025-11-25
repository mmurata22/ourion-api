from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import cv2
from pyzbar.pyzbar import decode
import numpy as np
import tempfile
import requests

app = Flask(__name__)
CORS(app)  # allow requests from React

@app.route("/process-image", methods=["POST"])
def process_image():
    if "image" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["image"]

    # Read image into OpenCV
    file_bytes = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    # Decode barcodes
    barcodes = decode(img)

    if not barcodes:
        return jsonify({"error": "No barcode detected"}), 404

    # Use first barcode only for now
    code = barcodes[0].data.decode("utf-8")
    print("BARCODE:", code)

    # Query OpenFoodFacts
    url = f"https://world.openfoodfacts.org/api/v0/product/{code}.json"
    response = requests.get(url).json()

    # Get product + packaging info
    product_info = {
        "barcode": code,
        "name": response.get("product", {}).get("product_name"),
        "packaging": response.get("product", {}).get("packaging"),
        "recycling": response.get("product", {}).get("packaging_recycling"),
    }

    return jsonify(product_info)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
