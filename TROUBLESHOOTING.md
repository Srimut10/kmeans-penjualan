# Troubleshooting Guide

## Problem: "Tidak ada kolom numerik terdeteksi"

### Penyebab
File CSV Anda memiliki kolom numerik, tapi terbaca sebagai text/string karena:
- Ada karakter non-numerik (spasi, koma, simbol mata uang)
- Format angka yang tidak standar
- Delimiter yang salah

### Solusi

**Langkah 1: Cek Info Kolom**
1. Setelah upload file, buka expander **"Info Kolom Dataset"**
2. Lihat tabel yang menampilkan:
   - Nama kolom
   - Tipe data (object = text, int64/float64 = numerik)
   - Contoh data
   - Jumlah null

**Langkah 2: Konversi Otomatis**
1. Di bagian bawah "Info Kolom Dataset", lihat tabel "Kolom yang bisa dikonversi ke numerik"
2. Jika ada kolom yang muncul di sini, klik tombol **"Konversi Kolom ke Numerik"**
3. Aplikasi akan otomatis mengkonversi kolom tersebut
4. Halaman akan refresh dan kolom numerik akan muncul

**Langkah 3: Manual Fix (jika auto-convert gagal)**
Jika konversi otomatis tidak berhasil, bersihkan file CSV Anda:
1. Buka file di Excel/LibreOffice
2. Hapus karakter non-numerik dari kolom angka (Rp, $, koma, dll)
3. Pastikan format kolom adalah "Number" bukan "Text"
4. Save dan upload ulang

## Problem: Grafik menampilkan Transaction ID bukan nama produk

### Penyebab
Anda memilih kolom Transaction ID untuk "Kolom Produk" di sidebar.

### Solusi
1. Di sidebar, bagian **"Kolom Produk"**
2. Pilih kolom yang berisi nama produk, seperti:
   - Product Name
   - Product
   - Item
   - Item Name
3. JANGAN pilih:
   - Transaction ID
   - Order ID
   - Customer ID

### Tips
Lihat info box di sidebar yang menunjukkan contoh kolom yang benar:
```
Kolom Produk:
- Pilih: Product Name, Item, Product
- Jangan: Transaction ID, Order ID

Kolom Penjualan:
- Pilih: Total Sales, Price, Amount
- Jangan: Transaction ID, Customer ID
```

## Problem: "Kolom 'Transaction ID' tidak memiliki data numerik yang valid"

### Penyebab
Anda memilih kolom ID untuk analisis penjualan. Kolom ID biasanya berisi text/string, bukan angka penjualan.

### Solusi
1. Pilih kolom yang berisi nilai penjualan/harga/quantity
2. Contoh kolom yang BENAR:
   - Total Sales
   - Price
   - Amount
   - Quantity
   - Revenue
3. Contoh kolom yang SALAH:
   - Transaction ID
   - Order ID
   - Customer ID
   - Product Name

## Problem: "Pilih minimal 1 fitur untuk clustering"

### Penyebab
Tidak ada kolom numerik yang tersedia untuk clustering.

### Solusi
1. Buka "Info Kolom Dataset"
2. Konversi kolom ke numerik (lihat solusi di atas)
3. Atau pastikan file CSV Anda memiliki minimal 1 kolom numerik

## Problem: Grafik tidak muncul atau kosong

### Penyebab
- Data tidak valid
- Kolom yang dipilih bukan numerik
- Semua data dihapus saat pembersihan

### Solusi
1. Cek "Detail Data yang Dihapus" untuk melihat berapa data yang hilang
2. Jika terlalu banyak data dihapus, cek kualitas data Anda
3. Pastikan kolom yang dipilih adalah kolom numerik
4. Gunakan "Info Kolom Dataset" untuk verifikasi

## Problem: Delimiter tidak terdeteksi dengan benar

### Gejala
- Semua data muncul dalam 1 kolom panjang
- Nama kolom berisi semua header digabung

### Solusi
1. Cek delimiter file CSV Anda (buka dengan text editor)
2. Aplikasi support: `,` `;` `\t` `|`
3. Jika menggunakan delimiter lain, ubah di Excel:
   - Save As → CSV (Comma delimited)
4. Upload ulang file

## Problem: Encoding error atau karakter aneh

### Gejala
- Karakter muncul sebagai �, ?, atau simbol aneh
- Error saat load file

### Solusi
1. Ubah **Encoding** di sidebar
2. Coba urutan ini:
   - utf-8 (default)
   - latin-1 (untuk file Windows)
   - cp1252 (untuk file Windows lama)
   - iso-8859-1 (untuk file Eropa)

## Tips Umum

1. **Gunakan "Info Kolom Dataset"** - Ini adalah tool debugging terbaik
2. **Bersihkan data di Excel dulu** - Lebih mudah daripada troubleshooting
3. **Pastikan format CSV standar** - Delimiter `,` dan encoding UTF-8
4. **Jangan pilih kolom ID** - Pilih kolom yang berisi angka penjualan
5. **Cek contoh data** - Lihat apakah data masuk akal

## Masih Bermasalah?

Jika masih ada masalah:
1. Cek file `sample_data.csv` sebagai referensi format yang benar
2. Bandingkan struktur file Anda dengan sample data
3. Pastikan file CSV Anda memiliki:
   - Header (baris pertama berisi nama kolom)
   - Minimal 1 kolom numerik
   - Data yang konsisten (tidak ada baris dengan jumlah kolom berbeda)


