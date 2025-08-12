import streamlit as st
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications import mobilenet_v2
from tensorflow.keras.applications.mobilenet_v2 import decode_predictions, preprocess_input
from PIL import Image

# Load Pre-trained Model
model = mobilenet_v2.MobileNetV2(weights="imagenet")

st.title("📷 Image Classification App")
st.write("Upload an image and get the predicted class with confidence score.")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    img = Image.open(uploaded_file).convert("RGB")
    st.image(img, caption="Uploaded Image", use_column_width=True)

    img_resized = img.resize((224, 224))
    img_array = image.img_to_array(img_resized)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    preds = model.predict(img_array)
    decoded = decode_predictions(preds, top=1)[0][0]
    label = decoded[1]
    confidence = decoded[2] * 100

    st.success(f"**Prediction:** {label} ({confidence:.2f}%)")
