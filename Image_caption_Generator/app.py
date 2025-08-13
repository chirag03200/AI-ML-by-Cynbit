import streamlit as st
from transformers import pipeline
from PIL import Image

# Page config
st.set_page_config(page_title="🖼️ Image Caption Generator", layout="wide")

# Sidebar settings
st.sidebar.title("⚙️ Settings")
model_name = st.sidebar.selectbox(
    "Choose Model",
    ["nlpconnect/vit-gpt2-image-captioning", "Salesforce/blip-image-captioning-base"],
    index=0
)
st.sidebar.markdown("---")
st.sidebar.write("📌 Upload an image and get a generated caption instantly.")

# Cache model loading
@st.cache_resource
def load_model(model_name):
    return pipeline("image-to-text", model=model_name)

# Load the model
with st.spinner("🔄 Loading model... Please wait."):
    captioner = load_model(model_name)

# Main title
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🖼️ AI Image Caption Generator</h1>", unsafe_allow_html=True)
st.write("Upload an image and let AI describe it for you! 🎯")

# Image uploader
uploaded_image = st.file_uploader("📤 Upload Image", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    image = Image.open(uploaded_image).convert("RGB")
    
    # Show uploaded image
    st.image(image, caption="Uploaded Image", use_container_width=True)
    
    # Generate caption button
    if st.button("✨ Generate Caption", use_container_width=True):
        with st.spinner("Generating caption... ⏳"):
            caption = captioner(image)[0]['generated_text']
        st.success("✅ Caption Generated!")
        st.markdown(f"<h3 style='color: #2196F3;'>📝 {caption}</h3>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("<p style='text-align:center; color:grey;'>Built with ❤️ using Streamlit & Hugging Face</p>", unsafe_allow_html=True)

