import os
import re
from datetime import datetime
from PIL import ImageGrab, Image
import pytesseract
from config import TESSERACT_PATH, CAPTURE_BBOX, SCREENSHOTS_PATH

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
os.makedirs(SCREENSHOTS_PATH, exist_ok=True)


def capture_screen():
    img = ImageGrab.grab(bbox=CAPTURE_BBOX)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(SCREENSHOTS_PATH, f"screenshot_{timestamp}.png")
    img.save(file_path)
    return file_path


def extract_text(image_path):
    img = Image.open(image_path)

    # Use LSTM OCR engine for better accuracy on code/terminal text
    custom_config = r"--oem 3 --psm 6"
    text = pytesseract.image_to_string(img, config=custom_config)

    # Light cleanup only — remove non-printable characters but keep
    # all symbols that appear in Python tracebacks and code
    text = re.sub(r"[^\x20-\x7E\n]", "", text)

    # Only drop lines that are pure whitespace or single characters
    # (don't filter by length — short lines matter in tracebacks)
    lines = text.splitlines()
    filtered = [line for line in lines if line.strip()]
    return "\n".join(filtered)