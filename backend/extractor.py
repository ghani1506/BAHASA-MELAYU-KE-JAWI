import fitz
from docx import Document
from pptx import Presentation
from PIL import Image
import pytesseract
import tempfile
import os
import shutil

# Auto detect tesseract
if shutil.which("tesseract"):
    pytesseract.pytesseract.tesseract_cmd = shutil.which("tesseract")

WINDOWS_PATHS = [
    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
    r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
]

for p in WINDOWS_PATHS:
    if os.path.exists(p):
        pytesseract.pytesseract.tesseract_cmd = p


def extract_text(uploaded_file):

    ext = os.path.splitext(uploaded_file.name)[1].lower()

    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        tmp.write(uploaded_file.getbuffer())
        path = tmp.name

    try:
        if ext == ".pdf":
            return extract_pdf(path)

        if ext == ".docx":
            return extract_docx(path)

        if ext == ".pptx":
            return extract_pptx(path)

        if ext in [".png",".jpg",".jpeg"]:
            return extract_image(path)

        return ""

    finally:
        try:
            os.remove(path)
        except:
            pass


def extract_pdf(path):

    doc = fitz.open(path)
    all_text = []

    for page in doc:
        txt = page.get_text().strip()

        if txt:
            all_text.append(txt)
        else:
            pix = page.get_pixmap()
            img = Image.frombytes("RGB",[pix.width,pix.height],pix.samples)
            all_text.append(ocr(img))

    return "\n".join(all_text)


def extract_docx(path):
    doc = Document(path)
    return "\n".join([p.text for p in doc.paragraphs])


def extract_pptx(path):

    prs = Presentation(path)
    texts = []

    for slide in prs.slides:
        for shape in slide.shapes:
            if hasattr(shape,"text"):
                texts.append(shape.text)

    return "\n".join(texts)


def extract_image(path):

    img = Image.open(path).convert("RGB")
    return ocr(img)


def ocr(img):

    try:
        return pytesseract.image_to_string(img, lang="eng")

    except pytesseract.TesseractNotFoundError:
        raise RuntimeError(
            "Tesseract OCR belum dipasang. "
            "Install dahulu: https://github.com/UB-Mannheim/tesseract/wiki"
        )
