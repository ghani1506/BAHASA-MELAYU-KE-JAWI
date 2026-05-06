import os
import sys
import tempfile

import fitz
from docx import Document
from pptx import Presentation
from PIL import Image
import pytesseract

if sys.platform.startswith("win"):
    default_tesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    if os.path.exists(default_tesseract_path):
        pytesseract.pytesseract.tesseract_cmd = default_tesseract_path


def extract_text(uploaded_file, use_ocr=True):
    suffix = os.path.splitext(uploaded_file.name)[1].lower()

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.getbuffer())
        path = tmp.name

    try:
        if suffix == ".pdf":
            return extract_pdf(path, use_ocr=use_ocr)
        if suffix == ".docx":
            return extract_docx(path)
        if suffix == ".pptx":
            return extract_pptx(path)
        if suffix in [".png", ".jpg", ".jpeg"]:
            return extract_image(path)
        return ""
    finally:
        try:
            os.remove(path)
        except OSError:
            pass


def extract_pdf(path, use_ocr=True):
    doc = fitz.open(path)
    text_parts = []

    for page_index, page in enumerate(doc):
        page_text = page.get_text("text", sort=True).strip()

        if page_text:
            text_parts.append(page_text)
        elif use_ocr:
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            ocr_text = ocr_image(img)
            if ocr_text:
                text_parts.append(ocr_text)

    return "\n\n".join(text_parts).strip()


def extract_docx(path):
    doc = Document(path)
    parts = []

    for p in doc.paragraphs:
        if p.text.strip():
            parts.append(p.text.strip())

    for table in doc.tables:
        for row in table.rows:
            row_text = " ".join(cell.text.strip() for cell in row.cells if cell.text.strip())
            if row_text:
                parts.append(row_text)

    return "\n".join(parts).strip()


def extract_pptx(path):
    prs = Presentation(path)
    text = []

    for slide in prs.slides:
        for shape in slide.shapes:
            if hasattr(shape, "text") and shape.text.strip():
                text.append(shape.text.strip())

    return "\n".join(text).strip()


def extract_image(path):
    image = Image.open(path).convert("RGB")
    return ocr_image(image)


def ocr_image(image):
    try:
        # Teks Melayu Rumi biasanya boleh dibaca dengan model English.
        return pytesseract.image_to_string(image, lang="eng").strip()
    except pytesseract.TesseractNotFoundError:
        raise RuntimeError(
            "Tesseract OCR tidak dijumpai. Sila pasang Tesseract OCR dan pastikan path tesseract.exe betul."
        )
