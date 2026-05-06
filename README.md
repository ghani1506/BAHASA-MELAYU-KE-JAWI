# Melayu ke Jawi Mobile OCR App

Versi ini sesuai digunakan di telefon kerana **tidak memerlukan Tesseract OCR**.

Aplikasi ini menggunakan:
- Streamlit
- OCR.Space API untuk baca teks daripada gambar/PDF scan
- Python backend
- Microsoft Word export

## Cara Pasang

```bash
pip install -r requirements.txt
```

## Cara Jalankan

```bash
streamlit run app.py
```

## OCR API

Default API key ialah demo:

```text
helloworld
```

Untuk penggunaan sebenar, daftar API key percuma di OCR.Space dan masukkan dalam sidebar app.

## Format Disokong

- PDF
- DOCX
- PPTX
- PNG
- JPG
- JPEG

## Nota

Untuk PDF yang sudah ada teks, app akan baca terus.
Untuk gambar atau PDF scan, app akan guna OCR.Space API.
