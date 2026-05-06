import fitz
from docx import Document
from pptx import Presentation
from PIL import Image
import pytesseract
import tempfile
import os
import sys

# Untuk Windows. Jika lokasi Tesseract anda berbeza, ubah path ini.
if sys.platform.startswith("win"):
    default_tesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    if os.path.exists(default_tesseract_path):
        pytesseract.pytesseract.tesseract_cmd = default_tesseract_path

def extract_text(uploaded_file):
    suffix = os.path.splitext(uploaded_file.name)[1].lower()

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.getbuffer())
        path = tmp.name

    try:
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
    finally:
        try:
            os.remove(path)
        except OSError:
            pass

def extract_pdf(path):
    text = ""
    doc = fitz.open(path)

    for page in doc:
        text += page.get_text("text", sort=True) + "\n"

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
    try:
        image = Image.open(path)
        image = image.convert("RGB")

        # Guna English OCR dahulu kerana Tesseract biasa tidak ada model "msa".
        # Untuk teks Melayu Rumi, eng biasanya boleh membaca dengan baik.
        return pytesseract.image_to_string(image, lang="eng").strip()

    except pytesseract.TesseractNotFoundError:
        raise RuntimeError(
            "Tesseract OCR tidak dijumpai. Sila pasang Tesseract OCR dan pastikan path "
            "tesseract.exe betul dalam backend/extractor.py."
        )

    except Exception as e:
        raise RuntimeError(f"Gagal membaca teks daripada gambar: {e}")
