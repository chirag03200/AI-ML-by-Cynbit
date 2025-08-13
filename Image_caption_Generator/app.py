from transformers import pipeline
import streamlit as st
from PIL import Image
import tempfile

@st.cache_resource
def load_model():
    return pipeline("image-to-text", model="nlpconnect/vit-gpt2-image-captioning")

st.set_page_config(page_title="Image Caption Generator", page_icon="🖼️", layout="centered")
st.title("🖼️ Image Caption Generator")

pipe = load_model()

uploaded_image = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])

if uploaded_image:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        image.save(tmp.name)
        result = pipe(tmp.name)

    caption = result[0]["generated_text"]
    st.subheader("Generated Caption:")
    st.success(caption)
