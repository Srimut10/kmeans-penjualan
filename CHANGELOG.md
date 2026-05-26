# Changelog - Sistem Clustering K-Means

## Version 2.0 (Latest)

### Fitur Baru

#### 1. Sistem Autentikasi
- Login/Logout dengan username & password
- Register user baru
- Ubah password di menu Pengaturan
- Session management dengan Streamlit
- Multi-user support
- Password hashing dengan SHA256
- User default: admin/admin123

**File Baru:**
- `auth.py` - Modul autentikasi
- `users.json` - Database user (auto-generated)

#### 2. History Analisis
- Simpan hasil analisis ke history
- Lihat semua analisis yang pernah dilakukan
- Detail lengkap setiap analisis:
  - Nama file
  - Tanggal & waktu
  - Jumlah cluster
  - Silhouette score
  - Total data & sales
  - Fitur yang digunakan
- Hapus history individual
- Hapus semua history
- History terpisah per user
- Export hasil clustering dengan timestamp

**File Baru:**
- `history_manager.py` - Modul manajemen history
- `history/` - Folder untuk menyimpan history per user

#### 3. Grafik Penjualan per Bulan
- Visualisasi time series penjualan bulanan
- Auto-detect kolom tanggal
- Support berbagai format tanggal
- Line chart dengan marker
- Area fill untuk trend
- Label nilai di setiap titik
- Analisis seasonality

**Fungsi Baru:**
- `plot_monthly_sales()` - Generate grafik penjualan per bulan

### Perubahan UI

#### Menu Navigasi
- Sidebar menu dengan 3 pilihan:
  - Analisis Data (default)
  - History
  - Pengaturan
- Header dengan info user dan tombol Logout
- Halaman login dengan tab Login & Register

#### Halaman Baru
- Login Page (tab Login & Register)
- History Page (lihat & kelola history)
- Settings Page (ubah password)

### Perubahan Struktur

#### Modul Sistem
- Total modul: 8 → 11 modul
- Modul baru:
  1. Modul Autentikasi
  2. Modul Visualisasi Penjualan per Bulan
  3. Modul History Analisis

#### Use Case
- Total use case: 8 → 12 use case utama
- Use case baru:
  - UC-00: Login/Logout
  - UC-05: Visualisasi Penjualan per Bulan
  - UC-09: Simpan ke History
  - UC-10: Lihat History

### Dokumentasi

#### File Diupdate
- `README.md` - Tambah fitur baru
- `CARA_MENJALANKAN.md` - Tambah panduan login
- `FITUR_BARU.md` - Tambah 3 fitur baru
- `MODUL_SISTEM.md` - Update 11 modul
- `USE_CASE_DETAIL.md` - Update use case
- `.gitignore` - Tambah users.json & history/

#### File Baru
- `CHANGELOG.md` - Dokumentasi perubahan

### Keamanan

- Password di-hash dengan SHA256 (tidak plain text)
- Session management untuk prevent unauthorized access
- History terpisah per user
- File hasil clustering tersimpan dengan username
- users.json dan history/ di-ignore dari git

### Bug Fixes

- Fix error index mismatch di interpretasi cluster
- Fix grafik produk terlaris menampilkan "ERROR"
- Fix visualisasi 2D dengan jitter untuk overlap

---

## Version 1.0

### Fitur Awal

1. Upload & Import Data
   - Auto-detect delimiter
   - Auto-detect encoding
   - Auto-convert kolom numerik

2. Pembersihan Data
   - Hapus duplikat
   - Hapus data unknown

3. Statistik Penjualan
   - Total data, penghasilan, rata-rata

4. Visualisasi Produk Terlaris
   - Bar chart
   - Per produk atau kategori

5. Clustering K-Means
   - Pilih fitur numerik
   - Atur jumlah cluster
   - Silhouette score

6. Visualisasi Clustering
   - Scatter plot per fitur
   - Scatter plot 2D
   - Distribusi cluster

7. Analisis Cluster
   - Karakteristik per cluster
   - Top 5 produk per cluster
   - Interpretasi bisnis

8. Export & Download
   - Download hasil clustering (CSV)

---

## Migration Guide (v1.0 → v2.0)

### Untuk User

1. **Pertama kali menjalankan v2.0:**
   - Login dengan user default: admin/admin123
   - Atau register user baru

2. **Data lama:**
   - File di folder `uploads/` tetap ada
   - Tidak ada history untuk analisis lama
   - Mulai simpan analisis baru ke history

3. **Workflow baru:**
   ```
   Login → Analisis → Simpan ke History → Logout
   ```

### Untuk Developer

1. **Dependencies baru:**
   - Tidak ada library baru
   - Hanya menggunakan built-in: hashlib, json, os, datetime

2. **File baru yang perlu di-track:**
   - `auth.py`
   - `history_manager.py`
   - `CHANGELOG.md`

3. **File yang di-ignore:**
   - `users.json` (sensitive)
   - `history/*.json` (sensitive)

4. **Breaking changes:**
   - Aplikasi sekarang memerlukan login
   - Tidak bisa langsung akses analisis tanpa login

---

## Roadmap

### Version 2.1 (Planned)
- Export history ke PDF
- Grafik perbandingan antar analisis
- Email notification untuk analisis selesai
- Role-based access (admin, user, viewer)

### Version 2.2 (Planned)
- Database support (SQLite/PostgreSQL)
- API endpoint untuk integrasi
- Scheduled analysis (cron job)
- Advanced clustering (DBSCAN, Hierarchical)

### Version 3.0 (Future)
- Real-time data streaming
- Machine learning model comparison
- Automated report generation
- Dashboard analytics

---

**Last Updated:** 2024
**Current Version:** 2.0
