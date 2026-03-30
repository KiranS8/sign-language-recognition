import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image

# Load model
@st.cache_resource
def load_model():
    return tf.keras.models.load_model("asl_cnn_model.keras")

model = load_model()

# Class labels
class_names = [
'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P',
'Q','R','S','T','U','V','W','X','Y','Z','del','nothing','space'
]

IMG_SIZE = 64

def preprocess(image):
    image = image.resize((IMG_SIZE, IMG_SIZE))
    image = np.array(image) / 255.0
    image = np.expand_dims(image, axis=0)
    return image

# UI
st.set_page_config(page_title="Sign Language Recognition")

st.title("Sign Language Recognition")
st.write("Upload an image of a hand sign")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg","png","jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image")

    if st.button("Predict"):
        processed = preprocess(image)
        predictions = model.predict(processed)

        predicted_index = np.argmax(predictions)
        confidence = float(np.max(predictions))

        st.success(f"Prediction: {class_names[predicted_index]}")
        st.info(f"Confidence: {confidence:.2f}")
