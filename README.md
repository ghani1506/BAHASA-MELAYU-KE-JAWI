# Melayu ke Jawi Kamus App

Aplikasi Streamlit untuk menukar teks Bahasa Melayu kepada tulisan Jawi, berdasarkan pendekatan kamus seperti **Daftar Kata Bahasa Melayu: Rumi-Sebutan-Jawi**.

## Ciri Utama

- Upload PDF, DOCX, PPTX, JPG, JPEG, PNG
- Ekstrak teks daripada dokumen
- OCR untuk gambar dan PDF scan
- Tukar Rumi Melayu kepada Jawi
- Utamakan padanan kamus `data/kamus_jawi.csv`
- Peraturan imbuhan asas: ber-, me-, men-, meng-, di-, ke-, se-, pe-, per-, -kan, -an, -nya
- Semakan manual sebelum eksport
- Eksport hasil ke Microsoft Word `.docx`

## Cara Pasang

```bash
pip install -r requirements.txt
```

## Penting Untuk Gambar / PDF Scan

Untuk OCR gambar, pasang Tesseract OCR.

### Windows

Pasang dari:
https://github.com/UB-Mannheim/tesseract/wiki

Laluan biasa:

```text
C:\Program Files\Tesseract-OCR\tesseract.exe
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

## Tambah Kamus Sendiri

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

Lebih banyak entri kamus dimasukkan, lebih tepat hasil Jawi.
