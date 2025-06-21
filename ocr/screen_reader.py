import os
import re
from datetime import datetime
from PIL import ImageGrab, Image
import pytesseract
from config import TESSERACT_PATH

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
SAVE_PATH = os.path.join(os.getcwd(), "screenshots")
os.makedirs(SAVE_PATH, exist_ok=True)  # ✅ ensure the folder exists


def capture_screen():
    # 🖼 Replace with your actual coordinates (top-left to bottom-right of terminal/editor)
    bbox = (363, 617, 1844, 1041)  # 👈 Change this based on your screen layout

    img = ImageGrab.grab(bbox=bbox)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(SAVE_PATH, f"screenshot_{timestamp}.png")
    img.save(file_path)
    return file_path


def extract_text(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)

    # 🧹 Clean OCR result with regex
    cleaned_text = re.sub(r'[^A-Za-z0-9:()\[\]\n\/\.\'\"\-\_\=\>\<\s]', '', text)

    # Remove tiny garbage lines
    lines = cleaned_text.splitlines()
    filtered_lines = [line for line in lines if len(line.strip()) > 10]
    cleaned_text = "\n".join(filtered_lines)

    return cleaned_text