---

## Masalah: Kolom Tanggal Tidak Terdeteksi

### Gejala
- Grafik "Penjualan per Bulan" tidak muncul
- Pesan: "Tidak ada kolom tanggal terdeteksi"
- Padahal file CSV memiliki kolom tanggal

### Penyebab
Nama kolom tanggal tidak sesuai dengan keyword deteksi sistem.

### Solusi

**Kolom tanggal yang didukung:**
- Date, Tanggal, Waktu, Time
- Created, Order Date, Transaction Date
- Waktu Pesanan Dibuat, Waktu Transaksi
- Timestamp, DateTime
- Bulan, Tahun, Month, Year
- Tgl, Dibuat, Pesanan

**Jika kolom Anda berbeda:**
1. Klik expander "Debug: Lihat Semua Kolom"
2. Lihat nama kolom tanggal Anda
3. Rename kolom di Excel sebelum upload
4. Atau hubungi developer untuk tambah keyword

**Contoh:**
- "Order_Date" → Terdeteksi ✓
- "Waktu Pesanan Dibuat" → Terdeteksi ✓
- "Tgl_Order" → Terdeteksi ✓
- "Col_A" → Tidak terdeteksi ✗

---

## Masalah: Dataset Tokopedia Tidak Muncul Analisis

### Gejala
- Upload file berhasil
- Tapi tidak ada grafik clustering
- Pesan: "Tidak ada kolom numerik untuk clustering"

### Penyebab
Kolom numerik tidak terdeteksi karena:
1. Kolom berisi text (contoh: "1.000" dengan titik)
2. Kolom berisi karakter khusus (contoh: "Rp 50.000")
3. Delimiter salah (data jadi 1 kolom)

### Solusi

**Langkah 1: Cek Info Kolom**
1. Buka expander "Info Kolom Dataset"
2. Lihat tipe data setiap kolom
3. Cek kolom mana yang seharusnya numerik

**Langkah 2: Konversi Otomatis**
1. Di expander "Info Kolom Dataset"
2. Lihat tabel "Kolom yang bisa dikonversi ke numerik"
3. Klik tombol "Konversi Kolom ke Numerik"
4. Refresh halaman

**Langkah 3: Jika Masih Gagal**
1. Buka file CSV di Excel
2. Hapus format currency (Rp, $, dll)
3. Ubah format kolom ke "Number"
4. Hapus titik pemisah ribuan
5. Save dan upload ulang

**Contoh Data yang Bermasalah:**
```
Total Pembayaran: "Rp 50.000" → Tidak bisa dikonversi
Total Pembayaran: "50.000" → Tidak bisa dikonversi (titik)
Total Pembayaran: "50000" → Bisa dikonversi ✓
```

**Tips:**
- Gunakan koma (,) sebagai delimiter
- Angka tanpa format currency
- Tanpa titik/koma pemisah ribuan
- Format: 50000 bukan 50.000 atau Rp 50.000

---

## Masalah: Grafik Per Bulan Kosong

### Gejala
- Kolom tanggal terdeteksi
- Tapi grafik tidak muncul atau kosong

### Penyebab
1. Format tanggal tidak valid
2. Kolom tanggal berisi text bukan tanggal
3. Semua data tanggal adalah NaN

### Solusi

**Cek Format Tanggal:**
Format yang didukung:
- YYYY-MM-DD (2024-01-15)
- DD/MM/YYYY (15/01/2024)
- MM/DD/YYYY (01/15/2024)
- YYYY-MM-DD HH:MM:SS (2024-01-15 10:30:00)

**Jika Format Berbeda:**
1. Buka file di Excel
2. Format kolom tanggal ke format standar
3. Save dan upload ulang

**Contoh:**
- "2024-04-01 00:15" → Valid ✓
- "01 April 2024" → Valid ✓
- "April 2024" → Tidak valid ✗
- "01/04/24" → Valid ✓

---

## Masalah: Analisis Tidak Tersimpan ke History

### Gejala
- Analisis selesai
- Tapi tidak ada di menu History

### Penyebab
1. Belum login
2. Error saat menyimpan
3. Folder history tidak ada

### Solusi

**Cek Login:**
- Pastikan sudah login
- Cek nama user di kanan atas

**Cek Folder:**
1. Pastikan folder `history/` ada di project
2. Jika tidak ada, buat manual

**Cek Pesan:**
- Setelah clustering selesai, cek pesan:
  - "✓ Analisis otomatis tersimpan ke history" → Berhasil
  - "✓ Analisis ini sudah tersimpan di history" → Sudah ada
  - Jika tidak ada pesan → Ada error

**Jika Masih Gagal:**
1. Logout
2. Login ulang
3. Lakukan analisis ulang

---

## Tips Umum

### Upload File CSV
- Gunakan delimiter standar (koma atau titik koma)
- Encoding UTF-8
- Tanpa karakter khusus di nama kolom
- Header di baris pertama

### Kolom Numerik
- Tanpa format currency
- Tanpa pemisah ribuan
- Gunakan titik (.) untuk desimal
- Contoh: 50000.50 bukan 50.000,50

### Kolom Tanggal
- Format standar (YYYY-MM-DD)
- Konsisten di semua baris
- Tanpa text tambahan

### Performa
- File < 10MB untuk performa optimal
- Jika file besar, filter data di Excel dulu
- Hapus kolom yang tidak perlu
