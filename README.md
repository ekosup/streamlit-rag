# Streamlit RAG - Indonesia Tax Court Verdict

Aplikasi RAG (Retrieval-Augmented Generation) berbasis Streamlit untuk mencari dan menganalisis putusan Pengadilan Pajak Indonesia menggunakan LLM.

## Fitur

- Pencarian semantik pada putusan Pengadilan Pajak
- Antarmuka chat untuk pertanyaan dalam bahasa Indonesia
- Browser data untuk eksplorasi putusan
- Statistik dan analisis data
- Integrasi dengan OpenRouter untuk berbagai model LLM

## Persyaratan Sistem

- Python 3.12+
- uv (rekomendasi) atau pip untuk manajemen paket

## Instalasi dan Setup

### 0. Install Dependencies

Gunakan `uv` (rekomendasi) atau `pip` untuk menginstall paket yang diperlukan:

```bash
# Dengan uv (rekomendasi)
uv sync

# Atau dengan pip
pip install -r requirements.txt
```

### 1. Persiapkan Data

1. Unduh dataset dari [Kaggle: Indonesia Tax Court Verdict](https://www.kaggle.com/datasets/christianwbsn/indonesia-tax-court-verdict)
2. Ekstrak file CSV dari dataset
3. Salin file CSV ke folder `data/` di root proyek:
   - `indonesia_tax_court_verdict_raw_html.csv`
   - `indonesia_tax_court_verdict.csv`

### 2. Bangun Index Vektor

Jalankan script untuk membangun index vektor dari data putusan:

```bash
# Dengan uv
uv run python scripts/build_index.py

# Atau dengan python langsung (jika dependencies sudah terinstall)
python scripts/build_index.py
```

Proses ini akan membuat embedding untuk semua putusan dan menyimpannya dalam database vektor.

### 3. Jalankan Aplikasi

```bash
# Dengan uv
uv run streamlit run app.py

# Atau dengan streamlit langsung
streamlit run app.py
```

Aplikasi akan berjalan di `http://localhost:8501`

### 4. Konfigurasi API dan Model

1. Di sidebar aplikasi, masukkan API key OpenRouter Anda
2. Pilih model LLM yang diinginkan (default: google/gemini-2.0-flash-001)
3. Mulai bertanya tentang putusan Pengadilan Pajak

## Struktur Proyek

```
streamlit-rag/
├── app.py                 # Aplikasi utama Streamlit
├── pyproject.toml         # Konfigurasi proyek dan dependencies
├── components/            # Komponen UI
│   ├── chat.py           # Interface chat
│   ├── data_browser.py   # Browser data
│   ├── sidebar.py        # Sidebar konfigurasi
│   ├── stats.py          # Halaman statistik
│   └── styles.py         # Styling CSS
├── data/                 # Folder data (tambahkan file CSV di sini)
├── model/                # Model embedding (diunduh otomatis)
├── scripts/              # Script utility
│   └── build_index.py    # Script pembuatan index
└── services/             # Layanan backend
    ├── data.py           # Pemrosesan data
    ├── llm.py            # Integrasi LLM
    └── vector_store.py   # Penyimpanan vektor
```

## Penggunaan

1. **Pencarian**: Gunakan tab "Pencarian" untuk bertanya tentang putusan pajak
2. **Data**: Jelajahi putusan di tab "Data" dengan filter dan pencarian teks
3. **Statistik**: Lihat analisis data di tab "Statistik"

## Catatan

- Pastikan API key OpenRouter valid dan memiliki kuota yang cukup
- Proses indexing mungkin memakan waktu tergantung ukuran data
- Model embedding diunduh otomatis pada pertama kali menjalankan build_index.py

## Lisensi

[MIT License]