from fastapi import FastAPI, UploadFile, File
from ocr import extract_text
from categorizer import categorize
from advisor import get_advice
import shutil

app = FastAPI()

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    with open("temp.png", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    text = extract_text("temp.png")
    category = categorize(text)
    advice = get_advice(text)
    return {"text": text, "category": category, "advice": advice}