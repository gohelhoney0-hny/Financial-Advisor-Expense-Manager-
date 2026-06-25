import pytesseract
from PIL import Image

def extract_text(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text
from PIL import Image
import pytesseract

# Tesseract path (Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text(image_path):
    img = Image.open(image_path)   # Open image properly
    img = img.convert("RGB")       # Convert to supported format
    text = pytesseract.image_to_string(img)
    return text