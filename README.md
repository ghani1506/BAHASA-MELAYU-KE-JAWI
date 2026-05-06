# Melayu ke Jawi Mobile OCR App

Versi ini sesuai digunakan di telefon kerana **tidak memerlukan Tesseract OCR**.

## Ciri Baru

- Boleh upload gambar `.jpg`, `.jpeg`, `.png` sehingga **10 MB**
- Gambar akan dikompres automatik sebelum dihantar ke OCR online
- Tidak perlu install Tesseract
- Boleh eksport hasil ke Microsoft Word

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

Untuk penggunaan sebenar, daftar API key percuma/berbayar di OCR.Space dan masukkan dalam sidebar app.

## Format Disokong

- PDF
- DOCX
- PPTX
- PNG
- JPG
- JPEG

## Nota Penting

Untuk imej besar, aplikasi akan compress gambar kepada saiz kecil sebelum OCR.
Jika gambar terlalu kabur selepas compress, cuba crop gambar atau ambil gambar lebih dekat.
