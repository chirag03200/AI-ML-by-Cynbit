import streamlit as st
from transformers import pipeline
from PIL import Image
import torch

# ------------------------
# App Config
# ------------------------
st.set_page_config(
    page_title="🖼 AI Image Caption Generator",
    page_icon="🖼",
    layout="wide"
)

st.markdown(
    """
    <style>
    .stApp { background-color: #f5f7fa; }
    .caption-box {
        padding: 15px;
        background-color: #ffffff;
        border-radius: 10px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
        font-size: 18px;
    }
    .title-text {
        text-align: center;
        font-size: 32px;
        color: #333;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ------------------------
# Load Model
# ------------------------
@st.cache_resource
def load_model(model_name="Salesforce/blip-image-captioning-base"):
    return pipeline("image-to-text", model=model_name, device=0 if torch.cuda.is_available() else -1)

# ------------------------
# UI Title
# ------------------------
st.markdown('<p class="title-text">🖼 AI Image Caption Generator</p>', unsafe_allow_html=True)

# Sidebar
st.sidebar.header("⚙️ Settings")
model_choice = st.sidebar.selectbox(
    "Model",
    ["Salesforce/blip-image-captioning-base", "Salesforce/blip-image-captioning-large"]
)
max_tokens = st.sidebar.slider("Max new tokens", 10, 100, 30)

# Load selected model
caption_model = load_model(model_choice)

# ------------------------
# File Upload
# ------------------------
uploaded_image = st.file_uploader("📤 Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_image:
    image = Image.open(uploaded_image).convert("RGB")

    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.image(image, caption="Uploaded image", use_container_width=True)

    with col2:
        if st.button("✨ Generate Caption", use_container_width=True):
            with st.spinner("Analyzing image..."):
                result = caption_model(image, max_new_tokens=max_tokens)
                caption_text = result[0]['generated_text']

            st.markdown("#### 📝 Generated Caption")
            st.markdown(f"<div class='caption-box'>{caption_text}</div>", unsafe_allow_html=True)

            st.caption(f"Model: `{model_choice}` | Max tokens: {max_tokens}")
