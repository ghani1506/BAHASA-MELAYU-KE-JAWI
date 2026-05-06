import csv
import re
from pathlib import Path


class MelayuJawiConverter:
    def __init__(self, kamus_path="data/kamus_jawi.csv"):
        self.kamus = self.load_kamus(kamus_path)

        self.digraphs = {
            "ng": "ڠ",
            "ny": "ڽ",
            "sy": "ش",
            "kh": "خ",
            "gh": "غ",
            "dz": "ذ",
            "th": "ث",
            "ch": "چ",
        }

        self.letters = {
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

        self.prefixes = [
            "memper", "diper", "meng", "meny", "men", "mem", "me",
            "peng", "peny", "pen", "pem", "pe", "ber", "ter", "per",
            "di", "ke", "se"
        ]

        self.suffixes = ["kannya", "annya", "kan", "an", "nya", "lah", "kah", "pun"]

        self.affix_jawi = {
            "di": "دي",
            "ke": "ک",
            "se": "س",
            "ber": "بر",
            "ter": "تر",
            "per": "ڤر",
            "pe": "ڤ",
            "pen": "ڤن",
            "pem": "ڤم",
            "peng": "ڤڠ",
            "peny": "ڤڽ",
            "me": "م",
            "men": "من",
            "mem": "مم",
            "meng": "مڠ",
            "meny": "مڽ",
            "memper": "ممڤر",
            "diper": "ديڤر",
            "kan": "کن",
            "an": "ن",
            "nya": "ڽ",
            "lah": "له",
            "kah": "که",
            "pun": "ڤون",
            "kannya": "کنڽ",
            "annya": "نڽ",
        }

    def load_kamus(self, path):
        kamus = {}
        p = Path(path)
        if not p.exists():
            return kamus

        with p.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rumi = (row.get("rumi") or "").strip().lower()
                jawi = (row.get("jawi") or "").strip()
                if rumi and jawi:
                    kamus[rumi] = jawi

        return kamus

    def convert_text(self, text):
        debug_rows = []
        lines = []

        for line in text.splitlines():
            tokens = re.findall(r"[A-Za-zÀ-ÿ]+|\d+|[^\w\s]|\s+", line, flags=re.UNICODE)
            converted_tokens = []

            for token in tokens:
                if token.isspace() or re.fullmatch(r"\d+|[^\w\s]", token, flags=re.UNICODE):
                    converted_tokens.append(token)
                    continue

                jawi, method = self.convert_word(token)
                converted_tokens.append(jawi)
                debug_rows.append({"rumi": token, "jawi": jawi, "kaedah": method})

            lines.append("".join(converted_tokens))

        return "\n".join(lines), debug_rows

    def convert_word(self, word):
        lower = word.lower()

        if lower in self.kamus:
            return self.kamus[lower], "kamus"

        affixed = self.convert_by_affix(lower)
        if affixed:
            return affixed, "imbuhan + kamus"

        return self.transliterate_basic(lower), "transliterasi asas"

    def convert_by_affix(self, word):
        for prefix in sorted(self.prefixes, key=len, reverse=True):
            if word.startswith(prefix) and len(word) > len(prefix) + 2:
                rest = word[len(prefix):]

                for suffix in sorted(self.suffixes, key=len, reverse=True):
                    if rest.endswith(suffix) and len(rest) > len(suffix) + 1:
                        root = rest[:-len(suffix)]
                        if root in self.kamus:
                            return self.affix_jawi[prefix] + self.kamus[root] + self.affix_jawi[suffix]

                if rest in self.kamus:
                    return self.affix_jawi[prefix] + self.kamus[rest]

        for suffix in sorted(self.suffixes, key=len, reverse=True):
            if word.endswith(suffix) and len(word) > len(suffix) + 2:
                root = word[:-len(suffix)]
                if root in self.kamus:
                    return self.kamus[root] + self.affix_jawi[suffix]

        return None

    def transliterate_basic(self, word):
        result = []
        i = 0

        while i < len(word):
            two = word[i:i+2]
            if two in self.digraphs:
                result.append(self.digraphs[two])
                i += 2
                continue

            result.append(self.letters.get(word[i], word[i]))
            i += 1

        return "".join(result)
