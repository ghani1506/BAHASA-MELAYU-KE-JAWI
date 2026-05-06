import fitz
from docx import Document
from pptx import Presentation
from PIL import Image
import pytesseract
import tempfile
import os

def extract_text(uploaded_file):
    suffix = os.path.splitext(uploaded_file.name)[1].lower()

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.read())
        path = tmp.name

    if suffix == ".pdf":
        return extract_pdf(path)
    elif suffix == ".docx":
        return extract_docx(path)
    elif suffix == ".pptx":
        return extract_pptx(path)
    elif suffix in [".png", ".jpg", ".jpeg"]:
        return extract_image(path)
    else:
        return ""

def extract_pdf(path):
    text = ""
    doc = fitz.open(path)

    for page in doc:
        text += page.get_text("text") + "\n"

    return text.strip()

def extract_docx(path):
    doc = Document(path)
    return "\n".join([p.text for p in doc.paragraphs]).strip()

def extract_pptx(path):
    prs = Presentation(path)
    text = []

    for slide in prs.slides:
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                text.append(shape.text)

    return "\n".join(text).strip()

def extract_image(path):
    image = Image.open(path)
    return pytesseract.image_to_string(image, lang="eng").strip()
