import streamlit as st
import joblib
import pandas as pd
import os

# Setup
st.set_page_config(page_title="Emotion Detector", page_icon="🧠", layout="centered")

st.markdown("<h1 style='text-align: center;'>🧠 Emotion Detection App</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Type a sentence and we'll predict the emotion it conveys.</p>", unsafe_allow_html=True)

# Load Model  
MODEL_PATH = "emotion_model.pkl"

if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
else:
    st.error("Model file not found! Please train the model first.")
    st.stop()

# Emoji Map 
emojis = {
    "joy": "😄", "anger": "😠", "sadness": "😢",
    "fear": "😨", "love": "❤️", "surprise": "😲" 
}

# Input Section 
with st.form("emotion_form"):
    text_input = st.text_input(" Enter your text:")
    submitted = st.form_submit_button("🔍 Detect Emotion")

# Prediction  
if submitted:
    if not text_input.strip():
        st.warning(" Please enter a valid sentence.")
    else:
        prediction = model.predict([text_input])[0]
        probabilities = model.predict_proba([text_input])[0]

        # Display predicted emotion
        emoji_display = emojis.get(prediction, "❓")
        st.markdown(f"<h3> Detected Emotion: <span style='color:#ff4b4b'>{prediction.capitalize()} {emoji_display}</span></h3>", unsafe_allow_html=True)

        # Optional warning if confidence is low
        confidence = max(probabilities)
        if confidence < 0.5:
            st.info(f" Prediction confidence is low: {confidence:.2f}")

        # Probability bar chart
        st.subheader("📊 Prediction Probabilities")
        prob_df = pd.DataFrame({
            "Emotion": model.classes_,
            "Probability": probabilities
        }).sort_values(by="Probability", ascending=False)

        st.bar_chart(prob_df.set_index("Emotion"))

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center;'>Made with ❤️ using Streamlit & scikit-learn</p>", unsafe_allow_html=True)
