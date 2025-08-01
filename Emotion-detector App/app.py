import streamlit as st
import cv2
from fer import FER
import numpy as np
from PIL import Image

# Streamlit page setup
st.set_page_config(page_title="Real-Time Emotion Detector", page_icon="😊", layout="centered")
st.markdown("<h1 style='text-align: center;'>🎥 Real-Time Emotion Detection using Webcam</h1>", unsafe_allow_html=True)

# Load emotion detector
detector = FER(mtcnn=False)

# Emoji mapping
EMOJI_MAP = {
    "happy": "😄", "sad": "😢", "angry": "😠",
    "surprise": "😲", "neutral": "😐", "fear": "😨", "disgust": "🤢"
}

# Helper function: OpenCV to PIL image
def convert_img(img):
    return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

# Checkbox to control webcam
run = st.checkbox("Start Webcam")
FRAME_WINDOW = st.image([])
emotion_text = st.empty()

# Webcam loop
if run:
    cap = cv2.VideoCapture(0)
    st.markdown("**Press Stop Webcam to release the camera.")

    while run:
        success, frame = cap.read()
        if not success:
            st.error("Failed to access webcam.")
            break

        # Detect emotion
        result = detector.top_emotion(frame)

        if result is not None and isinstance(result, tuple):
            emotion, score = result
            if emotion is not None:
                label = f"{emotion.capitalize()} {EMOJI_MAP.get(emotion, '')} ({score*100:.1f}%)"
                cv2.putText(frame, emotion.capitalize(), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (255, 255, 0), 2)
            else:
                label = "No emotion detected"
                cv2.putText(frame, label, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (100, 100, 100), 2)
        else:
            label = "No face or emotion found"
            cv2.putText(frame, label, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (100, 100, 100), 2)

        # Show video frame and label
        FRAME_WINDOW.image(convert_img(frame))
        emotion_text.markdown(f"### Detected Emotion: {label}")
    
    cap.release()
    cv2.destroyAllWindows()
else:
    st.info("Click the checkbox above to start webcam and detect emotions.")