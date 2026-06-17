import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import base64
import os
from datetime import datetime
from auth import AuthManager
from history_manager import HistoryManager

# Set page config harus di paling atas
st.set_page_config(
    page_title="Analisis Clustering Penjualan",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS Responsif untuk Mobile
st.markdown("""
<style>
/* Mobile responsif */
@media (max-width: 768px) {
    /* Perkecil padding utama */
    .main .block-container {
        padding: 1rem 0.5rem !important;
        max-width: 100% !important;
    }
    
    /* Metric card lebih kecil */
    [data-testid="metric-container"] {
        padding: 0.5rem !important;
    }
    
    /* Font lebih kecil di mobile */
    h1 { font-size: 1.5rem !important; }
    h2 { font-size: 1.3rem !important; }
    h3 { font-size: 1.1rem !important; }
    
    /* Tabel scroll horizontal */
    [data-testid="stDataFrame"] {
        overflow-x: auto !important;
    }
    
    /* Grafik full width */
    [data-testid="stImage"] img {
        width: 100% !important;
        height: auto !important;
    }
    
    /* Tombol full width */
    .stButton > button {
        width: 100% !important;
        margin: 0.25rem 0 !important;
    }
    
    /* Download button */
    .stDownloadButton > button {
        width: 100% !important;
    }
    
    /* Kolom jadi satu baris di mobile */
    [data-testid="column"] {
        min-width: 100% !important;
    }
    
    /* Sidebar lebih kecil */
    [data-testid="stSidebar"] {
        min-width: 80vw !important;
    }
    
    /* Form input full width */
    .stTextInput input, .stSelectbox select {
        width: 100% !important;
    }
    
    /* Radio button horizontal jadi vertikal */
    .stRadio > div {
        flex-direction: column !important;
    }
}

/* Tampilan umum - semua device */
[data-testid="metric-container"] {
    background: #f8f9fa;
    border: 1px solid #e9ecef;
    border-radius: 8px;
    padding: 1rem;
}

.stAlert {
    border-radius: 8px;
}

/* Header lebih rapi */
h1, h2, h3 {
    color: #1a1a2e;
}

/* Tabel responsif */
[data-testid="stDataFrame"] {
    border-radius: 8px;
    overflow: hidden;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'user_name' not in st.session_state:
    st.session_state.user_name = None

# Initialize managers
auth_manager = AuthManager()
history_manager = HistoryManager()

# Set matplotlib backend
plt.switch_backend('Agg')

def show_login_page():
    """Tampilkan halaman login"""
    st.title("Login - Sistem Analisis Clustering")
    
    st.subheader("Login ke Sistem")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            if username and password:
                success, user_name = auth_manager.login(username, password)
                if success:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.user_name = user_name
                    st.success(f"Selamat datang, {user_name}!")
                    st.rerun()
                else:
                    st.error("Username atau password salah!")
            else:
                st.warning("Masukkan username dan password!")

def show_history_page():
    """Tampilkan halaman history"""
    st.title("History Analisis")

    history = history_manager.get_history(st.session_state.username)

    if len(history) == 0:
        st.info("Belum ada history analisis")
        return

    # Tombol hapus semua
    col_title, col_hapus = st.columns([4, 1])
    with col_title:
        st.write(f"Total analisis tersimpan: **{len(history)}**")
    with col_hapus:
        if st.button("Hapus Semua History", type="secondary"):
            history_manager.clear_history(st.session_state.username)
            st.success("Semua history dihapus")
            st.rerun()

    st.markdown("---")

    df_history = pd.DataFrame(history)
    df_history['timestamp'] = pd.to_datetime(df_history['timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')

    # Tampilkan setiap history sebagai card
    for _, row in df_history.iterrows():
        with st.expander(f"#{row['id']} | {row['filename']} | {row['timestamp']} | Cluster: {row['n_clusters']} | Skor: {row['silhouette_score']:.3f}"):

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Data", f"{row['total_data']:,}")
            with col2:
                st.metric("Jumlah Cluster", row['n_clusters'])
            with col3:
                st.metric("Silhouette Score", f"{row['silhouette_score']:.3f}")

            # Load file hasil
            result_path = os.path.join('uploads', row['result_file'])

            if os.path.exists(result_path):
                df_result = pd.read_csv(result_path)

                # Tampilkan tabel hasil
                st.subheader("Data Hasil Segmentasi")
                st.dataframe(df_result, use_container_width=True, hide_index=True)

                # Grafik segmentasi jika ada kolom yang dibutuhkan
                product_col_h = row.get('product_col', None)
                sales_col_h = row.get('sales_col', None)

                if 'Frekuensi' in df_result.columns and 'Total_Belanja' in df_result.columns and 'Segmen' in df_result.columns:
                    st.subheader("Grafik Segmentasi")
                    seg_colors = {
                        'Sultan / Loyal': '#e74c3c',
                        'Hemat': '#2ecc71',
                        'Baru / Pasif': '#3498db'
                    }
                    fig_h, ax_h = plt.subplots(figsize=(10, 6))
                    customer_col_h = product_col_h if product_col_h and product_col_h in df_result.columns else df_result.columns[0]

                    for seg, color in seg_colors.items():
                        subset = df_result[df_result['Segmen'] == seg]
                        if len(subset) == 0:
                            continue
                        ax_h.scatter(subset['Frekuensi'], subset['Total_Belanja'],
                                     label=f"{seg} ({len(subset)})",
                                     color=color, alpha=1.0, s=200,
                                     edgecolors='black', linewidth=1.5, marker='o')
                        ax_h.scatter(subset['Frekuensi'].mean(), subset['Total_Belanja'].mean(),
                                     color=color, s=600, edgecolors='black', linewidth=2.5,
                                     zorder=10, marker='o')

                    ax_h.set_xlabel('Frekuensi Belanja', fontsize=12, fontweight='bold')
                    ax_h.set_ylabel('Total Belanja', fontsize=12, fontweight='bold')
                    ax_h.set_title('Segmentasi Pelanggan', fontsize=13, fontweight='bold')
                    ax_h.legend(fontsize=10)
                    ax_h.grid(True, alpha=0.3, linestyle='--')
                    ax_h.set_facecolor('#f8f9fa')
                    plt.tight_layout()
                    st.pyplot(fig_h)
                    plt.close(fig_h)

                # Download ulang
                st.markdown("---")
                col_dl, col_del = st.columns([3, 1])
                with col_dl:
                    with open(result_path, 'rb') as f:
                        st.download_button(
                            label="Download Hasil CSV",
                            data=f,
                            file_name=row['result_file'],
                            mime='text/csv',
                            key=f"dl_{row['id']}"
                        )
                with col_del:
                    if st.button("Hapus History Ini", key=f"del_{row['id']}", type="secondary"):
                        history_manager.delete_history(st.session_state.username, row['id'])
                        st.success("History dihapus")
                        st.rerun()
            else:
                st.warning("File hasil tidak ditemukan")
                if st.button("Hapus History Ini", key=f"del_missing_{row['id']}", type="secondary"):
                    history_manager.delete_history(st.session_state.username, row['id'])
                    st.rerun()


def plot_monthly_sales(df, date_col, sales_col, selected_year=None):
    """Membuat grafik penjualan per bulan - jumlah item terjual"""
    try:
        df_plot = df.copy()
        
        # Konversi tanggal - support format Indonesia (01 Januari 2026)
        bulan_indo = {
            'januari': 'January', 'februari': 'February', 'maret': 'March',
            'april': 'April', 'mei': 'May', 'juni': 'June',
            'juli': 'July', 'agustus': 'August', 'september': 'September',
            'oktober': 'October', 'november': 'November', 'desember': 'December'
        }
        def parse_date(val):
            s = str(val).strip().lower()
            for indo, eng in bulan_indo.items():
                s = s.replace(indo, eng)
            try:
                return pd.to_datetime(s, dayfirst=True)
            except:
                return pd.NaT

        # Coba konversi biasa dulu, fallback ke format Indonesia
        converted = pd.to_datetime(df_plot[date_col], errors='coerce')
        if converted.isna().sum() > len(df_plot) * 0.5:
            converted = df_plot[date_col].apply(parse_date)
        df_plot[date_col] = converted
        df_plot = df_plot.dropna(subset=[date_col])
        
        if len(df_plot) == 0:
            st.error("Tidak ada data tanggal yang valid!")
            return None
        
        # Filter berdasarkan tahun jika dipilih
        if selected_year and selected_year != "Semua Tahun":
            df_plot = df_plot[df_plot[date_col].dt.year == int(selected_year)]
            
            if len(df_plot) == 0:
                st.warning(f"Tidak ada data untuk tahun {selected_year}")
                return None
        
        # Extract bulan dan tahun
        df_plot['YearMonth'] = df_plot[date_col].dt.to_period('M')
        # Nama bulan Bahasa Indonesia
        bulan_map = {
            'January': 'Januari', 'February': 'Februari', 'March': 'Maret',
            'April': 'April', 'May': 'Mei', 'June': 'Juni',
            'July': 'Juli', 'August': 'Agustus', 'September': 'September',
            'October': 'Oktober', 'November': 'November', 'December': 'Desember'
        }
        df_plot['MonthName'] = df_plot[date_col].dt.strftime('%B %Y').apply(
            lambda x: bulan_map.get(x.split()[0], x.split()[0]) + ' ' + x.split()[1]
        )
        
        # Group by bulan - HITUNG JUMLAH TRANSAKSI (bukan total harga)
        monthly_count = df_plot.groupby(['YearMonth', 'MonthName']).size().reset_index(name='Jumlah_Terjual')
        monthly_count = monthly_count.sort_values('YearMonth')
        
        if len(monthly_count) == 0:
            st.error("Tidak ada data penjualan per bulan!")
            return None
        
        # Plot dengan bar chart
        fig, ax = plt.subplots(figsize=(14, 7))
        
        x_pos = range(len(monthly_count))
        colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(monthly_count)))
        
        bars = ax.bar(x_pos, monthly_count['Jumlah_Terjual'].values, 
                      color=colors, edgecolor='black', linewidth=1.5, alpha=0.8)
        
        # Tambahkan nilai di atas setiap bar
        for i, (bar, val) in enumerate(zip(bars, monthly_count['Jumlah_Terjual'].values)):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(val)} produk',
                    ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        ax.set_xticks(x_pos)
        ax.set_xticklabels(monthly_count['MonthName'].values, rotation=45, ha='right', fontsize=10)
        
        # Title berdasarkan filter
        if selected_year and selected_year != "Semua Tahun":
            title = f'Jumlah Produk Terjual per Bulan - Tahun {selected_year}'
        else:
            title = 'Jumlah Produk Terjual per Bulan - Semua Periode'
        
        ax.set_title(title, fontsize=15, fontweight='bold', pad=15)
        ax.set_xlabel('Bulan', fontsize=12, fontweight='bold')
        ax.set_ylabel('Jumlah Produk Terjual', fontsize=12, fontweight='bold')
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        ax.set_facecolor('#f8f9fa')
        
        plt.tight_layout()
        return fig
    except Exception as e:
        st.error(f"Error creating monthly chart: {e}")
        return None

def load_data(file):
    """Load CSV file dengan auto-detect delimiter, encoding, dan header row"""
    try:
        # Reset file pointer
        file.seek(0)
        
        # Coba berbagai encoding
        encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252', 'utf-16']
        df = None
        detected_encoding = 'utf-8'
        
        for encoding in encodings:
            try:
                file.seek(0)
                # Baca semua baris untuk detect header
                raw_lines = []
                for line in file:
                    try:
                        raw_lines.append(line.decode(encoding))
                    except:
                        break
                
                if not raw_lines:
                    continue
                
                file.seek(0)
                first_line = raw_lines[0]
                
                # Detect delimiter dari baris pertama
                possible_delimiters = [',', ';', '\t', '|']
                delimiter = ','
                max_cols = 0
                for delim in possible_delimiters:
                    cols = len(first_line.split(delim))
                    if cols > max_cols:
                        max_cols = cols
                        delimiter = delim
                
                # Cari baris header yang sebenarnya
                # Header yang valid = baris yang punya banyak kolom non-kosong
                header_row = 0
                max_non_empty = 0
                for i, line in enumerate(raw_lines[:20]):  # cek 20 baris pertama
                    cols = [c.strip().strip('"') for c in line.split(delimiter)]
                    non_empty = sum(1 for c in cols if c and c.lower() not in ['none', 'nan'])
                    if non_empty > max_non_empty:
                        max_non_empty = non_empty
                        header_row = i
                
                # Load CSV dengan header row yang terdeteksi
                file.seek(0)
                df = pd.read_csv(file, sep=delimiter, encoding=encoding, 
                                 header=header_row, on_bad_lines='skip')
                
                # Hapus baris yang semua nilainya NaN
                df = df.dropna(how='all')
                
                # Hapus kolom yang semua nilainya NaN
                df = df.dropna(axis=1, how='all')
                
                # Hapus baris yang isinya sama dengan nama kolom (header duplikat)
                header_vals = set(str(c).lower().strip() for c in df.columns)
                def is_header_row(row):
                    vals = set(str(v).lower().strip() for v in row.values if pd.notna(v))
                    overlap = len(vals & header_vals)
                    return overlap >= len(df.columns) * 0.5
                mask_header = df.apply(is_header_row, axis=1)
                df = df[~mask_header]
                
                # Hapus kolom Unnamed
                df = df.loc[:, ~df.columns.astype(str).str.startswith('Unnamed')]
                
                # Reset index
                df = df.reset_index(drop=True)
                
                detected_encoding = encoding
                
                # Auto-convert kolom yang seharusnya numerik
                for col in df.columns:
                    if df[col].dtype == 'object':
                        converted = pd.to_numeric(df[col], errors='coerce')
                        if converted.notna().sum() > len(df) * 0.3:
                            df[col] = converted
                
                break
            except:
                continue
        
        if df is None:
            st.error("Gagal membaca file. Coba format CSV yang berbeda.")
            return None, None
        
        return df, delimiter
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None, None

def clean_data(df):
    """Membersihkan data duplikat dan data unknown"""
    initial_rows = len(df)
    
    # Hitung duplikat
    duplicates = df.duplicated().sum()
    
    # Hapus duplikat
    df_cleaned = df.drop_duplicates()
    
    # Hapus baris yang SEMUA kolomnya kosong/None/NaN
    df_cleaned = df_cleaned.dropna(how='all')
    
    # Hapus baris yang mayoritas kolomnya kosong (lebih dari 50% kolom kosong)
    threshold = len(df_cleaned.columns) * 0.5
    df_cleaned = df_cleaned.dropna(thresh=int(threshold))
    
    # Hitung data unknown (case-insensitive)
    unknown_count = 0
    unknown_per_column = {}
    
    for col in df_cleaned.columns:
        if df_cleaned[col].dtype == 'object':
            unknown_mask = df_cleaned[col].astype(str).str.lower().str.strip().isin([
                'unknown', 'unkown', 'unknow', 'n/a', 'na', '-', '', 'none', 'null'
            ])
            col_unknown = unknown_mask.sum()
            if col_unknown > 0:
                unknown_per_column[col] = col_unknown
                unknown_count += col_unknown
    
    # Hapus baris yang mengandung "unknown"/"none" di kolom KUNCI (customer, nama barang)
    key_cols = [col for col in df_cleaned.columns 
                if any(k in col.lower() for k in ['customer', 'nama', 'barang', 'product'])]
    
    for col in key_cols:
        if df_cleaned[col].dtype == 'object':
            df_cleaned = df_cleaned[
                ~df_cleaned[col].astype(str).str.lower().str.strip().isin([
                    'unknown', 'unkown', 'unknow', 'n/a', 'na', '-', '', 'none', 'null'
                ])
            ]
    
    removed_rows = initial_rows - len(df_cleaned)
    
    return df_cleaned, removed_rows, duplicates, unknown_per_column, unknown_count

def calculate_statistics(df, sales_col):
    """Menghitung statistik penjualan"""
    total_data = len(df)
    try:
        # Konversi ke numerik, paksa error menjadi NaN
        sales_numeric = pd.to_numeric(df[sales_col], errors='coerce')
        total_sales = sales_numeric.sum()
        avg_sales = sales_numeric.mean()
        return total_data, total_sales, avg_sales
    except Exception as e:
        st.error(f"Error menghitung statistik: Kolom '{sales_col}' bukan kolom numerik!")
        return total_data, 0, 0

def plot_top_products(df, product_col, sales_col, top_n=10):
    """Membuat grafik produk terlaris - berdasarkan jumlah item terjual"""
    try:
        # Konversi kolom penjualan ke numerik
        df_plot = df.copy()
        
        # Hapus baris dengan NaN di product_col
        df_plot = df_plot.dropna(subset=[product_col])
        
        if len(df_plot) == 0:
            st.error(f"Kolom '{product_col}' tidak memiliki data yang valid!")
            return None
        
        # Group by product dan HITUNG JUMLAH (bukan sum sales)
        top_products = df_plot.groupby(product_col).size().sort_values(ascending=False).head(top_n)
        
        # Filter produk yang bukan error/invalid
        top_products = top_products[~top_products.index.astype(str).str.lower().isin(['error', 'nan', 'none', '', 'null'])]
        
        if len(top_products) == 0:
            st.error("Tidak ada data produk yang valid untuk ditampilkan!")
            return None
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(range(len(top_products)), top_products.values, color='steelblue', edgecolor='black', linewidth=1)
        
        # Tambahkan label jumlah di atas bar
        for i, (idx, val) in enumerate(top_products.items()):
            ax.text(i, val, f'{int(val)} produk', ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        ax.set_xticks(range(len(top_products)))
        ax.set_xticklabels(top_products.index, rotation=45, ha='right')
        ax.set_title(f'Top {len(top_products)} Produk Terlaris', fontsize=14, fontweight='bold')
        ax.set_xlabel('Produk', fontsize=12)
        ax.set_ylabel('Jumlah Produk Terjual', fontsize=12)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        plt.tight_layout()
        return fig
    except Exception as e:
        st.error(f"Error creating chart: {e}")
        return None

def perform_clustering(df, features, n_clusters, sales_col=None, random_state=42):
    """Melakukan clustering K-Means dan urutkan berdasarkan jumlah data"""
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df[features])
    
    kmeans = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=10)
    clusters = kmeans.fit_predict(X_scaled)
    
    silhouette_avg = silhouette_score(X_scaled, clusters)
    
    # Urutkan cluster berdasarkan JUMLAH DATA (jumlah transaksi)
    cluster_values = []
    for i in range(n_clusters):
        cluster_mask = clusters == i
        count = cluster_mask.sum()
        cluster_values.append((i, count))
    
    # Sort descending - dari banyak ke sedikit
    cluster_values.sort(key=lambda x: x[1], reverse=True)
    
    # Buat mapping: cluster lama -> cluster baru
    cluster_mapping = {old_id: new_id for new_id, (old_id, _) in enumerate(cluster_values)}
    
    # Remap clusters
    clusters_remapped = np.array([cluster_mapping[c] for c in clusters])
    
    return clusters_remapped, kmeans, scaler, X_scaled, silhouette_avg


def build_loyalty_sales_features(df, product_col, sales_col):
    """
    Bangun fitur per produk untuk segmentasi loyalitas vs penjualan:
    - frekuensi: jumlah transaksi (loyalitas)
    - total_penjualan: total nilai penjualan (revenue)
    - rata_penjualan: rata-rata nilai per transaksi
    Kembalikan DataFrame per produk dengan fitur-fitur tersebut.
    """
    df_temp = df.copy()
    df_temp[sales_col] = pd.to_numeric(df_temp[sales_col], errors='coerce')
    df_temp = df_temp.dropna(subset=[product_col, sales_col])

    agg = df_temp.groupby(product_col).agg(
        frekuensi=(sales_col, 'count'),
        total_penjualan=(sales_col, 'sum'),
        rata_penjualan=(sales_col, 'mean')
    ).reset_index()

    return agg


def perform_loyalty_clustering(df_agg, n_clusters, random_state=42):
    """
    Clustering segmentasi loyalitas vs penjualan tinggi.
    Input: df_agg hasil build_loyalty_sales_features
    Output: df_agg dengan kolom Cluster dan label segmen
    """
    features = ['frekuensi', 'total_penjualan', 'rata_penjualan']
    X = df_agg[features].values

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    kmeans = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=10)
    clusters = kmeans.fit_predict(X_scaled)

    silhouette_avg = silhouette_score(X_scaled, clusters) if n_clusters > 1 else 0.0

    df_agg = df_agg.copy()
    df_agg['Cluster'] = clusters

    # Hitung rata-rata frekuensi dan total_penjualan per cluster untuk labeling
    cluster_summary = df_agg.groupby('Cluster')[['frekuensi', 'total_penjualan']].mean()

    freq_median = cluster_summary['frekuensi'].median()
    sales_median = cluster_summary['total_penjualan'].median()

    def label_cluster(row):
        freq = cluster_summary.loc[row['Cluster'], 'frekuensi']
        sales = cluster_summary.loc[row['Cluster'], 'total_penjualan']
        tinggi_freq = freq >= freq_median
        tinggi_sales = sales >= sales_median
        if tinggi_freq and tinggi_sales:
            return 'Loyal & Penjualan Tinggi'
        elif tinggi_freq and not tinggi_sales:
            return 'Loyal & Penjualan Rendah'
        elif not tinggi_freq and tinggi_sales:
            return 'Jarang & Penjualan Tinggi'
        else:
            return 'Jarang & Penjualan Rendah'

    df_agg['Segmen'] = df_agg.apply(label_cluster, axis=1)

    return df_agg, X_scaled, silhouette_avg, cluster_summary


def plot_loyalty_scatter(df_agg):
    """Scatter plot frekuensi vs total penjualan dengan warna per segmen"""
    fig, ax = plt.subplots(figsize=(12, 8))

    segmen_list = df_agg['Segmen'].unique()
    colors = plt.cm.tab10(np.arange(len(segmen_list)))
    color_map = {seg: colors[i] for i, seg in enumerate(segmen_list)}

    for seg in segmen_list:
        subset = df_agg[df_agg['Segmen'] == seg]
        ax.scatter(subset['frekuensi'], subset['total_penjualan'],
                   label=seg, alpha=0.75, s=100,
                   color=color_map[seg], edgecolors='black', linewidth=0.5)

    ax.set_xlabel('Frekuensi Transaksi (Loyalitas)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Total Penjualan (Revenue)', fontsize=12, fontweight='bold')
    ax.set_title('Segmentasi Produk: Loyalitas vs Penjualan Tinggi', fontsize=14, fontweight='bold')
    ax.legend(loc='best', fontsize=10, framealpha=0.9)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_facecolor('#f8f9fa')
    plt.tight_layout()
    return fig

def plot_clustering_results(df, X_scaled, clusters, features):
    """Visualisasi hasil clustering"""
    df_plot = df.copy()
    df_plot['Cluster'] = clusters
    
    n_features = len(features)
    n_cols = min(3, n_features)
    n_rows = (n_features + n_cols - 1) // n_cols
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5*n_rows))
    if n_features == 1:
        axes = [axes]
    else:
        axes = axes.flatten() if n_features > 1 else [axes]
    
    # Warna yang lebih kontras untuk setiap cluster
    n_clusters = len(np.unique(clusters))
    colors = plt.cm.tab10(np.arange(n_clusters))
    
    for idx, feature in enumerate(features):
        ax = axes[idx]
        
        # Plot setiap cluster dengan warna berbeda
        for cluster_id in np.unique(clusters):
            cluster_mask = df_plot['Cluster'] == cluster_id
            cluster_data = df_plot[cluster_mask][feature]
            cluster_indices = cluster_data.index
            
            # Semua menggunakan marker bulat (circle)
            ax.scatter(cluster_indices, cluster_data, 
                      c=[colors[cluster_id]], 
                      label=f'Cluster {cluster_id} (n={len(cluster_data)})',
                      alpha=0.7, s=60, marker='o', edgecolors='black', linewidth=0.5)
        
        ax.set_title(f'Clustering: {feature}', fontsize=13, fontweight='bold', pad=10)
        ax.set_xlabel('Index Data', fontsize=11)
        ax.set_ylabel(feature, fontsize=11)
        ax.legend(loc='best', fontsize=9, framealpha=0.9)
        ax.grid(True, alpha=0.3, linestyle='--')
        
        # Set background color
        ax.set_facecolor('#f8f9fa')
    
    # Hapus subplot yang tidak digunakan
    for idx in range(len(features), len(axes)):
        fig.delaxes(axes[idx])
    
    plt.tight_layout()
    return fig

def plot_cluster_distribution(df, clusters):
    """Plot distribusi cluster"""
    fig, ax = plt.subplots(figsize=(10, 6))
    unique, counts = np.unique(clusters, return_counts=True)
    
    # Buat bar chart dengan warna berbeda per cluster
    colors = plt.cm.viridis(np.linspace(0, 1, len(unique)))
    bars = ax.bar(unique, counts, color=colors, edgecolor='black', linewidth=1.5)
    
    # Tambahkan label nilai di atas setiap bar
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    ax.set_title('Distribusi Data per Cluster', fontsize=14, fontweight='bold')
    ax.set_xlabel('Cluster', fontsize=12)
    ax.set_ylabel('Jumlah Data', fontsize=12)
    ax.set_xticks(unique)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    plt.tight_layout()
    return fig

def download_results(df, clusters):
    """Generate download link untuk hasil clustering"""
    df_result = df.copy()
    df_result['Cluster'] = clusters
    csv = df_result.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="hasil_clustering.csv">Download Hasil Clustering (CSV)</a>'
    return href

# Check login status
if not st.session_state.logged_in:
    show_login_page()
    st.stop()

# Main App (setelah login)
# Header dengan info user dan logout
col1, col2 = st.columns([3, 1])
with col1:
    st.title("Analisis Clustering K-Means - Data Penjualan")
with col2:
    st.write(f"User: **{st.session_state.user_name}**")
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.user_name = None
        st.rerun()

st.markdown("---")

# Menu navigasi
menu = st.sidebar.radio("Menu", ["Analisis Data", "History", "Pengaturan"])

if menu == "History":
    show_history_page()
    st.stop()

elif menu == "Pengaturan":
    st.title("Pengaturan Akun")
    
    # Fitur ubah password - admin bisa pilih akun, user biasa hanya akun sendiri
    if st.session_state.username == "admin":
        st.subheader("Ubah Password Akun")
        
        # Ambil daftar akun untuk dipilih
        try:
            import requests as _req2
            SUPA_URL2 = "https://xaudrzfhhssvliozsxbo.supabase.co"
            SUPA_KEY2 = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhhdWRyemZoaHNzdmxpb3pzeGJvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzk3NTU0OTQsImV4cCI6MjA5NTMzMTQ5NH0.vyeu-_zq9Ue9SpRHfqMR491508T6a1e54LFjpcoQdik"
            hdrs2 = {"apikey": SUPA_KEY2, "Authorization": f"Bearer {SUPA_KEY2}"}
            res2 = _req2.get(f"{SUPA_URL2}/rest/v1/users", headers=hdrs2, params={"select": "username,name"})
            all_users = res2.json()
            user_options = [u["username"] for u in all_users]
        except:
            user_options = [st.session_state.username]

        with st.form("change_password_form"):
            target_user = st.selectbox("Pilih Akun", user_options)
            new_password = st.text_input("Password Baru", type="password")
            confirm_new_password = st.text_input("Konfirmasi Password Baru", type="password")
            submit = st.form_submit_button("Ubah Password")

            if submit:
                if new_password and confirm_new_password:
                    if new_password == confirm_new_password:
                        # Update password langsung tanpa cek password lama (admin)
                        try:
                            import hashlib as _hl
                            new_hash = _hl.sha256(new_password.encode()).hexdigest()
                            res_upd = _req2.patch(
                                f"{SUPA_URL2}/rest/v1/users",
                                headers={**hdrs2, "Content-Type": "application/json"},
                                params={"username": f"eq.{target_user}"},
                                json={"password": new_hash, "password_plain": new_password}
                            )
                            if res_upd.status_code in [200, 204]:
                                st.success(f"Password akun '{target_user}' berhasil diubah!")
                            else:
                                st.error("Gagal mengubah password")
                        except Exception as e:
                            st.error(f"Error: {e}")
                    else:
                        st.error("Password baru tidak cocok!")
                else:
                    st.warning("Lengkapi semua field!")
    else:
        st.subheader("Ubah Password")
        with st.form("change_password_form"):
            old_password = st.text_input("Password Lama", type="password")
            new_password = st.text_input("Password Baru", type="password")
            confirm_new_password = st.text_input("Konfirmasi Password Baru", type="password")
            submit = st.form_submit_button("Ubah Password")
            
            if submit:
                if old_password and new_password and confirm_new_password:
                    if new_password == confirm_new_password:
                        success, message = auth_manager.change_password(
                            st.session_state.username, old_password, new_password
                        )
                        if success:
                            st.success(message)
                        else:
                            st.error(message)
                    else:
                        st.error("Password baru tidak cocok!")
                else:
                    st.warning("Lengkapi semua field!")

    # Fitur tambah akun - khusus admin
    if st.session_state.username == "admin":
        st.markdown("---")
        st.subheader("Kelola Akun Pengguna")

        # Tambah akun baru
        with st.expander("Tambah Akun Baru"):
            with st.form("add_user_form"):
                new_username = st.text_input("Username")
                new_name = st.text_input("Nama Lengkap")
                new_password = st.text_input("Password", type="password")
                confirm_password = st.text_input("Konfirmasi Password", type="password")
                add_submit = st.form_submit_button("Tambah Akun")

                if add_submit:
                    if new_username and new_name and new_password:
                        if new_password == confirm_password:
                            success, message = auth_manager.register(new_username, new_password, new_name, new_password)
                            if success:
                                st.success(f"Akun '{new_username}' berhasil ditambahkan!")
                            else:
                                st.error(message)
                        else:
                            st.error("Password tidak cocok!")
                    else:
                        st.warning("Lengkapi semua field!")

        # Daftar akun yang ada
        st.write("Daftar Akun Terdaftar:")
        try:
            import requests as _req
            SUPA_URL = "https://xaudrzfhhssvliozsxbo.supabase.co"
            SUPA_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhhdWRyemZoaHNzdmxpb3pzeGJvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzk3NTU0OTQsImV4cCI6MjA5NTMzMTQ5NH0.vyeu-_zq9Ue9SpRHfqMR491508T6a1e54LFjpcoQdik"
            hdrs = {"apikey": SUPA_KEY, "Authorization": f"Bearer {SUPA_KEY}"}
            res = _req.get(
                f"{SUPA_URL}/rest/v1/users",
                headers=hdrs,
                params={"select": "username,name,password_plain,created_at"}
            )
            users_data = res.json()
            user_list = [
                {
                    "Username": u["username"],
                    "Nama": u["name"],
                    "Password": u.get("password_plain", "-"),
                    "Dibuat": str(u.get("created_at", "-"))[:10]
                }
                for u in users_data
            ]
            st.dataframe(user_list, use_container_width=True, hide_index=True)
        except Exception as e:
            st.error(f"Gagal memuat daftar akun: {e}")

    st.stop()

# Main App - Analisis Data

# Sidebar
st.sidebar.header("Pengaturan")

# Upload File
uploaded_file = st.sidebar.file_uploader("Upload File CSV", type=['csv'])

if uploaded_file is not None:
    # Simpan file otomatis ke lokal (fallback)
    try:
        import os
        if not os.path.exists('uploads'):
            os.makedirs('uploads')
        file_path = os.path.join('uploads', uploaded_file.name)
        with open(file_path, 'wb') as f:
            f.write(uploaded_file.getbuffer())
    except Exception as e:
        pass

    # Load data dengan auto-detect encoding
    df, detected_delimiter = load_data(uploaded_file)

    if df is not None:
        # Debug: Tampilkan info kolom
        with st.expander("Info Kolom Dataset"):
            st.write(f"**Jumlah kolom:** {len(df.columns)}")
            st.write(f"**Jumlah baris:** {len(df)}")
            
            # Tampilkan tipe data setiap kolom
            col_info = pd.DataFrame({
                'Kolom': df.columns,
                'Tipe Data': df.dtypes.values,
                'Contoh Data': [str(df[col].iloc[0]) if len(df) > 0 else 'N/A' for col in df.columns],
                'Null Count': df.isnull().sum().values
            })
            st.dataframe(col_info, use_container_width=True)
            
            # Coba konversi kolom ke numerik
            st.write("**Mencoba konversi kolom ke numerik...**")
            numeric_candidates = []
            for col in df.columns:
                if df[col].dtype == 'object':
                    # Coba konversi ke numerik
                    converted = pd.to_numeric(df[col], errors='coerce')
                    non_null_count = converted.notna().sum()
                    if non_null_count > 0:
                        numeric_candidates.append({
                            'Kolom': col,
                            'Bisa Dikonversi': f"{non_null_count}/{len(df)} baris ({non_null_count/len(df)*100:.1f}%)"
                        })
            
            if numeric_candidates:
                st.success("Kolom yang bisa dikonversi ke numerik:")
                st.dataframe(pd.DataFrame(numeric_candidates), use_container_width=True)
                
                # Opsi untuk konversi otomatis
                if st.button("Konversi Kolom ke Numerik", key="convert_numeric"):
                    for col in df.columns:
                        if df[col].dtype == 'object':
                            converted = pd.to_numeric(df[col], errors='coerce')
                            # Konversi jika minimal 30% data valid
                            if converted.notna().sum() > len(df) * 0.3:
                                df[col] = converted
                    st.success("Konversi selesai! Refresh halaman untuk melihat perubahan.")
                    st.rerun()
            else:
                st.info("Tidak ada kolom yang bisa dikonversi ke numerik.")
        
        # Pilih kolom
        st.sidebar.subheader("Pilih Kolom Data")
        all_columns = df.columns.tolist()
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        # Auto-detect kolom customer
        customer_candidates = []
        for col in all_columns:
            col_lower = col.lower()
            if any(k in col_lower for k in ['customer', 'pelanggan', 'pembeli', 'nama', 'name', 'client', 'buyer']):
                if 'id' not in col_lower and 'code' not in col_lower:
                    customer_candidates.append(col)
        default_customer = customer_candidates[0] if customer_candidates else all_columns[0]
        
        customer_col = st.sidebar.selectbox(
            "Kolom Customer (Pelanggan)",
            all_columns,
            index=all_columns.index(default_customer) if default_customer in all_columns else 0
        )
        
        # Auto-detect kolom produk
        product_candidates = []
        for col in all_columns:
            col_lower = col.lower()
            if any(keyword in col_lower for keyword in ['product', 'item', 'nama barang', 'barang', 'menu']):
                if 'id' not in col_lower and 'code' not in col_lower:
                    product_candidates.append(col)
        default_product = product_candidates[0] if product_candidates else all_columns[0]
        
        product_col = st.sidebar.selectbox(
            "Kolom Produk",
            all_columns,
            index=all_columns.index(default_product) if default_product in all_columns else 0
        )
        
        # Coba konversi kolom TOTAL dan JUMLAH ke numerik jika belum
        for col in df.columns:
            if col.upper().strip() in ['TOTAL', 'JUMLAH']:
                cleaned = (df[col].astype(str)
                           .str.replace(r'Rp', '', regex=False)
                           .str.replace(r'\s', '', regex=True)
                           .str.replace(r'\.', '', regex=True)
                           .str.replace(',', '.', regex=False))
                converted = pd.to_numeric(cleaned, errors='coerce')
                if converted.notna().sum() > len(df) * 0.3:
                    df[col] = converted

        # Refresh setelah konversi
        all_columns = df.columns.tolist()
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

        # Kolom yang bisa dipilih untuk harga: semua kolom kecuali NO/ID
        harga_col_options = [c for c in all_columns
                             if c.lower().strip() not in ['no', 'no.', 'nomor', 'number', 'id', 'index']]

        # Default: pilih kolom bernama TOTAL dulu, lalu JUMLAH, lalu kolom numerik lain
        total_exact = [c for c in harga_col_options if c.upper().strip() == 'TOTAL']
        jumlah_exact = [c for c in harga_col_options if c.upper().strip() == 'JUMLAH']
        numeric_harga = [c for c in numeric_cols if c.lower().strip() not in ['no', 'no.', 'nomor', 'number', 'id', 'index']]

        if total_exact:
            default_harga = total_exact[0]
        elif jumlah_exact:
            default_harga = jumlah_exact[0]
        elif numeric_harga:
            default_harga = numeric_harga[0]
        else:
            default_harga = harga_col_options[0] if harga_col_options else all_columns[0]

        sales_col = st.sidebar.selectbox(
            "Kolom Harga/Nilai Transaksi",
            harga_col_options,
            index=harga_col_options.index(default_harga) if default_harga in harga_col_options else 0,
            help="Pilih kolom yang berisi nilai uang/harga per transaksi"
        )

        # Konversi sales_col ke numerik jika belum
        if df[sales_col].dtype == object:
            cleaned = (df[sales_col].astype(str)
                       .str.replace(r'Rp', '', regex=False)
                       .str.replace(r'\s', '', regex=True)
                       .str.replace(r'\.', '', regex=True)
                       .str.replace(',', '.', regex=False))
            df[sales_col] = pd.to_numeric(cleaned, errors='coerce')
        
        # Parameter clustering
        st.sidebar.subheader("Parameter Clustering")
        n_clusters = st.sidebar.slider("Jumlah Cluster", 2, 5, 3)
        
        # Pembersihan Data
        st.header("Pembersihan Data")
        df_cleaned, removed, duplicates, unknown_per_column, unknown_count = clean_data(df)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Data Awal", len(df))
        with col2:
            st.metric("Data Dihapus", removed)
        with col3:
            st.metric("Data Bersih", len(df_cleaned))
        
        # Detail data yang dihapus
        if removed > 0:
            with st.expander("Detail Data yang Dihapus"):
                st.write(f"**Total baris dihapus:** {removed}")
                st.write(f"**Duplikat dihapus:** {duplicates}")
                st.write(f"**Baris dengan data 'unknown':** {unknown_count}")
                
                if unknown_count > 0:
                    st.write("**Data 'unknown' per kolom:**")
                    st.write("(Termasuk variasi: unknown, n/a, na, -, kosong)")
                    unknown_df = pd.DataFrame({
                        'Kolom': list(unknown_per_column.keys()),
                        'Jumlah Unknown': list(unknown_per_column.values())
                    })
                    st.dataframe(unknown_df, use_container_width=True)
                
                st.info("""
                **Catatan:** 
                - Hanya data duplikat dan data 'unknown' yang dihapus
                - Missing values (NaN) TIDAK dihapus
                - Data dengan nilai kosong atau '-' dianggap unknown
                """)
        
        # ============================================================
        # SEGMENTASI PELANGGAN - INTI SISTEM
        # ============================================================

        # Tampilkan Data CSV
        # Auto-detect tahun dari kolom tanggal
        tahun_dataset = ""
        for col in df_cleaned.columns:
            if any(k in col.lower() for k in ['tanggal', 'date', 'waktu', 'time', 'created', 'order']):
                try:
                    tgl = pd.to_datetime(df_cleaned[col], errors='coerce')
                    tahun_list = sorted(tgl.dt.year.dropna().unique().astype(int))
                    if tahun_list:
                        if len(tahun_list) == 1:
                            tahun_dataset = f" {tahun_list[0]}"
                        else:
                            tahun_dataset = f" {tahun_list[0]}-{tahun_list[-1]}"
                        break
                except:
                    pass

        st.header(f"Data Penjualan{tahun_dataset}")
        st.write(f"Menampilkan **{len(df_cleaned):,}** baris data")
        rows_to_show = st.slider("Jumlah baris yang ditampilkan", 10, len(df_cleaned), min(100, len(df_cleaned)))
        st.dataframe(df_cleaned.head(rows_to_show), use_container_width=True, hide_index=True)

        # Statistik Penjualan - ambil dari kolom TOTAL jika ada
        st.header("Statistik Penjualan")
        # Pakai sales_col yang sudah dipilih (sudah auto-detect ke TOTAL)
        total_data, total_sales, avg_sales = calculate_statistics(df_cleaned, sales_col)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Data Penjualan", f"{total_data:,} produk")
        with col2:
            total_formatted = f"{total_sales:,.0f}".replace(",", ".")
            st.metric("Total Penghasilan", f"Rp {total_formatted}")
            if total_sales >= 1_000_000_000:
                st.caption(f"({total_sales/1_000_000_000:.2f} miliar rupiah)")
            elif total_sales >= 1_000_000:
                st.caption(f"({total_sales/1_000_000:.2f} juta rupiah)")
            elif total_sales >= 1_000:
                st.caption(f"({total_sales/1_000:.2f} ribu rupiah)")
            else:
                st.caption(f"({total_sales:.0f} rupiah)")
        with col3:
            avg_formatted = f"{avg_sales:,.0f}".replace(",", ".")
            st.metric("Rata-rata Penjualan", f"Rp {avg_formatted}")
            if avg_sales >= 1_000_000:
                st.caption(f"({avg_sales/1_000_000:.2f} juta per transaksi)")
            elif avg_sales >= 1_000:
                st.caption(f"({avg_sales/1_000:.2f} ribu per transaksi)")
            else:
                st.caption(f"({avg_sales:.0f} rupiah per transaksi)")

        st.markdown("---")
        st.header("Segmentasi Pelanggan K-Means")

        if customer_col and sales_col and customer_col in df_cleaned.columns and sales_col in df_cleaned.columns:

            df_seg = df_cleaned.copy()
            df_seg[sales_col] = pd.to_numeric(df_seg[sales_col], errors='coerce')
            df_seg = df_seg.dropna(subset=[customer_col, sales_col])

            # Agregasi per CUSTOMER
            df_agg = df_seg.groupby(customer_col).agg(
                Frekuensi=(sales_col, 'count'),
                Total_Belanja=(sales_col, 'sum')
            ).reset_index()

            if len(df_agg) < n_clusters:
                st.warning(f"Jumlah customer unik ({len(df_agg)}) lebih sedikit dari jumlah cluster ({n_clusters}). Kurangi jumlah cluster di sidebar.")
            else:
                X = df_agg[['Frekuensi', 'Total_Belanja']].values
                scaler_seg = StandardScaler()
                X_scaled = scaler_seg.fit_transform(X)

                kmeans_seg = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
                raw_clusters = kmeans_seg.fit_predict(X_scaled)
                silhouette = silhouette_score(X_scaled, raw_clusters) if n_clusters > 1 else 0.0

                df_agg['Cluster'] = raw_clusters

                # Label berdasarkan NILAI TOTAL BELANJA (bukan ranking K-Means)
                # Sultan >= 20 juta, Hemat 5-20 juta, Baru/Pasif < 5 juta
                def assign_label(total):
                    if total >= 20_000_000:
                        return 'Sultan / Loyal'
                    elif total >= 5_000_000:
                        return 'Hemat'
                    else:
                        return 'Baru / Pasif'

                df_agg['Segmen'] = df_agg['Total_Belanja'].apply(assign_label)

                # Metrik
                st.subheader("Metrik Clustering")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Jumlah Cluster", n_clusters)
                with col2:
                    st.metric("Silhouette Score", f"{silhouette:.3f}")
                with col3:
                    st.metric("Total Customer Dianalisis", len(df_agg))

                # Grafik segmentasi
                st.subheader("Grafik Segmentasi Pelanggan")
                st.caption(f"Sumbu X = Frekuensi belanja customer | Sumbu Y = Total belanja dari kolom '{sales_col}'")
                seg_colors = {
                    'Sultan / Loyal': '#e74c3c',
                    'Hemat': '#2ecc71',
                    'Baru / Pasif': '#3498db'
                }
                fig_seg, ax = plt.subplots(figsize=(12, 8))
                for seg, color in seg_colors.items():
                    subset = df_agg[df_agg['Segmen'] == seg]
                    if len(subset) == 0:
                        continue
                    # Titik data individual - jelas dan solid
                    ax.scatter(subset['Frekuensi'], subset['Total_Belanja'],
                               label=f"{seg} ({len(subset)} customer)",
                               color=color, alpha=1.0, s=200,
                               edgecolors='black', linewidth=1.5,
                               marker='o', zorder=5)
                    # Label nama customer
                    for _, row in subset.iterrows():
                        ax.annotate(str(row[customer_col])[:12],
                                    (row['Frekuensi'], row['Total_Belanja']),
                                    textcoords='offset points', xytext=(6, 6),
                                    fontsize=8, fontweight='bold', alpha=1.0)
                    # Centroid - bulat besar dengan border tebal
                    ax.scatter(subset['Frekuensi'].mean(), subset['Total_Belanja'].mean(),
                               color=color, s=800, edgecolors='black', linewidth=3,
                               zorder=10, marker='o', alpha=1.0)

                ax.set_xlabel('Frekuensi Belanja (Jumlah Transaksi)', fontsize=13, fontweight='bold')
                ax.set_ylabel(f'Total Belanja ({sales_col})', fontsize=13, fontweight='bold')
                ax.set_title('Segmentasi Pelanggan: Loyalitas vs Total Belanja', fontsize=15, fontweight='bold')
                ax.legend(loc='upper left', fontsize=11, framealpha=0.95)
                ax.grid(True, alpha=0.3, linestyle='--')
                ax.set_facecolor('#f8f9fa')
                ax.yaxis.set_major_formatter(
                    plt.FuncFormatter(lambda x, _: f'{x:,.0f}'.replace(',', '.'))
                )
                plt.tight_layout()
                st.pyplot(fig_seg)

                # Tombol download grafik sebagai PNG
                import io
                buf = io.BytesIO()
                fig_seg.savefig(buf, format='png', dpi=150, bbox_inches='tight')
                buf.seek(0)
                st.download_button(
                    label="Download Grafik Clustering (PNG)",
                    data=buf,
                    file_name=f"grafik_segmentasi_{uploaded_file.name.replace('.csv','')}.png",
                    mime='image/png'
                )
                plt.close(fig_seg)

                # Ringkasan segmen
                col1, col2, col3 = st.columns(3)
                with col1:
                    n_sultan = len(df_agg[df_agg['Segmen'] == 'Sultan / Loyal'])
                    st.metric("Sultan / Loyal", f"{n_sultan} customer")
                    st.caption("Sering belanja + belanja besar")
                with col2:
                    n_hemat = len(df_agg[df_agg['Segmen'] == 'Hemat'])
                    st.metric("Hemat", f"{n_hemat} customer")
                    st.caption("Sering belanja + belanja kecil")
                with col3:
                    n_pasif = len(df_agg[df_agg['Segmen'] == 'Baru / Pasif'])
                    st.metric("Baru / Pasif", f"{n_pasif} customer")
                    st.caption("Jarang belanja + belanja kecil")

                # Tabel hasil per customer
                st.subheader("Daftar Customer per Segmen")
                df_cust = df_agg[[customer_col, 'Frekuensi', 'Total_Belanja', 'Segmen']].copy()
                segmen_order = {'Sultan / Loyal': 0, 'Hemat': 1, 'Baru / Pasif': 2}
                df_cust['_sort'] = df_cust['Segmen'].map(segmen_order).fillna(3)
                df_cust = df_cust.sort_values(['_sort', 'Total_Belanja'], ascending=[True, False])
                df_cust = df_cust.drop(columns=['_sort'])
                df_cust['Total_Belanja_Fmt'] = df_cust['Total_Belanja'].apply(
                    lambda x: f"{x:,.0f}".replace(',', '.')
                )
                df_show = df_cust[[customer_col, 'Frekuensi', 'Total_Belanja_Fmt', 'Segmen']].copy()
                df_show.columns = ['Customer', 'Frekuensi Belanja', f'Total {sales_col}', 'Segmen']
                st.dataframe(df_show, use_container_width=True, hide_index=True)

                # Auto-save ke history
                analysis_key = f"{uploaded_file.name}_{n_clusters}_{len(df_agg)}_{silhouette:.3f}"
                if 'last_saved_analysis' not in st.session_state:
                    st.session_state.last_saved_analysis = None

                if st.session_state.last_saved_analysis != analysis_key:
                    result_filename = f"hasil_clustering_{st.session_state.username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                    result_path = os.path.join('uploads', result_filename)
                    df_agg.to_csv(result_path, index=False)
                    analysis_data = {
                        'filename': uploaded_file.name,
                        'n_clusters': n_clusters,
                        'silhouette_score': float(silhouette),
                        'features': ['Frekuensi', 'Total_Belanja'],
                        'total_data': len(df_agg),
                        'total_sales': float(df_agg['Total_Belanja'].sum()),
                        'result_file': result_filename,
                        'product_col': product_col,
                        'sales_col': sales_col
                    }
                    history_id = history_manager.save_analysis(st.session_state.username, analysis_data)
                    st.session_state.last_saved_analysis = analysis_key
                    st.success(f"Analisis otomatis tersimpan ke history (ID: {history_id})")
                else:
                    st.info("Analisis ini sudah tersimpan di history")

                # Download - paling bawah
                st.markdown("---")
                st.subheader("Download Hasil Analisis")
                csv_bytes = df_agg.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download Hasil Segmentasi CSV",
                    data=csv_bytes,
                    file_name=f"segmentasi_{uploaded_file.name}",
                    mime='text/csv'
                )
        else:
            st.warning("Pilih kolom produk dan kolom harga/nilai transaksi yang valid di sidebar.")

        st.markdown("---")

        # Grafik Penjualan
        st.header("Visualisasi Penjualan")
        
        # Opsi pilih jenis grafik
        graph_type = st.radio(
            "Pilih Jenis Grafik:",
            ["Produk Terlaris", "Penjualan per Bulan"],
            horizontal=True
        )
        
        if graph_type == "Produk Terlaris":
            # Grafik Produk Terlaris
            if product_col in df_cleaned.columns and sales_col in df_cleaned.columns:
                # Opsi untuk memilih tampilan
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.info(f"Grafik berdasarkan: **{product_col}** (produk) dan **{sales_col}** (penjualan)")
                with col2:
                    # Cek apakah ada kolom kategori
                    category_cols = [col for col in df_cleaned.columns if 'categor' in col.lower() or 'type' in col.lower() or 'class' in col.lower()]
                    
                    if len(category_cols) > 0:
                        view_option = st.selectbox(
                            "Tampilkan berdasarkan:",
                            ["Nama Produk", "Kategori Produk"],
                            help="Pilih apakah ingin melihat per produk atau per kategori"
                        )
                        
                        if view_option == "Kategori Produk":
                            # Pilih kolom kategori
                            category_col = st.selectbox("Pilih Kolom Kategori", category_cols)
                            display_col = category_col
                        else:
                            display_col = product_col
                    else:
                        display_col = product_col
                        st.caption("Tidak ada kolom kategori terdeteksi")
                
                top_n = st.slider("Jumlah Teratas", 5, 20, 10)
                fig_top = plot_top_products(df_cleaned, display_col, sales_col, top_n)
                if fig_top:
                    st.pyplot(fig_top)
                    plt.close(fig_top)
            else:
                st.warning("Pilih kolom produk dan penjualan yang valid untuk melihat grafik.")
        
        else:
            # Grafik Penjualan per Bulan
            # Fungsi konversi tanggal Indonesia
            def convert_indo_date(series):
                bulan_indo = {
                    'januari': 'January', 'februari': 'February', 'maret': 'March',
                    'april': 'April', 'mei': 'May', 'juni': 'June',
                    'juli': 'July', 'agustus': 'August', 'september': 'September',
                    'oktober': 'October', 'november': 'November', 'desember': 'December'
                }
                def parse_one(val):
                    s = str(val).strip().lower()
                    for indo, eng in bulan_indo.items():
                        s = s.replace(indo, eng)
                    try:
                        return pd.to_datetime(s, dayfirst=True)
                    except:
                        return pd.NaT
                return series.apply(parse_one)

            # Cari kolom tanggal
            date_cols = []
            for col in df_cleaned.columns:
                col_lower = col.lower()
                date_keywords = [
                    'date', 'tanggal', 'waktu', 'time', 'created', 'order',
                    'dibuat', 'pesanan', 'transaksi', 'transaction', 'timestamp',
                    'tgl', 'datetime', 'bulan', 'tahun', 'month', 'year'
                ]
                if any(keyword in col_lower for keyword in date_keywords):
                    try:
                        # Coba konversi biasa dulu
                        test_convert = pd.to_datetime(df_cleaned[col].head(10), errors='coerce')
                        if test_convert.notna().sum() >= 3:
                            date_cols.append(col)
                            continue
                        # Coba konversi format Indonesia
                        test_convert2 = convert_indo_date(df_cleaned[col].head(10))
                        if test_convert2.notna().sum() >= 3:
                            date_cols.append(col)
                    except:
                        pass
            
            if len(date_cols) > 0:
                date_col = st.selectbox("Pilih Kolom Tanggal", date_cols,
                                       help="Pilih kolom yang berisi tanggal/waktu transaksi")
                
                # Extract tahun yang tersedia
                df_cleaned_temp = df_cleaned.copy()
                df_cleaned_temp[date_col] = pd.to_datetime(df_cleaned_temp[date_col], errors='coerce')
                available_years = sorted(df_cleaned_temp[date_col].dt.year.dropna().unique())
                
                if len(available_years) > 0:
                    year_options = ["Semua Tahun"] + [str(year) for year in available_years]
                    selected_year = st.selectbox("Pilih Tahun", year_options,
                                                help="Filter data berdasarkan tahun")
                else:
                    selected_year = "Semua Tahun"
                
                fig_monthly = plot_monthly_sales(df_cleaned, date_col, sales_col, selected_year)
                if fig_monthly:
                    st.pyplot(fig_monthly)
                    plt.close(fig_monthly)
                    
                    # Tampilkan info bulan tertinggi
                    df_temp = df_cleaned.copy()
                    df_temp[date_col] = pd.to_datetime(df_temp[date_col], errors='coerce')
                    
                    if selected_year and selected_year != "Semua Tahun":
                        df_temp = df_temp[df_temp[date_col].dt.year == int(selected_year)]
                    
                    if len(df_temp) > 0:
                        df_temp['Month'] = df_temp[date_col].dt.strftime('%B %Y')
                        monthly_count = df_temp.groupby('Month').size()
                        top_month = monthly_count.idxmax()
                        top_count = monthly_count.max()
                        
                        st.success(f"Bulan dengan penjualan tertinggi: **{top_month}** ({top_count} produk terjual)")
            else:
                st.warning("""
                Tidak ada kolom tanggal terdeteksi.
                
                Pastikan file CSV Anda memiliki kolom tanggal dengan nama seperti:
                - Date, Tanggal, Waktu
                - Created, Order Date
                - Waktu Pesanan Dibuat
                - Transaction Date
                """)
                
                # Debug: tampilkan semua kolom
                with st.expander("Debug: Lihat Semua Kolom"):
                    st.write("Kolom yang tersedia:")
                    for col in df_cleaned.columns:
                        st.write(f"- {col}")
else:
    st.info("Upload file CSV untuk memulai analisis")
