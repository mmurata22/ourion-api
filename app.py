from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
from pyzbar.pyzbar import decode
import numpy as np
import requests
import os

app = Flask(__name__)

CORS(app, resources={
    r"/*": {
        "origins": [
            "https://www.ourion.app",
            "https://ourion.app",
            "http://localhost:3000",
            "http://localhost:5173"
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

def extract_material_category(packaging_str, recycling_str, product_name):
    """
    Extracts the primary material type from packaging strings
    Falls back to product name if packaging data is missing
    """
    if not packaging_str and not recycling_str and not product_name:
        return "unknown"
    
    combined = f"{packaging_str or ''} {recycling_str or ''} {product_name or ''}".lower()
    
    # Check for materials in order of specificity
    if "aluminium" in combined or "aluminum" in combined or "metal can" in combined or "can" in combined:
        return "aluminum"
    elif "plastic" in combined or "pet" in combined or "hdpe" in combined or "pp" in combined or "bottle" in combined:
        return "plastic"
    elif "glass" in combined:
        return "glass"
    elif "cardboard" in combined or "carton" in combined or "paper" in combined or "box" in combined:
        return "cardboard"
    elif "battery" in combined or "batteries" in combined:
        return "batteries"
    elif "steel" in combined or "tin" in combined:
        return "metal"
    # Fallback: common product types
    elif "soda" in combined or "cola" in combined or "pop" in combined:
        return "aluminum"
    else:
        return "unknown"

@app.route("/process-image", methods=["POST"])
def process_image():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200
    
    if "image" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["image"]
    # NEW: Grab the hint from your React scanner
    local_hint = request.form.get("local_cv_guess", "unknown")
    
    # Read image into OpenCV
    file_bytes = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    
    # 1. ATTEMPT BARCODE DECODE (High Precision)
    barcodes = decode(img)
    
    if barcodes:
        code = barcodes[0].data.decode("utf-8")
        url = f"https://world.openfoodfacts.org/api/v0/product/{code}.json"
        response = requests.get(url).json()
        
        product = response.get("product", {})
        packaging = product.get("packaging")
        recycling = product.get("packaging_recycling")
        
        category = extract_material_category(packaging, recycling, product.get("product_name"))
        
        return jsonify({
            "source": "barcode",
            "barcode": code,
            "name": product.get("product_name") or "Known Product",
            "category": category,
            "packaging": packaging,
            "recycling": recycling,
        })

    # 2. FALLBACK TO LOCAL AI HINT (High Flexibility)
    if local_hint != "unknown":
        # Map the YOLO label to your recycling categories
        category = extract_material_category("", "", local_hint)
        
        return jsonify({
            "source": "visual_ai",
            "name": f"Detected {local_hint}",
            "category": category,
            "note": "Classified based on visual shape (no barcode found)."
        })
    
    # 3. ABSOLUTE FAILURE
    return jsonify({"error": "No barcode detected and visual scan uncertain"}), 404

@app.route('/')
def home():
    env = os.getenv('FLASK_ENV', 'production')
    return f"Ourion API is Running! (Environment: {env})"

@app.route('/health')
def health():
    """Health check endpoint for monitoring"""
    return jsonify({
        "status": "healthy", 
        "environment": os.getenv('FLASK_ENV', 'production')
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)