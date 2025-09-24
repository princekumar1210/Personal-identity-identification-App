import cv2
import pytesseract

def preprocess_image(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Denoise, threshold, deskew if needed
    processed = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)[1]
    return processed

def extract_text(image_path):
    processed = preprocess_image(image_path)
    text = pytesseract.image_to_string(processed)
    data = pytesseract.image_to_data(processed, output_type=pytesseract.Output.DICT)
    # 'data' contains bounding boxes and confidence scores
    return text, data
