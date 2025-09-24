from workers.detectors.regexdetector import detect_pii_with_regex
from workers.detectors.nerdetector import detect_pii_with_ner
from workers.detectors.ensemble import ensemble_detections

sample_text = """
John Doe's Aadhaar is 1234 5678 9012. PAN is ABCDE1234F.
He lives in Hyderabad. Call +91 9876543210 or email john@example.com.
"""

regex_matches = detect_pii_with_regex(sample_text)
ner_matches = detect_pii_with_ner(sample_text)
merged = ensemble_detections(regex_matches, ner_matches, sample_text)

for d in merged:
    print(f"{d['type']}: {d['value']} (Confidence: {d['confidence']}, Source: {d['detector']})")
