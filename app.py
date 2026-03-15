from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import tensorflow as tf
import numpy as np
from PIL import Image
import os

app = Flask(__name__, static_folder=".")
CORS(app)

# Load trained model
model = tf.keras.models.load_model("model.keras")

# Class labels
class_names = [
'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P',
'Q','R','S','T','U','V','W','X','Y','Z','del','nothing','space'
]

IMG_SIZE = 64

def preprocess_image(image):
    image = image.resize((IMG_SIZE, IMG_SIZE))
    image = np.array(image) / 255.0
    image = np.expand_dims(image, axis=0)
    return image

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/predict", methods=["POST"])
def predict():

    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"})

    file = request.files['file']
    image = Image.open(file).convert("RGB")

    processed = preprocess_image(image)

    predictions = model.predict(processed)

    predicted_index = np.argmax(predictions)
    confidence = float(np.max(predictions))

    predicted_label = class_names[predicted_index]

    return jsonify({
        "prediction": predicted_label,
        "confidence": confidence
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
