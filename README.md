# Melayu ke Jawi Standard Kamus App

Aplikasi Streamlit untuk menukar teks Bahasa Melayu Rumi kepada tulisan Jawi dengan pendekatan:

1. **Kamus dahulu** — rujuk `data/kamus_jawi.csv`
2. **Peraturan ejaan Jawi** — vokal, digraf, imbuhan, kata sendi, partikel, kata ganda
3. **Pembetulan pengguna** — boleh tambah perkataan baharu ke kamus daripada UI
4. **OCR online** — sesuai untuk telefon, tidak perlu Tesseract
5. **Eksport Word** — hasil akhir dimuat turun sebagai `.docx`

## Cara Pasang

```bash
pip install -r requirements.txt
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

## Telefon / Mobile

App ini tidak memerlukan Tesseract. Untuk gambar atau PDF scan, app menggunakan OCR.Space API.

Default API key demo:

```text
helloworld
```

Untuk kegunaan lebih stabil, daftar API key sendiri di OCR.Space dan masukkan dalam sidebar.

## Tambah Ketepatan Kamus

Edit fail:

```text
data/kamus_jawi.csv
```

Format:

```csv
rumi,jawi,kategori
bahasa,بهاس,kata dasar
melayu,ملايو,kata dasar
```

Semakin banyak entri daripada Daftar Kata Rumi-Sebutan-Jawi dimasukkan, semakin tepat hasil ejaan.
