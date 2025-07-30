import cv2
from fer import FER
import emoji
import numpy as np

# Initialize the emotion detector (mtcnn=False = Haar Cascade fallback)
detector = FER(mtcnn=False)

# Open webcam
cap = cv2.VideoCapture(0)

# Emoji mapping
def get_emoji(emotion):
    emojis = {
        "happy": "😊", "sad": "😢", "angry": "😡",
        "surprise": "😲", "neutral": "😐", "fear": "😨",
        "disgust": "🤢"
    }
    return emojis.get(emotion, "😐")

# Main loop
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (640, 480))  # Resize for performance

    # Detect faces and emotions
    results = detector.detect_emotions(frame)

    if results:
        for face in results:
            (x, y, w, h) = face["box"]
            emotions = face["emotions"]
            dominant = max(emotions, key=emotions.get)
            emoji_icon = get_emoji(dominant)

            # Draw face rectangle
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # Label with dominant emotion and emoji
            cv2.putText(frame, f"{emoji_icon} {dominant}", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)

            # Draw emotion bars
            bar_x = x
            bar_y = y + h + 20
            for emotion, score in emotions.items():
                cv2.putText(frame, f"{emotion}:", (bar_x, bar_y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
                cv2.rectangle(frame, (bar_x + 80, bar_y - 10),
                              (bar_x + 80 + int(150 * score), bar_y + 10),
                              (0, 255, 255), -1)
                bar_y += 25

    # Add instructions
    cv2.putText(frame, "Press Q to quit", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 200, 200), 2)

    # Show frame
    cv2.imshow("🎯 Real-Time Emotion Detector", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()