# Melayu ke Jawi App — Local OCR Version

Aplikasi Streamlit untuk menukar Bahasa Melayu Rumi kepada tulisan Jawi.

Versi ini:
- Tidak guna API
- Tidak perlukan Tesseract
- Guna EasyOCR untuk gambar dan PDF scan
- Boleh eksport hasil ke Microsoft Word `.docx`

## Cara Pasang

```bash
pip install -r requirements.txt
```

Nota: EasyOCR mungkin mengambil masa semasa pemasangan pertama kerana ia menggunakan PyTorch dan model OCR.

## Cara Jalankan

```bash
streamlit run app.py
```

## Format Disokong

- PDF
- DOCX
- PPTX
- PNG
- JPG
- JPEG

## Cara Tambah Kamus Jawi

Edit fail:

```text
data/kamus_jawi.csv
```

Format:

```csv
rumi,jawi
bahasa,بهاس
melayu,ملايو
```

Lebih banyak entri kamus, lebih tepat hasil Jawi.
