import streamlit as st
import pandas as pd

from backend.extractor import extract_text
from backend.jawi_converter import MelayuJawiConverter
from backend.word_exporter import export_to_word

MAX_IMAGE_MB = 10
MAX_IMAGE_BYTES = MAX_IMAGE_MB * 1024 * 1024

st.set_page_config(
    page_title="Melayu ke Jawi Mobile OCR",
    layout="wide"
)

st.title("Penukar Melayu ke Jawi")
st.caption("Versi telefon: boleh upload JPG/JPEG/PNG sehingga 10 MB. Gambar akan dikompres sebelum OCR.")

with st.sidebar:
    st.header("Tetapan OCR")
    st.write("Untuk telefon, gunakan OCR online.")
    ocr_api_key = st.text_input(
        "OCR.Space API Key",
        value="helloworld",
        type="password",
        help="Guna 'helloworld' untuk demo. Untuk penggunaan kerap, daftar API key sendiri."
    )
    use_online_ocr = st.checkbox("Guna OCR online untuk gambar/PDF scan", value=True)
    show_debug = st.checkbox("Papar maklumat padanan", value=False)

uploaded_file = st.file_uploader(
    "Muat naik fail",
    type=["pdf", "docx", "pptx", "png", "jpg", "jpeg"]
)

manual_text = st.text_area(
    "Atau tampal teks Melayu di sini",
    height=140,
    placeholder="Contoh: Bahasa Melayu ialah bahasa kebangsaan."
)

if uploaded_file:
    ext = uploaded_file.name.lower().split(".")[-1]
    if ext in ["png", "jpg", "jpeg"] and uploaded_file.size > MAX_IMAGE_BYTES:
        st.error(f"Saiz imej terlalu besar. Sila upload gambar {MAX_IMAGE_MB} MB ke bawah.")
        st.stop()

if uploaded_file or manual_text.strip():
    try:
        original_text = ""

        if uploaded_file:
            with st.spinner("Membaca fail..."):
                original_text = extract_text(
                    uploaded_file,
                    use_online_ocr=use_online_ocr,
                    ocr_api_key=ocr_api_key
                )

        if manual_text.strip():
            original_text = (original_text + "\n" + manual_text).strip()

        if not original_text.strip():
            st.warning("Tiada teks dapat dibaca. Pastikan gambar jelas atau masukkan API key OCR.Space.")
            st.stop()

        converter = MelayuJawiConverter("data/kamus_jawi.csv")

        with st.spinner("Menukar ke Jawi..."):
            jawi_text, debug_rows = converter.convert_text(original_text)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Teks Rumi")
            st.text_area("Rumi", original_text, height=420)

        with col2:
            st.subheader("Teks Jawi")
            edited_jawi = st.text_area(
                "Semak/edit Jawi sebelum download",
                jawi_text,
                height=420
            )

        if show_debug:
            st.subheader("Padanan Kamus / Peraturan")
            st.dataframe(pd.DataFrame(debug_rows), use_container_width=True)

        output_path = export_to_word(original_text, edited_jawi)

        with open(output_path, "rb") as f:
            st.download_button(
                "Download Microsoft Word",
                data=f,
                file_name="hasil_jawi.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

    except Exception as e:
        st.error("Ralat semasa memproses fail.")
        st.code(str(e))
