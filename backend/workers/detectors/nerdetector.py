import spacy

nlp = spacy.load("en_core_web_sm")

def detect_pii_with_ner(text: str) -> list:
    """
    Detect PERSON, ORG, GPE (location) entities using spaCy NER.
    Returns a list of dicts with 'type', 'value', 'start', 'end', 'context'.
    """
    doc = nlp(text)
    results = []
    for ent in doc.ents:
        if ent.label_ in ["PERSON", "ORG", "GPE"]:  # Focus on names, orgs, locations
            context_start = max(0, ent.start_char - 20)
            context_end = min(len(text), ent.end_char + 20)
            context = text[context_start:context_end].replace('\n', ' ')
            results.append({
                'type': ent.label_,
                'value': ent.text,
                'start': ent.start_char,
                'end': ent.end_char,
                'context': context
            })
    return results
