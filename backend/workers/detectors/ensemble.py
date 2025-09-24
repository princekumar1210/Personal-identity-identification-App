from typing import List, Dict, TypedDict
import re

class PIIDetection(TypedDict):
    type: str
    value: str
    start: int
    end: int
    context: str
    detector: str
    confidence: float

STRUCTURED_IDS = {"AADHAAR", "PAN", "PHONE", "EMAIL"}
ID_KEYWORDS = {"aadhaar", "aadhar", "pan"}

def _clean_ner_results(ner_results: List[Dict], text: str) -> List[Dict]:
    """Drop or trim NER entities that are just ID keywords."""
    cleaned = []
    for ent in ner_results:
        val = ent["value"].strip()
        low = val.lower()
        # Drop bare PAN/Aadhaar
        if low in ID_KEYWORDS:
            continue
        # Trim "John Doe's Aadhaar" -> "John Doe"
        if any(k in low for k in ID_KEYWORDS):
            m = re.match(r"^(?P<name>.+?)(?:'s)?\s*(aadhaar|aadhar|pan)$", val, flags=re.IGNORECASE)
            if m and ent["type"] == "PERSON":
                name = m.group("name").strip()
                if name:
                    ent2 = ent.copy()
                    ent2["value"] = name
                    ent2["end"] = ent2["start"] + len(name)
                    cleaned.append(ent2)
            continue
        cleaned.append(ent)
    return cleaned

def ensemble_detections(regex_results: List[Dict], ner_results: List[Dict], text: str) -> List[PIIDetection]:
    all_detections: List[PIIDetection] = []

    # 1. Regex detections (high confidence)
    for res in regex_results:
        all_detections.append({
            **res,
            "detector": "regex",
            "confidence": 0.99,
            "type": res["type"].upper(),
        })

    # 2. Clean NER results
    ner_results = _clean_ner_results(ner_results, text)
    for res in ner_results:
        all_detections.append({
            **res,
            "detector": "ner",
            "confidence": 0.85,
            "type": res["type"].upper(),
        })

    # 3. Sort by start
    all_detections.sort(key=lambda x: x["start"])

    # 4. Resolve overlaps (regex > ner for structured IDs)
    i = 0
    while i < len(all_detections) - 1:
        cur = all_detections[i]
        nxt = all_detections[i + 1]
        if cur["end"] > nxt["start"]:  # overlap
            if cur["detector"] == "regex" and cur["type"] in STRUCTURED_IDS:
                all_detections.pop(i + 1)
                continue
            if nxt["detector"] == "regex" and nxt["type"] in STRUCTURED_IDS:
                all_detections.pop(i)
                continue
        i += 1

    # 5. Deduplicate
    unique = []
    seen = set()
    for d in all_detections:
        key = (d["type"], d["value"], d["start"], d["end"])
        if key in seen:
            continue
        seen.add(key)
        unique.append(d)

    return unique
