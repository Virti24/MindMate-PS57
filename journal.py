import json
from pathlib import Path

DATA_FILE = Path(__file__).with_name("journal_entries.json")

MOOD_KEYWORDS = {
    "Happy": ["happy", "great", "good", "excited", "joy", "grateful", "amazing", "proud", "love"],
    "Sad": ["sad", "cry", "lonely", "down", "upset", "hurt", "empty", "miss"],
    "Stressed": ["stress", "stressed", "pressure", "overwhelmed", "deadline", "tired", "exhausted", "burden"],
    "Anxious": ["anxious", "anxiety", "worried", "panic", "nervous", "scared", "fear"],
}

DISTRESS_TERMS = [
    "hopeless",
    "helpless",
    "worthless",
    "can't cope",
    "cannot cope",
    "can't go on",
    "cannot go on",
    "no way out",
    "suicide",
    "suicidal",
    "kill myself",
    "end my life",
    "self harm",
    "self-harm",
    "hurt myself",
    "want to die",
    "don't want to live",
    "do not want to live",
    "abuse",
    "immediate danger"
]


def mood_from_text(text: str):
    value = text.lower()
    distress = any(term in value for term in DISTRESS_TERMS)
    counts = {mood: sum(1 for word in words if word in value) for mood, words in MOOD_KEYWORDS.items()}
    mood = max(counts, key=counts.get) if max(counts.values(), default=0) else "Reflective"
    return mood, distress


def load_entries():
    if not DATA_FILE.exists():
        return []
    try:
        data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        return sorted(data if isinstance(data, list) else [], key=lambda x: x.get("created_at", ""), reverse=True)
    except (json.JSONDecodeError, OSError):
        return []


def save_entry(entry):
    entries = load_entries()
    entries.insert(0, entry)
    DATA_FILE.write_text(json.dumps(entries, ensure_ascii=False, indent=2), encoding="utf-8")


def delete_entry(entry_id):
    entries = [e for e in load_entries() if e.get("id") != entry_id]
    DATA_FILE.write_text(json.dumps(entries, ensure_ascii=False, indent=2), encoding="utf-8")
