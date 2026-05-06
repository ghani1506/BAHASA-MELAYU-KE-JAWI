from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import os

def export_to_word(rumi, jawi):

    os.makedirs("output", exist_ok=True)

    doc = Document()

    doc.add_heading("Melayu ke Jawi", level=1)

    doc.add_heading("Rumi", level=2)
    doc.add_paragraph(rumi)

    doc.add_heading("Jawi", level=2)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    run = p.add_run(jawi)
    run.font.size = Pt(18)

    path = "output/hasil_jawi.docx"

    doc.save(path)

    return path
