import csv
import re
from pathlib import Path


class StandardJawiConverter:
    """
    Enjin Jawi berasaskan:
    1. Kamus penuh dahulu.
    2. Analisis imbuhan.
    3. Kaedah vokal/suku kata asas.
    4. Transliterasi fallback.
    """

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

        self.consonants = {
            "b": "ب",
            "c": "چ",
            "d": "د",
            "f": "ف",
            "g": "ݢ",
            "h": "ه",
            "j": "ج",
            "k": "ک",
            "l": "ل",
            "m": "م",
            "n": "ن",
            "p": "ڤ",
            "q": "ق",
            "r": "ر",
            "s": "س",
            "t": "ت",
            "v": "ۏ",
            "w": "و",
            "x": "کس",
            "y": "ي",
            "z": "ز",
        }

        self.vowels = set("aeiou")

        self.prefixes = [
            "memper", "diper", "meng", "meny", "men", "mem", "me",
            "peng", "peny", "pen", "pem", "pe", "ber", "bel", "ter", "per",
            "di", "ke", "se"
        ]

        self.suffixes = [
            "kannya", "annya", "kan", "an", "nya", "lah", "kah", "tah", "pun"
        ]

        self.affix_jawi = {
            "di": "دي",
            "ke": "ک",
            "se": "س",
            "ber": "بر",
            "bel": "بل",
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
            "tah": "ته",
            "pun": "ڤون",
            "kannya": "کنڽ",
            "annya": "نڽ",
        }

        self.separate_prepositions = {
            "di": "دي",
            "ke": "ک",
            "dari": "دري",
            "daripada": "درڤد",
            "kepada": "کڤد",
            "pada": "ڤد",
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

    def convert_text(self, text, standard_mode=True):
        debug_rows = []
        out_lines = []

        for line in text.splitlines():
            tokens = re.findall(r"[A-Za-zÀ-ÿ]+(?:-[A-Za-zÀ-ÿ]+)*|\d+|[^\w\s]|\s+", line, re.UNICODE)
            converted = []

            for token in tokens:
                if token.isspace() or re.fullmatch(r"\d+|[^\w\s]", token, re.UNICODE):
                    converted.append(token)
                    continue

                if standard_mode:
                    jawi, method = self.convert_word_standard(token)
                else:
                    jawi, method = self.convert_word_basic(token)

                converted.append(jawi)
                debug_rows.append({"rumi": token, "jawi": jawi, "kaedah": method})

            out_lines.append("".join(converted))

        return "\n".join(out_lines), debug_rows

    def convert_word_standard(self, word):
        original = word
        word = word.lower()

        if word in self.kamus:
            return self.kamus[word], "kamus penuh"

        if "-" in word:
            return self.convert_hyphenated(word), "kata ganda / sempang"

        if word in self.separate_prepositions:
            return self.separate_prepositions[word], "kata sendi"

        affixed = self.convert_by_affix(word)
        if affixed:
            return affixed, "imbuhan + kamus"

        phonetic = self.convert_by_syllable_rules(word)
        return phonetic, "peraturan vokal/suku kata"

    def convert_word_basic(self, word):
        return self.transliterate_raw(word.lower()), "transliterasi asas"

    def convert_hyphenated(self, word):
        parts = word.split("-")
        converted = []

        for p in parts:
            if p in self.kamus:
                converted.append(self.kamus[p])
            else:
                converted.append(self.convert_by_affix(p) or self.convert_by_syllable_rules(p))

        return "-".join(converted)

    def convert_by_affix(self, word):
        # awalan + akhiran
        for prefix in sorted(self.prefixes, key=len, reverse=True):
            if word.startswith(prefix) and len(word) > len(prefix) + 2:
                rest = word[len(prefix):]

                # kes men + c/d/j/z/t dsb, atau meng + vokal. Cuba kata dasar asal juga.
                candidates = self.root_candidates(prefix, rest)

                for suffix in sorted(self.suffixes, key=len, reverse=True):
                    if rest.endswith(suffix) and len(rest) > len(suffix) + 1:
                        raw_root = rest[:-len(suffix)]
                        for root in self.root_candidates(prefix, raw_root):
                            if root in self.kamus:
                                return self.affix_jawi[prefix] + self.kamus[root] + self.affix_jawi[suffix]

                for root in candidates:
                    if root in self.kamus:
                        return self.affix_jawi[prefix] + self.kamus[root]

        # akhiran sahaja
        for suffix in sorted(self.suffixes, key=len, reverse=True):
            if word.endswith(suffix) and len(word) > len(suffix) + 2:
                root = word[:-len(suffix)]
                if root in self.kamus:
                    return self.kamus[root] + self.affix_jawi[suffix]

        return None

    def root_candidates(self, prefix, rest):
        candidates = [rest]

        # Kaedah praktikal untuk awalan nasal.
        if prefix in ["meny", "peny"]:
            candidates.append("s" + rest)
        elif prefix in ["mem", "pem"]:
            candidates.extend(["p" + rest, "b" + rest, "f" + rest])
        elif prefix in ["men", "pen"]:
            candidates.extend(["t" + rest, "d" + rest, "c" + rest, "j" + rest, "z" + rest])
        elif prefix in ["meng", "peng"]:
            candidates.extend(["k" + rest, "g" + rest, rest])

        return list(dict.fromkeys(candidates))

    def convert_by_syllable_rules(self, word):
        """
        Peraturan praktikal:
        - Digraf ng, ny, sy, kh, gh dipetakan dahulu.
        - Vokal awal ditulis dengan alif/ya/wau.
        - Vokal i/e taling sering ya.
        - Vokal u/o sering wau.
        - Vokal a akhir terbuka biasanya tidak semestinya ditulis, kecuali kata pendek/awal.
        - Schwa e pepet sering tidak ditulis.
        """
        chunks = self.segment(word)
        result = []

        for i, ch in enumerate(chunks):
            if ch in self.digraphs:
                result.append(self.digraphs[ch])
                continue

            if len(ch) == 1 and ch in self.consonants:
                result.append(self.consonants[ch])
                continue

            if len(ch) == 1 and ch in self.vowels:
                result.append(self.vowel_to_jawi(ch, i, chunks, word))
                continue

            result.append(ch)

        # ringkaskan alif berlebihan dalam beberapa keadaan
        text = "".join(result)
        text = re.sub("اا+", "ا", text)
        return text

    def segment(self, word):
        chunks = []
        i = 0
        while i < len(word):
            two = word[i:i+2]
            if two in self.digraphs:
                chunks.append(two)
                i += 2
            else:
                chunks.append(word[i])
                i += 1
        return chunks

    def vowel_to_jawi(self, vowel, index, chunks, word):
        prev = chunks[index - 1] if index > 0 else ""
        nxt = chunks[index + 1] if index + 1 < len(chunks) else ""
        at_start = index == 0
        at_end = index == len(chunks) - 1

        if vowel == "a":
            if at_start:
                return "ا"
            # kata sangat pendek seperti "ma", "ya"
            if at_end and len(word) <= 3:
                return "ا"
            # akhir terbuka lazimnya tidak diberi alif dalam banyak kata dasar Melayu
            if at_end:
                return ""
            return "ا"

        if vowel == "i":
            return "اي" if at_start else "ي"

        if vowel == "u":
            return "او" if at_start else "و"

        if vowel == "o":
            return "او" if at_start else "و"

        if vowel == "e":
            # heuristik: e awal diberi alif, e tengah dianggap pepet dan gugur
            if at_start:
                return "ا"
            # jika hujung seperti cafe, beri ya
            if at_end:
                return "ي"
            return ""

        return ""

    def transliterate_raw(self, word):
        result = []
        chunks = self.segment(word)

        for ch in chunks:
            if ch in self.digraphs:
                result.append(self.digraphs[ch])
            elif ch in self.consonants:
                result.append(self.consonants[ch])
            elif ch == "a":
                result.append("ا")
            elif ch in ["i", "e"]:
                result.append("ي")
            elif ch in ["u", "o"]:
                result.append("و")
            else:
                result.append(ch)

        return "".join(result)
