import streamlit as st
import pandas as pd
from pathlib import Path

from backend.extractor import extract_text
from backend.jawi_converter import MelayuJawiConverter
from backend.word_exporter import export_to_word

st.set_page_config(page_title="Melayu ke Jawi Kamus", layout="wide")

st.title("Penukar Bahasa Melayu ke Tulisan Jawi")
st.caption("Versi kamus + peraturan asas, sesuai dikembangkan dengan Daftar Kata Rumi-Sebutan-Jawi.")

with st.sidebar:
    st.header("Tetapan")
    use_ocr = st.checkbox("Guna OCR untuk PDF/gambar", value=True)
    show_debug = st.checkbox("Papar padanan kamus/peraturan", value=False)
    st.info("Untuk gambar JPG/JPEG/PNG dan PDF scan, pastikan Tesseract OCR sudah dipasang.")

uploaded_file = st.file_uploader(
    "Muat naik PDF, Word, PowerPoint atau gambar",
    type=["pdf", "docx", "pptx", "png", "jpg", "jpeg"]
)

manual_text = st.text_area(
    "Atau tampal teks Melayu di sini",
    height=140,
    placeholder="Contoh: Bahasa Melayu ialah bahasa kebangsaan."
)

if uploaded_file or manual_text.strip():
    try:
        if uploaded_file:
            with st.spinner("Mengekstrak teks..."):
                original_text = extract_text(uploaded_file, use_ocr=use_ocr)
        else:
            original_text = manual_text

        if manual_text.strip() and uploaded_file:
            original_text = original_text + "\n" + manual_text.strip()

        if not original_text.strip():
            st.warning("Tiada teks dapat dibaca. Untuk imej/PDF scan, pastikan OCR aktif dan gambar jelas.")
            st.stop()

        converter = MelayuJawiConverter("data/kamus_jawi.csv")

        with st.spinner("Menukar ke Jawi..."):
            jawi_text, debug_rows = converter.convert_text(original_text)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Teks Asal")
            st.text_area("Rumi", original_text, height=420)

        with col2:
            st.subheader("Teks Jawi")
            edited_jawi = st.text_area("Jawi boleh disemak/edit sebelum muat turun", jawi_text, height=420)

        if show_debug:
            st.subheader("Maklumat Padanan")
            st.dataframe(pd.DataFrame(debug_rows), use_container_width=True)

        output_path = export_to_word(original_text, edited_jawi)

        with open(output_path, "rb") as f:
            st.download_button(
                "Muat Turun Fail Microsoft Word",
                data=f,
                file_name="teks_jawi.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

    except Exception as e:
        st.error("Ralat semasa memproses fail.")
        st.code(str(e))
