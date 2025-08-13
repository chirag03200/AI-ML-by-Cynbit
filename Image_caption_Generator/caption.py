import os
from pathlib import Path
from PIL import Image
from tqdm import tqdm

from transformers import pipeline

# CONFIG
MODEL_NAME = "Salesforce/blip-image-captioning-base"
IMAGE_DIR = Path("sample_images")
OUTPUT_FILE = Path("output_captions.txt")

def load_captioner(model_name: str):
    # device_map="auto" lets it use GPU if available, otherwise CPU
    return pipeline("image-to-text", model=model_name, device_map="auto")

def main():
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)

    # Collect images
    exts = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}
    images = [p for p in IMAGE_DIR.iterdir() if p.suffix.lower() in exts]
    if not images:
        print(f"No images found in {IMAGE_DIR.resolve()}. "
              f"Add at least 5 images or run:")
        return

    captioner = load_captioner(MODEL_NAME)

    lines = []
    print(f"Generating captions with '{MODEL_NAME}'...")
    for img_path in tqdm(images, desc="Captioning"):
        try:
            img = Image.open(img_path).convert("RGB")
            # num_return_sequences=1; max_new_tokens governs caption length
            out = captioner(img, max_new_tokens=30)[0]["generated_text"]
            line = f"{img_path.name}\t{out}"
            lines.append(line)
            print(f"- {img_path.name}: {out}")
        except Exception as e:
            err = f"{img_path.name}\t<error: {e}>"
            lines.append(err)
            print(f"! Error on {img_path.name}: {e}")

    OUTPUT_FILE.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nSaved captions to {OUTPUT_FILE.resolve()}")

if __name__ == "__main__":
    main()
