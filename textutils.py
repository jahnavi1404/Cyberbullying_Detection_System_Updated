import re


def normalize(text):
    """Clean a message the same way for training and for prediction."""
    t = str(text).lower()
    t = re.sub(r"http\S+", " ", t)
    t = re.sub(r"@\w+", " ", t)
    t = re.sub(r"(.)\1{2,}", r"\1\1", t)          # stupiddd -> stupidd
    t = re.sub(r"([.!?,;:])(?=[a-z])", r"\1 ", t)  # "address.i have" -> "address. i have"
    t = re.sub(r"\s+", " ", t).strip()
    return t


# Very specific patterns that are almost always harassment, stalking or threats.
# They work together with the machine learning model, so serious messages are
# never missed just because the model has not seen that exact wording before.
RULES = [
    (r"\b(?:i|we)(?:'m|'ve| am| have| had|'d|m|ve)?\b[^.!?]{0,25}\bstalk(?:ing|ed)?\s+(?:you|u|your)\b",
     "Stalking admission"),
    (r"\bi know where (?:you|u) (?:live|stay|study|work|are)\b", "Threatening you know where they are"),
    (r"\b(?:kill|hang|hurt|end)\s+(?:yourself|urself|ur self)\b", "Telling someone to harm themselves"),
    (r"\b(?:go|just|please)\s+(?:and\s+)?die\b", "Telling someone to die"),
    (r"\b(?:i|i'll|ill|i will|i'm going to|im going to|gonna)\s+(?:kill|hurt|beat|find|ruin|destroy|stab|shoot)\s+(?:you|u)\b(?!\s+(?:at|in|on|to|a|an|the|some)\b)",
     "Direct threat"),
    (r"\b(?:send|give|show)\s+me\s+(?:your|ur)\s+(?:nudes?|nude pics?|private (?:photos|pics|pictures))\b",
     "Sexual harassment / blackmail"),
    (r"\b(?:or|otherwise|else)\b[^.!?]{0,30}\b(?:i will|i'll|ill)\s+(?:post|share|leak|expose|tell everyone)\b",
     "Blackmail"),
    (r"\b(?:i|i'll|ill|will)\b[^.!?]{0,15}\b(?:post|share|leak)\b[^.!?]{0,20}\b(?:your|ur)\s+(?:address|number|phone|photos|pictures|pics|secret)\b",
     "Threat to expose private information"),
    (r"\b(?:i'm|im|i am|i have been|i've been|ive been)\s+(?:watching|tracking)\s+(?:you|your (?:every move|location|profile|house|home))\b",
     "Surveillance of the person"),
    (r"\b(?:i'm|im|i am|i have been|i've been|ive been|i will|i'll)\s+following\s+(?:you|u)\s+(?:home|everywhere|around)\b",
     "Following the person"),
    (r"\b(?:nobody|no one|noone)\s+(?:likes|loves|wants|would miss|cares about)\s+(?:you|u)\b", "Social exclusion"),
    (r"\beveryone\s+hates\s+(?:you|u)\b", "Social exclusion"),
]
COMPILED_RULES = [(re.compile(p), why) for p, why in RULES]
