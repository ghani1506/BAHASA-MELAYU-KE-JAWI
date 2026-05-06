import streamlit as st
from backend.extractor import extract_text
from backend.jawi_converter import convert_text
from backend.word_exporter import export_to_word

st.set_page_config(page_title="Melayu ke Jawi")

st.title("Penukar Melayu ke Jawi")

uploaded_file = st.file_uploader(
    "Upload file",
    type=["pdf","docx","pptx","png","jpg","jpeg"]
)

manual = st.text_area("Atau tampal teks")

if uploaded_file or manual.strip():

    try:
        text = ""

        if uploaded_file:
            text = extract_text(uploaded_file)

        if manual.strip():
            text += "\n" + manual

        if not text.strip():
            st.warning("Tiada teks dijumpai")
            st.stop()

        jawi = convert_text(text)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Rumi")
            st.text_area("rumi", text, height=400)

        with col2:
            st.subheader("Jawi")
            jawi_edit = st.text_area("jawi", jawi, height=400)

        path = export_to_word(text, jawi_edit)

        with open(path, "rb") as f:
            st.download_button(
                "Download Word",
                f,
                file_name="hasil_jawi.docx"
            )

    except Exception as e:
        st.error(str(e))
