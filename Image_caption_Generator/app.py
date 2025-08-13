import io
from PIL import Image
import streamlit as st
from transformers import pipeline

st.set_page_config(page_title="Image Caption Generator (BLIP)", layout="centered")
st.title("🖼️→📝 Image Caption Generator")

@st.cache_resource(show_spinner=False)
def get_captioner(model_name: str):
    # device_map="auto" uses GPU if available; CPU otherwise
    return pipeline("image-to-text", model=model_name)

with st.sidebar:
    st.header("Settings")
    model_choice = st.selectbox(
        "Model",
        ["Salesforce/blip-image-captioning-base", "Salesforce/blip-image-captioning-large"],
        index=0,
        help="Base = faster; Large = better but slower"
    )
    max_tokens = st.slider("Max new tokens", 10, 64, 30, 2,
                           help="Approximate caption length")

uploader = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png", "webp", "bmp"])
generate = st.button("Generate Caption", type="primary", use_container_width=True)

placeholder = st.empty()

if generate:
    if uploader is None:
        st.warning("Please upload an image first.")
    else:
        img_bytes = uploader.read()
        image = Image.open(io.BytesIO(img_bytes)).convert("RGB")

        with st.spinner("Loading model & generating caption..."):
            captioner = get_captioner(model_choice)
            out = captioner(image, max_new_tokens=max_tokens)[0]["generated_text"]

        col1, col2 = st.columns([1, 1])
        with col1:
            st.image(image, caption="Uploaded image", use_column_width=True)
        with col2:
            st.subheader("Generated caption")
            st.write(out)
            st.caption(f"Model: `{model_choice}` | Max tokens: {max_tokens}")

