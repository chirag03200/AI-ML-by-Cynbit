import cv2
from fer import FER
import numpy as np

# ------------------ Configuration ------------------
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
BAR_WIDTH = 150
FONT = cv2.FONT_HERSHEY_SIMPLEX

# ------------------ Emoji Mapping ------------------
EMOJI_MAP = {
    "happy": "😊", "sad": "😢", "angry": "😡",
    "surprise": "😲", "neutral": "😐", "fear": "😨",
    "disgust": "🤢"
}

def get_emoji(emotion: str) -> str:
    return EMOJI_MAP.get(emotion, "😐")

# ------------------ Initialize Detector ------------------
detector = FER(mtcnn=False)
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

# ------------------ Main Loop ------------------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))
    results = detector.detect_emotions(frame)

    for face in results:
        (x, y, w, h) = face["box"]
        emotions = face["emotions"]
        dominant = max(emotions, key=emotions.get)
        emoji_icon = get_emoji(dominant)

        # Draw face box
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Draw label with emoji and emotion
        label = f"{emoji_icon} {dominant}"
        cv2.putText(frame, label, (x, y - 10), FONT, 1, (255, 255, 0), 2, cv2.LINE_AA)

        # Draw emotion bars
        bar_y = y + h + 20
        for emotion, score in emotions.items():
            score_percent = int(BAR_WIDTH * score)

            # Emotion label
            cv2.putText(frame, f"{emotion}:", (x, bar_y), FONT, 0.6, (255, 255, 255), 1)

            # Emotion bar
            cv2.rectangle(frame, (x + 80, bar_y - 10), (x + 80 + score_percent, bar_y + 10), (0, 255, 255), -1)
            bar_y += 25

    # Instruction
    cv2.putText(frame, "Press Q to quit", (10, 30), FONT, 0.7, (0, 200, 200), 2)

    # Display result
    cv2.imshow("🎯 Real-Time Emotion Detector", frame)

    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ------------------ Cleanup ------------------
cap.release()
cv2.destroyAllWindows()