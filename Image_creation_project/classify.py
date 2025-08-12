import os
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications import mobilenet_v2
from tensorflow.keras.applications.mobilenet_v2 import decode_predictions, preprocess_input
import matplotlib.pyplot as plt

# Paths
IMAGE_FOLDER = "images"
OUTPUT_FOLDER = "outputs"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Load Pre-trained Model
model = mobilenet_v2.MobileNetV2(weights="imagenet")

# Function to classify a single image
def classify_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    preds = model.predict(img_array)
    decoded = decode_predictions(preds, top=1)[0][0]
    label = decoded[1]
    confidence = decoded[2] * 100
    return label, confidence

# Loop through all images
for img_file in os.listdir(IMAGE_FOLDER):
    img_path = os.path.join(IMAGE_FOLDER, img_file)
    label, confidence = classify_image(img_path)

    print(f"{img_file} ➡ {label} ({confidence:.2f}%)")

    # Save output image with prediction text
    img = image.load_img(img_path)
    plt.imshow(img)
    plt.axis("off")
    plt.title(f"{label} ({confidence:.2f}%)", fontsize=12)
    output_path = os.path.join(OUTPUT_FOLDER, f"pred_{img_file}")
    plt.savefig(output_path)
    plt.close()
