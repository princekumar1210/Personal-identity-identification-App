from workers.detectors.ocrdetector import extract_text

image_path = "sample.jpg"  # place a test image (scan, Aadhaar card, etc.) in backend/ folder

text, data = extract_text(image_path)
print("EXTRACTED TEXT:")
print(text)
print("BOUNDING BOXES AND CONFIDENCE:")
print(data)
