"""Analyzes text input against predefined psychological stress categories."""

LIFESTYLE_FACTORS = {
    "Work/College": ["assignment", "exam", "boss", "deadline", "office", "presentation", "study", "college"],
    "Health/Sleep": ["tired", "sleep", "exhausted", "insomnia", "sick", "pain", "gym", "workout"],
    "Social/Family": ["friend", "lonely", "argument", "family", "party", "call", "home"],
    "Financial": ["money", "bills", "expensive", "job", "rent"]
}

def detect_lifestyle_triggers(text: str) -> str:
    """Returns a comma-separated string of identified lifestyle triggers."""
    found_triggers = [
        category for category, words in LIFESTYLE_FACTORS.items() 
        if any(word in text.lower() for word in words)
    ]
    return ", ".join(found_triggers) if found_triggers else "General"