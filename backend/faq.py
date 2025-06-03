import json, pathlib

_FAQ = json.load(open(pathlib.Path(__file__).parent / "data" / "surgery_faqs.json"))

def lookup(question: str) -> str | None:
    q = question.strip().lower()
    for item in _FAQ:
        if q == item["question"].lower():
            return item["answer"]
    return None
