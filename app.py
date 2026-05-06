import streamlit as st
from backend.extractor import extract_text
from backend.jawi_converter import melayu_to_jawi
from backend.word_exporter import export_to_word

st.set_page_config(page_title="Melayu ke Jawi", layout="wide")

st.title("Penukar Bahasa Melayu ke Tulisan Jawi")
st.write(
    "Muat naik PDF, Word, PowerPoint atau gambar. "
    "Sistem akan ekstrak teks, tukar ke Jawi, dan jana fail Microsoft Word."
)

uploaded_file = st.file_uploader(
    "Muat naik fail",
    type=["pdf", "docx", "pptx", "png", "jpg", "jpeg"]
)

if uploaded_file:
    with st.spinner("Memproses fail..."):
        original_text = extract_text(uploaded_file)
        jawi_text = melayu_to_jawi(original_text)
        output_path = export_to_word(original_text, jawi_text)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Teks Asal")
        st.text_area("Melayu", original_text, height=400)

    with col2:
        st.subheader("Teks Jawi")
        st.text_area("Jawi", jawi_text, height=400)

    with open(output_path, "rb") as f:
        st.download_button(
            "Muat Turun Microsoft Word",
            data=f,
            file_name="teks_jawi.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
