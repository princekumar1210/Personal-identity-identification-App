import re
from typing import List, Dict, Optional

# Aadhaar number: either masked 'XXXX XXXX XXXX' or actual
AADHAAR_PATTERN = r'\b(?:\d{4}\s\d{4}\s\d{4}|\d{4}-?\d{4}-?\d{4})\b'

# PAN card: 5 letters, 4 digits, 1 letter
PAN_PATTERN = r'\b[A-Z]{5}\d{4}[A-Z]{1}\b'

# Indian phone numbers: optional country code, optional dash/space, 10 digits
PHONE_PATTERN = r'(?:\+?91[- ]?)?[6-9]\d{9}\b'

# Email: standard pattern
EMAIL_PATTERN = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

def detect_pii_with_regex(text: str) -> List[Dict[str, str]]:
    """
    Detect PII in text using regex patterns.
    Returns a list of dicts with 'type', 'value', and 'context' for each match.
    """
    patterns = [
        ('AADHAAR', AADHAAR_PATTERN),
        ('PAN', PAN_PATTERN),
        ('PHONE', PHONE_PATTERN),
        ('EMAIL', EMAIL_PATTERN)
    ]
    
    results = []
    for pii_type, pattern in patterns:
        # Find all matches in the text
        for match in re.finditer(pattern, text, re.IGNORECASE):
            span = match.span()
            context_start = max(0, span[0]-20)
            context_end = min(len(text), span[1]+20)
            context = text[context_start:context_end].replace('\n', ' ')
            results.append({
                'type': pii_type,
                'value': match.group(),
                'context': context,
                'start': span[0],
                'end': span[1]
            })
    return results
