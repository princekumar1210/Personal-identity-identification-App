from workers.detectors.regexdetector import detect_pii_with_regex

sample_text = """
My Aadhaar is 1234 5678 9012. PAN is ABCDE1234F.
Call me at +91 9876543210 or email me at test@example.com.
"""

results = detect_pii_with_regex(sample_text)
for res in results:
    print(f"{res['type']}: {res['value']} (Context: {res['context']})")
