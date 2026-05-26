# Quick Start Guide

## 🚀 Mulai dalam 3 Langkah

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Jalankan Aplikasi
```bash
streamlit run app.py
```
Atau double-click `jalankan.bat` (Windows)

### 3. Login
- Username: `admin`
- Password: `admin123`

---

## 📊 Workflow Analisis

```
1. Login
   ↓
2. Upload CSV
   ↓
3. Pilih Kolom (Produk & Penjualan)
   ↓
4. Pilih Fitur untuk Clustering
   ↓
5. Atur Jumlah Cluster
   ↓
6. Lihat Hasil:
   - Statistik
   - Grafik Produk Terlaris
   - Grafik Penjualan per Bulan
   - Clustering
   - Interpretasi
   ↓
7. Simpan ke History
   ↓
8. Download Hasil (CSV)
   ↓
9. Logout
```

---

## 🎯 Fitur Utama

### Login & User Management
- Login/Logout
- Register user baru
- Ubah password

### Analisis Data
- Upload CSV (auto-detect format)
- Pembersihan data otomatis
- Statistik penjualan
- Grafik produk terlaris
- Grafik penjualan per bulan
- Clustering K-Means
- Visualisasi lengkap
- Interpretasi bisnis

### History
- Simpan hasil analisis
- Lihat history lengkap
- Hapus history

---

## 📁 Format Data

### Kolom yang Diperlukan:
1. **Kolom Produk** - Nama produk (Coffee, Tea, dll)
2. **Kolom Penjualan** - Nilai numerik (harga, quantity, total)
3. **Kolom Tanggal** (opsional) - Untuk grafik per bulan

### Contoh:
```csv
Product,Quantity,Price,Total_Sales,Date
Coffee,100,25000,2500000,2024-01-15
Tea,80,15000,1200000,2024-01-16
Sandwich,50,35000,1750000,2024-01-17
```

---

## ⚡ Tips

1. **Gunakan nama kolom yang jelas**
   - Produk: Product, Item, Menu
   - Penjualan: Sales, Total, Amount
   - Tanggal: Date, Time, Created

2. **Pilih fitur numerik yang relevan**
   - Quantity, Price, Total_Sales
   - Minimal 1 fitur, maksimal semua

3. **Atur jumlah cluster yang tepat**
   - Mulai dari 3-5 cluster
   - Lihat Silhouette Score (>0.5 = bagus)

4. **Simpan analisis penting**
   - Klik "Simpan ke History"
   - Bisa dilihat kapan saja di menu History

5. **Grafik per bulan**
   - Pastikan ada kolom tanggal
   - Format tanggal harus valid

---

## 🔧 Troubleshooting

### Tidak bisa login?
- Gunakan: admin / admin123
- Atau register user baru

### File tidak bisa diupload?
- Pastikan format CSV
- Cek delimiter (koma, titik koma, tab)

### Grafik tidak muncul?
- Pastikan kolom yang dipilih benar
- Kolom produk = nama produk (bukan ID)
- Kolom penjualan = angka (bukan text)

### Clustering error?
- Pilih minimal 1 fitur numerik
- Pastikan ada data setelah pembersihan

---

## 📚 Dokumentasi Lengkap

- [README.md](README.md) - Overview lengkap
- [CARA_MENJALANKAN.md](CARA_MENJALANKAN.md) - Panduan detail
- [FITUR_BARU.md](FITUR_BARU.md) - Fitur login, history, grafik bulan
- [MODUL_SISTEM.md](MODUL_SISTEM.md) - Arsitektur sistem
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Solusi masalah

---

## 💡 Use Case

**Cafe/Restaurant:**
- Analisis produk terlaris
- Trend penjualan per bulan
- Segmentasi menu

**E-commerce:**
- Clustering produk
- Analisis kategori
- Perencanaan inventory

**Retail:**
- Pola pembelian
- Strategi promosi
- Analisis seasonality

---

**Version:** 2.0
**Support:** Baca dokumentasi atau cek TROUBLESHOOTING.md
