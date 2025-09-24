from workers.detectors.nerdetector import detect_pii_with_ner

sample_text = """
John Doe works at Google in New York. His email is john@example.com.
"""

results = detect_pii_with_ner(sample_text)
for res in results:
    print(f"{res['type']}: {res['value']} (Context: {res['context']})")
