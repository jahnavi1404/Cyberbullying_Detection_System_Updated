import os
import pickle

from textutils import normalize, COMPILED_RULES

BASE = os.path.dirname(os.path.abspath(__file__))
model = pickle.load(open(os.path.join(BASE, "model.pkl"), "rb"))
vectorizer = pickle.load(open(os.path.join(BASE, "vectorizer.pkl"), "rb"))

THRESHOLD = 0.45   # a little below 0.5 so harmful messages are caught rather than missed


def classify(text):
    """Return a dict: is_bullying, label, confidence (0-100), reason."""
    clean = normalize(text)
    if not clean:
        return {"is_bullying": False, "label": "Normal", "confidence": 100, "reason": "Empty message"}

    proba = float(model.predict_proba(vectorizer.transform([clean]))[0][1])  # P(cyberbullying)

    for pattern, why in COMPILED_RULES:
        if pattern.search(clean):
            return {"is_bullying": True, "label": "Cyberbullying",
                    "confidence": round(max(proba, 0.97) * 100), "reason": why}

    if proba >= THRESHOLD:
        return {"is_bullying": True, "label": "Cyberbullying",
                "confidence": round(proba * 100), "reason": "Harmful language detected by the model"}
    return {"is_bullying": False, "label": "Normal",
            "confidence": round((1 - proba) * 100), "reason": "No harmful language detected"}
