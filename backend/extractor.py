import os
import tempfile

import fitz
import numpy as np
from docx import Document
from pptx import Presentation
from PIL import Image

_easyocr_reader = None


def get_easyocr_reader():
    global _easyocr_reader
    if _easyocr_reader is None:
        import easyocr
        # EasyOCR tiada model khusus Melayu; English sesuai untuk teks Melayu Rumi.
        _easyocr_reader = easyocr.Reader(["en"], gpu=False)
    return _easyocr_reader


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
            return extract_image(path) if use_ocr else ""
        return ""
    finally:
        try:
            os.remove(path)
        except OSError:
            pass


def extract_pdf(path, use_ocr=True):
    doc = fitz.open(path)
    text_parts = []

    for page in doc:
        page_text = page.get_text("text", sort=True).strip()

        if page_text:
            text_parts.append(page_text)
        elif use_ocr:
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            ocr_text = ocr_pil_image(img)
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
    return ocr_pil_image(image)


def ocr_pil_image(image):
    reader = get_easyocr_reader()
    image_np = np.array(image)

    results = reader.readtext(image_np, detail=0, paragraph=True)

    if not results:
        return ""

    return "\n".join(str(item).strip() for item in results if str(item).strip())
