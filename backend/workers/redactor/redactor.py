import cv2
import numpy as np
import fitz
def redact_image(image_path: str, boxes: list, output_path: str):
    """
    Redact (black out) regions in an image.

    :param image_path: Path to input image (e.g., 'scanned.jpg')
    :param boxes: List of dicts with 'x1', 'y1', 'x2', 'y2' (top-left and bottom-right coords)
    :param output_path: Path to save redacted image (e.g., 'scanned_redacted.jpg')
    """
    img = cv2.imread(image_path)
    for box in boxes:
        x1, y1, x2, y2 = box['x1'], box['y1'], box['x2'], box['y2']
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 0), -1)  # -1 = filled rectangle
    cv2.imwrite(output_path, img)




def redact_pdf(pdf_path: str, matches: list, output_path: str):
    """
    Redact matched text regions in a PDF with black rectangles.

    :param pdf_path: Path to input PDF (e.g., 'document.pdf')
    :param matches: List of dicts with 'text', 'page', 'x1', 'y1', 'x2', 'y2'
                   (page is 0-based; x1,y1 top-left, x2,y2 bottom-right)
    :param output_path: Path to save redacted PDF (e.g., 'document_redacted.pdf')
    """
    doc = fitz.open(pdf_path)
    for match in matches:
        page = doc[match['page']]
        rect = fitz.Rect(match['x1'], match['y1'], match['x2'], match['y2'])
        annot = page.addRedactAnnot(rect)
        page.apply_redactions()
    doc.save(output_path)






def redact_text_file(text: str, matches: list) -> str:
    """
    Replace detected PII in text with [REDACTED].

    :param text: Input text content
    :param matches: List of dicts with 'start', 'end', 'value' (character positions)
    :return: Redacted text
    """
    redacted = list(text)
    for match in sorted(matches, key=lambda x: x['start'], reverse=True):
        start, end = match['start'], match['end']
        redacted[start:end] = '[REDACTED]'
    return ''.join(redacted)




