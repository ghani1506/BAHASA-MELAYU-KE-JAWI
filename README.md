# Melayu ke Jawi Streamlit App

Aplikasi ini menukar teks Bahasa Melayu daripada PDF, Word, PowerPoint atau gambar kepada tulisan Jawi dan mengeksport hasilnya ke Microsoft Word.

## Cara Pasang Python Packages

```bash
pip install -r requirements.txt
```

## Penting Untuk Gambar / JPG / PNG

Untuk membaca teks daripada gambar, anda mesti pasang **Tesseract OCR** di komputer.

### Windows

1. Muat turun dan pasang Tesseract OCR:
   https://github.com/UB-Mannheim/tesseract/wiki

2. Biasanya lokasi pemasangan:
   ```text
   C:\Program Files\Tesseract-OCR\tesseract.exe
   ```

3. Dalam fail `backend/extractor.py`, baris ini sudah disediakan:
   ```python
   pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
   ```

### Mac

```bash
brew install tesseract
```

### Ubuntu / Linux

```bash
sudo apt install tesseract-ocr
```

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
