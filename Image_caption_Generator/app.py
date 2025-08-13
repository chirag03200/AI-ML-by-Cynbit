import streamlit as st
from transformers import pipeline
from PIL import Image
import io
import os

# Page config
st.set_page_config(
    page_title="AI Image Caption Generator",
    layout="centered",
    page_icon="🖼️"
)

# Title
st.markdown(
    "<h1 style='text-align: center; color: #4CAF50;'>🖼️ AI Image Caption Generator</h1>",
    unsafe_allow_html=True
)

# Hugging Face API token
HF_TOKEN = os.getenv("HF_TOKEN")  # Set in Streamlit secrets or env
model_name = "Salesforce/blip-image-captioning-large"

@st.cache_resource
def load_model():
    return pipeline("image-to-text", model=model_name, device_map="auto", use_auth_token=HF_TOKEN)

pipe = load_model()

# File uploader
uploaded_file = st.file_uploader(
    "📤 Upload an image",
    type=["jpg", "jpeg", "png"],
    help="Upload an image to generate a caption."
)

# Generate caption button
if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_container_width=True)

    if st.button("✨ Generate Caption", use_container_width=True):
        with st.spinner("Generating caption..."):
            caption = pipe(image)[0]['generated_text']

        # Display caption in styled card
        st.markdown(
            f"""
            <div style="
                background-color: #f9f9f9;
                padding: 15px;
                border-radius: 10px;
                border: 1px solid #ddd;
                margin-top: 20px;
                box-shadow: 0px 2px 10px rgba(0,0,0,0.05);
                text-align: center;
                font-size: 18px;
                color: #333;
            ">
                <b>Generated Caption:</b><br>{caption}
            </div>
            """,
            unsafe_allow_html=True
        )

# Footer
st.markdown(
    "<p style='text-align: center; color: gray; font-size: 13px;'>Made with ❤️ using Hugging Face & Streamlit</p>",
    unsafe_allow_html=True
)
