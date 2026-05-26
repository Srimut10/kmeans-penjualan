# Sistem Analisis Clustering K-Means untuk Data Penjualan

Aplikasi web berbasis Streamlit untuk analisis clustering data penjualan menggunakan algoritma K-Means dengan fitur login, history, dan visualisasi lengkap.

## Fitur Utama

### 1. Autentikasi User
- Login/Logout dengan username & password
- Register user baru
- Ubah password
- Session management
- Multi-user support

### 2. Upload & Import Data
- Upload file CSV dengan drag & drop
- Auto-detect delimiter (`,`, `;`, `\t`, `|`)
- Auto-detect encoding (utf-8, latin-1, iso-8859-1, cp1252, utf-16)
- Auto-convert kolom numerik
- File otomatis tersimpan di folder uploads/

### 3. Pembersihan Data
- Hapus data duplikat
- Hapus data 'unknown' (unknown, n/a, na, -, kosong)
- Detail data yang dihapus
- Missing values (NaN) tetap dipertahankan

### 4. Statistik Penjualan
- Total data penjualan
- Total penghasilan
- Rata-rata penjualan

### 5. Visualisasi Produk Terlaris
- Grafik bar chart produk terlaris
- Pilihan tampilan: per produk atau per kategori
- Slider jumlah produk (5-20)
- Auto-detect kolom kategori

### 6. Visualisasi Penjualan per Bulan (BARU!)
- Grafik line chart penjualan bulanan
- Auto-detect kolom tanggal
- Time series analysis
- Trend penjualan per periode

### 7. Clustering K-Means
- Pilih fitur numerik untuk clustering
- Atur jumlah cluster (2-10)
- Standardisasi data otomatis
- Hitung Silhouette Score

### 8. Visualisasi Clustering
- Scatter plot per fitur
- Scatter plot 2D dengan centroid
- Distribusi data per cluster
- Warna berbeda per cluster
- Jitter untuk menghindari overlap

### 9. Analisis Cluster
- Pola dan karakteristik per cluster
- Top 5 produk terlaris per cluster
- Interpretasi bisnis
- Cluster terbaik (total sales)
- Cluster rata-rata tertinggi

### 10. History Analisis (BARU!)
- Simpan hasil analisis
- Lihat history lengkap
- Detail setiap analisis
- Hapus history individual atau semua
- History terpisah per user

### 11. Export & Download
- Download hasil clustering (CSV)
- Export dengan kolom cluster
- Auto-save dengan timestamp

## Teknologi

- **Python 3.8+**
- **Streamlit** - Web framework
- **Pandas** - Data manipulation
- **NumPy** - Numerical computing
- **Scikit-learn** - Machine learning (K-Means)
- **Matplotlib** - Data visualization
- **Hashlib** - Password hashing

## Instalasi

1. Clone atau download repository ini
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Jalankan aplikasi:
   ```bash
   streamlit run app.py
   ```
   Atau double-click `jalankan.bat` (Windows)

4. Login dengan user default:
   - Username: `admin`
   - Password: `admin123`

## Struktur Project

```
project/
├── app.py                  # Aplikasi utama
├── auth.py                 # Modul autentikasi
├── history_manager.py      # Modul history
├── requirements.txt        # Dependencies
├── jalankan.bat           # Batch file Windows
├── sample_data.csv        # Contoh data
├── users.json             # Database user
├── uploads/               # Folder upload
├── history/               # Folder history
└── dokumentasi/
    ├── CARA_MENJALANKAN.md
    ├── FITUR_BARU.md
    ├── FITUR_GRAFIK.md
    ├── MODUL_SISTEM.md
    ├── USE_CASE_DETAIL.md
    └── TROUBLESHOOTING.md
```

## Dokumentasi

- [Cara Menjalankan](CARA_MENJALANKAN.md) - Panduan instalasi dan menjalankan
- [Fitur Baru](FITUR_BARU.md) - Penjelasan fitur login, history, grafik bulan
- [Fitur Grafik](FITUR_GRAFIK.md) - Panduan visualisasi produk
- [Modul Sistem](MODUL_SISTEM.md) - Arsitektur 11 modul sistem
- [Use Case Detail](USE_CASE_DETAIL.md) - Use case diagram lengkap
- [Troubleshooting](TROUBLESHOOTING.md) - Solusi masalah umum

## Use Case

Aplikasi ini cocok untuk:
- Analisis segmentasi pelanggan
- Identifikasi pola pembelian
- Strategi marketing berbasis cluster
- Analisis produk terlaris
- Perencanaan inventory
- Analisis trend penjualan bulanan

## Contoh Dataset

File `sample_data.csv` berisi contoh data penjualan dengan kolom:
- Product: Nama produk
- Quantity: Jumlah terjual
- Price: Harga satuan
- Total_Sales: Total penjualan
- Category: Kategori produk

## Lisensi

MIT License

## Kontributor

Dikembangkan untuk tugas Data Mining - Clustering K-Means

---

**Versi:** 2.0 (dengan Login, History, dan Grafik Bulan)
**Update:** 2024
