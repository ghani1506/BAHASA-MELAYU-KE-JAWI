import re

JAWI_MAP = {
    "a": "ا",
    "b": "ب",
    "c": "چ",
    "d": "د",
    "e": "",
    "f": "ف",
    "g": "ݢ",
    "h": "ه",
    "i": "ي",
    "j": "ج",
    "k": "ک",
    "l": "ل",
    "m": "م",
    "n": "ن",
    "o": "و",
    "p": "ڤ",
    "q": "ق",
    "r": "ر",
    "s": "س",
    "t": "ت",
    "u": "و",
    "v": "ۏ",
    "w": "و",
    "x": "کس",
    "y": "ي",
    "z": "ز",
}

SPECIAL_WORDS = {
    "saya": "ساي",
    "awak": "اوق",
    "bahasa": "بهاس",
    "melayu": "ملايو",
    "jawi": "جاوي",
}

def convert_word(word):
    clean = re.sub(r"[^A-Za-zÀ-ÿ]", "", word).lower()

    if clean in SPECIAL_WORDS:
        jawi = SPECIAL_WORDS[clean]
    else:
        jawi = "".join(JAWI_MAP.get(ch.lower(), ch) for ch in clean)

    punctuation = re.sub(r"[A-Za-zÀ-ÿ]", "", word)
    return jawi + punctuation

def melayu_to_jawi(text):
    lines = []

    for line in text.splitlines():
        words = line.split(" ")
        converted = [convert_word(word) if word else "" for word in words]
        lines.append(" ".join(converted))

    return "\n".join(lines)
