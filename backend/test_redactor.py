from workers.redactor.redactor import redact_pdf, redact_image, redact_text_file

from workers.redactor.redactor import redact_image
from workers.redactor.redactor import redact_pdf
from workers.redactor.redactor import redact_text_file


boxes = [{'x1': 50, 'y1': 100, 'x2': 200, 'y2': 150}]  # Example box (get from OCR)
redact_image('scanned.jpg', boxes, 'scanned_redacted.jpg')

# Example: PDF redaction

matches = [{'page': 0, 'x1': 100, 'y1': 200, 'x2': 300, 'x2': 250}]  # Example match (get from parser)
redact_pdf('document.pdf', matches, 'document_redacted.pdf')

# Example: Text file redaction

text = open('notes.txt').read()
matches = [{'start': 30, 'end': 45, 'value': 'Aadhaar: 1234 5678 9012'}]  # Example match (get from detection)
redacted_text = redact_text_file(text, matches)
with open('notes_redacted.txt', 'w') as f:
    f.write(redacted_text)
