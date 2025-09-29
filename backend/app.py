from fastapi import FastAPI, UploadFile, File
from backend.workers.detectors.ocrdetector import extract_text

from workers.detectors.regexdetector import detect_pii_with_regex
from workers.detectors.nerdetector import detect_pii_with_ner
from workers.detectors.ensemble import ensemble_detections
import shutil

app = FastAPI()

@app.post("/ocr/")
async def ocr_api(file: UploadFile = File(...)):
    temp_path = f"temp_{file.filename}"

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Step 1: Extract text via OCR
    text, data = extract_text(temp_path)

    # Step 2: Run Regex + NER
    regex_results = detect_pii_with_regex(text)
    ner_results = detect_pii_with_ner(text)

    # Step 3: Unify detections with ensemble
    all_results = ensemble_detections(regex_results, ner_results, text)

    return {
        "text": text,
        "boxes": data,
        "pii": all_results
    }
