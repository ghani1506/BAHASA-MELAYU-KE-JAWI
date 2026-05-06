import streamlit as st
import pandas as pd
from pathlib import Path

from backend.extractor import extract_text
from backend.jawi_converter import StandardJawiConverter
from backend.word_exporter import export_to_word
from backend.dictionary_manager import append_dictionary_entry, load_dictionary_frame

MAX_IMAGE_MB = 10
MAX_IMAGE_BYTES = MAX_IMAGE_MB * 1024 * 1024
KAMUS_PATH = "data/kamus_jawi.csv"

st.set_page_config(
    page_title="Melayu ke Jawi Standard Kamus",
    layout="wide"
)

st.title("Penukar Bahasa Melayu ke Tulisan Jawi Standard")
st.caption("Versi kamus + peraturan ejaan Jawi + OCR online untuk telefon.")

with st.sidebar:
    st.header("Tetapan OCR")
    ocr_api_key = st.text_input(
        "OCR.Space API Key",
        value="helloworld",
        type="password",
        help="Guna demo 'helloworld' atau masukkan API key OCR.Space sendiri."
    )
    use_online_ocr = st.checkbox("Guna OCR online untuk gambar/PDF scan", value=True)

    st.header("Tetapan Jawi")
    mode = st.selectbox(
        "Mod penukaran",
        ["Standard Kamus", "Transliterasi Asas"],
        index=0
    )
    show_debug = st.checkbox("Papar kaedah setiap perkataan", value=False)
    show_dictionary = st.checkbox("Papar kamus", value=False)

tab1, tab2, tab3 = st.tabs(["Tukar ke Jawi", "Tambah ke Kamus", "Panduan"])

with tab1:
    uploaded_file = st.file_uploader(
        "Muat naik PDF, Word, PowerPoint atau gambar",
        type=["pdf", "docx", "pptx", "png", "jpg", "jpeg"]
    )

    manual_text = st.text_area(
        "Atau tampal teks Melayu di sini",
        height=150,
        placeholder="Contoh: Bahasa Melayu ialah bahasa kebangsaan negara Malaysia."
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

            converter = StandardJawiConverter(KAMUS_PATH)

            with st.spinner("Menukar ke tulisan Jawi..."):
                jawi_text, debug_rows = converter.convert_text(
                    original_text,
                    standard_mode=(mode == "Standard Kamus")
                )

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Teks Rumi")
                st.text_area("Rumi", original_text, height=430)

            with col2:
                st.subheader("Teks Jawi")
                edited_jawi = st.text_area(
                    "Semak dan edit Jawi sebelum download",
                    jawi_text,
                    height=430
                )

            if show_debug:
                st.subheader("Kaedah Penukaran")
                st.dataframe(pd.DataFrame(debug_rows), use_container_width=True)

            output_path = export_to_word(original_text, edited_jawi)

            with open(output_path, "rb") as f:
                st.download_button(
                    "Download Microsoft Word",
                    data=f,
                    file_name="hasil_jawi_standard.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )

        except Exception as e:
            st.error("Ralat semasa memproses fail.")
            st.code(str(e))

with tab2:
    st.subheader("Tambah Perkataan ke Kamus")
    st.write("Gunakan ruang ini untuk menambah ejaan Jawi yang betul. Selepas ditambah, perkataan itu akan digunakan untuk penukaran seterusnya.")

    col_a, col_b, col_c = st.columns([1, 1, 1])
    with col_a:
        new_rumi = st.text_input("Perkataan Rumi", placeholder="contoh: kebangsaan")
    with col_b:
        new_jawi = st.text_input("Ejaan Jawi", placeholder="contoh: کبڠساءن")
    with col_c:
        new_cat = st.text_input("Kategori", value="pengguna")

    if st.button("Tambah ke Kamus"):
        if new_rumi.strip() and new_jawi.strip():
            append_dictionary_entry(KAMUS_PATH, new_rumi.strip(), new_jawi.strip(), new_cat.strip())
            st.success(f"Ditambah: {new_rumi} → {new_jawi}")
        else:
            st.warning("Sila isi perkataan Rumi dan ejaan Jawi.")

    if show_dictionary:
        st.subheader("Kamus Semasa")
        st.dataframe(load_dictionary_frame(KAMUS_PATH), use_container_width=True)

with tab3:
    st.subheader("Prinsip App Ini")
    st.markdown(
        """
        **Keutamaan penukaran:**

        1. Cari perkataan penuh dalam kamus.
        2. Cari bentuk berimbuhan seperti `ber-`, `me-`, `men-`, `meng-`, `di-`, `ke-`, `se-`, `pe-`, `per-`, `-kan`, `-an`, `-nya`.
        3. Tangani kata ganda seperti `baik-baik`, `kanak-kanak`.
        4. Tangani partikel seperti `-lah`, `-kah`, `-pun`.
        5. Jika tiada padanan, gunakan peraturan fonetik/vokal asas.
        6. Hasil masih boleh diedit sebelum dieksport ke Word.

        **Nota penting:** Untuk ketepatan sangat tinggi, masukkan lebih banyak entri rasmi ke dalam `data/kamus_jawi.csv`.
        """
    )
