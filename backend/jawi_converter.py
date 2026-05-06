kamus = {
    "saya":"ساي",
    "awak":"اوق",
    "bahasa":"بهاس",
    "melayu":"ملايو",
    "jawi":"جاوي",
    "dan":"دان",
    "yang":"يڠ",
    "ini":"اين",
    "itu":"ايتو",
    "dengan":"دڠن",
    "untuk":"اونتوق",
}

map_huruf = {
    "a":"ا",
    "b":"ب",
    "c":"چ",
    "d":"د",
    "e":"",
    "f":"ف",
    "g":"ݢ",
    "h":"ه",
    "i":"ي",
    "j":"ج",
    "k":"ک",
    "l":"ل",
    "m":"م",
    "n":"ن",
    "o":"و",
    "p":"ڤ",
    "q":"ق",
    "r":"ر",
    "s":"س",
    "t":"ت",
    "u":"و",
    "v":"ۏ",
    "w":"و",
    "x":"کس",
    "y":"ي",
    "z":"ز",
}

def convert_word(word):

    w = word.lower()

    if w in kamus:
        return kamus[w]

    out = ""

    for ch in w:
        out += map_huruf.get(ch, ch)

    return out

def convert_text(text):

    words = text.split()

    return " ".join([convert_word(w) for w in words])
