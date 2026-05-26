# Fitur Grafik Produk Terlaris

## Opsi Tampilan

Grafik produk terlaris sekarang memiliki 2 opsi tampilan:

### 1. Nama Produk (Default)
Menampilkan produk individual berdasarkan nama produk.

**Contoh:**
```
Coffee Latte: 125,000
Espresso: 98,500
Cappuccino: 87,300
Green Tea: 75,200
Black Tea: 68,900
```

**Kapan Menggunakan:**
- Ingin melihat produk spesifik yang paling laris
- Analisis detail per item
- Identifikasi best seller individual

### 2. Kategori Produk
Menampilkan penjualan berdasarkan kategori/grup produk.

**Contoh:**
```
Beverages: 450,000
Food: 320,000
Snacks: 180,000
Desserts: 125,000
```

**Kapan Menggunakan:**
- Ingin melihat kategori mana yang paling menguntungkan
- Analisis portfolio produk
- Strategi inventory per kategori
- Perencanaan promosi per kategori

## Cara Menggunakan

### Langkah 1: Upload Data
Upload file CSV yang memiliki:
- Kolom nama produk (Product, Item, Product Name)
- Kolom penjualan (Total Sales, Price, Amount)
- (Opsional) Kolom kategori (Category, Product Category, Type)

### Langkah 2: Pilih Kolom
Di sidebar:
- **Kolom Produk**: Pilih kolom nama produk
- **Kolom Penjualan**: Pilih kolom nilai penjualan

### Langkah 3: Pilih Tampilan
Di bagian "Produk Terlaris":
- Dropdown **"Tampilkan berdasarkan"**:
  - Pilih "Nama Produk" untuk melihat per item
  - Pilih "Kategori Produk" untuk melihat per kategori
- Jika pilih "Kategori Produk", pilih kolom kategori yang sesuai

### Langkah 4: Atur Jumlah
- Slider **"Jumlah Teratas"**: Pilih berapa banyak yang ingin ditampilkan (5-20)

## Auto-Detect Kategori

Aplikasi otomatis mendeteksi kolom kategori berdasarkan nama kolom yang mengandung:
- "categor" (category, categories, product_category)
- "type" (product_type, item_type)
- "class" (product_class, classification)

Jika tidak ada kolom kategori terdeteksi, hanya opsi "Nama Produk" yang tersedia.

## Contoh Use Case

### Use Case 1: Cafe Sales
**Data:**
- Product: Coffee Latte, Espresso, Sandwich, Cake
- Category: Beverages, Food, Desserts
- Total Sales: nilai penjualan

**Analisis per Produk:**
Lihat produk mana yang paling laris untuk:
- Stok inventory
- Menu highlight
- Promosi spesifik

**Analisis per Kategori:**
Lihat kategori mana yang paling menguntungkan untuk:
- Strategi menu
- Alokasi space
- Marketing campaign

### Use Case 2: E-commerce
**Data:**
- Product: Laptop Dell XPS, iPhone 13, Samsung TV
- Category: Electronics, Phones, Home Appliances
- Total Sales: revenue

**Analisis per Produk:**
- Best seller items
- Product bundling
- Cross-selling opportunities

**Analisis per Kategori:**
- Category performance
- Inventory planning
- Seasonal trends

## Tips

1. **Gunakan Nama Produk** jika:
   - Ingin detail spesifik
   - Produk tidak banyak (<50)
   - Analisis micro-level

2. **Gunakan Kategori** jika:
   - Ingin overview
   - Produk sangat banyak (>100)
   - Analisis macro-level
   - Perencanaan strategis

3. **Kombinasi Keduanya**:
   - Lihat kategori terbaik dulu
   - Lalu drill-down ke produk dalam kategori tersebut
   - Gunakan untuk strategi yang lebih komprehensif

## Troubleshooting

### Tidak Ada Opsi "Kategori Produk"
**Penyebab:** Tidak ada kolom kategori terdeteksi

**Solusi:**
1. Pastikan file CSV memiliki kolom kategori
2. Nama kolom harus mengandung: category, type, atau class
3. Atau tambahkan kolom kategori di Excel sebelum upload

### Grafik Kategori Tidak Akurat
**Penyebab:** Kolom kategori yang dipilih salah

**Solusi:**
1. Pilih kolom kategori yang benar dari dropdown
2. Pastikan kolom berisi kategori produk, bukan kategori lain
3. Cek data di tabel untuk memastikan

### Terlalu Banyak Kategori
**Solusi:**
1. Kurangi slider "Jumlah Teratas"
2. Atau grup kategori di Excel sebelum upload
3. Fokus pada kategori utama saja
