import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
import plotly.graph_objects as go
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- Konfigurasi halaman
st.set_page_config(
    page_title="Tourism Data Warehouse",
    layout="wide",
    page_icon="🏝️",
    initial_sidebar_state="expanded"
)

# --- Custom CSS untuk tampilan yang clean
st.markdown("""
<style>
    /* Main background */
    .main {
        background-color: #f8f9fa;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2E8BC0 0%, #145DA0 100%);
    }
    
    /* Card styling untuk metrics */
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #2E8BC0;
        margin-bottom: 10px;
    }
    
    /* Title styling */
    .main-title {
        color: #145DA0;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    .section-title {
        color: #2E8BC0;
        font-size: 1.5rem;
        font-weight: 600;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e9ecef;
    }
    
    /* Button styling */
    .stButton button {
        background: linear-gradient(45deg, #2E8BC0, #145DA0);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 500;
    }
    
    .stButton button:hover {
        background: linear-gradient(45deg, #145DA0, #0C2D48);
        color: white;
    }
    
    /* SELECTBOX FIX - PERBAIKAN UTAMA */
    .stSelectbox > div > div {
        border-radius: 8px !important;
        border: 2px solid #e9ecef !important;
        padding: 4px 8px !important;
        min-height: 40px !important;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #2E8BC0 !important;
    }
    
    .stSelectbox > div > div[data-baseweb="select"] > div {
        border-radius: 8px !important;
    }
    
    /* Dropdown menu styling */
    div[role="listbox"] {
        border-radius: 8px !important;
        border: 2px solid #e9ecef !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important;
        max-height: 300px !important;
        overflow-y: auto !important;
    }
    
    div[role="listbox"] > div {
        padding: 10px 15px !important;
        border-bottom: 1px solid #f1f3f4 !important;
    }
    
    div[role="listbox"] > div:hover {
        background-color: #f8f9fa !important;
    }
    
    div[role="listbox"] > div[aria-selected="true"] {
        background-color: #2E8BC0 !important;
        color: white !important;
    }
    
    /* Dataframe styling */
    .dataframe {
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    /* Radio button styling */
    div[role="radiogroup"] > label {
        background-color: rgba(255,255,255,0.1) !important;
        border-radius: 10px !important;
        padding: 8px 12px !important;
        margin: 5px 0px !important;
        transition: all 0.3s ease-in-out !important;
        font-weight: 500 !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
    }
    
    div[role="radiogroup"] > label:hover {
        background-color: rgba(255,255,255,0.25) !important;
        transform: scale(1.03) !important;
    }
    
    div[role="radiogroup"] > label[data-checked="true"] {
        background-color: #00A8E8 !important;
        color: white !important;
        font-weight: bold !important;
        border: 1px solid #00A8E8 !important;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_database_connection():
    """Koneksi ke Supabase dengan pooling"""
    try:
        DB_USER = st.secrets["DB_USER"]
        DB_PASSWORD = st.secrets["DB_PASSWORD"]
        DB_HOST = st.secrets["DB_HOST"]
        DB_PORT = st.secrets["DB_PORT"]
        DB_NAME = st.secrets["DB_NAME"]
        
        # Gunakan connection pooling
        DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        
        # Tambahkan parameter connection
        engine = create_engine(
            DATABASE_URL,
            pool_size=5,
            max_overflow=10,
            pool_pre_ping=True
        )
        
        # Test connection dengan timeout
        with engine.connect() as conn:
            conn.execute("SELECT 1")
            
        return engine
        
    except Exception as e:
        st.error(f"❌ Database connection failed: {e}")
        return None

@st.cache_data
def load_data(_engine, table_name):
    """Load data dari tabel dengan caching"""
    try:
        df = pd.read_sql(f"SELECT * FROM {table_name}", _engine)
        return df
    except Exception as e:
        st.error(f"❌ Gagal memuat tabel {table_name}: {e}")
        return pd.DataFrame()

# --- Function untuk membuat metric card
def metric_card(title, value, delta=None, delta_color="normal"):
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 0.9rem; color: #6c757d; margin-bottom: 5px;">{title}</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: #145DA0;">{value}</div>
            {f'<div style="font-size: 0.8rem; color: {"green" if delta_color == "normal" else "red"};">{delta}</div>' if delta else ''}
        </div>
        """, unsafe_allow_html=True)

def main():
    # Dapatkan koneksi database
    engine = get_database_connection()
    
    if engine is None:
        st.error("""
        🔧 **Database Connection Troubleshooting:**
        1. Pastikan PostgreSQL berjalan
        2. Cek password di kode (ganti 'your_password_here')
        3. Pastikan database 'tourism_warehouse' ada
        4. Jalankan etl.py terlebih dahulu untuk membuat tabel
        """)
        return
    
    # Load data dengan error handling
    try:
        with st.spinner('🔄 Memuat data dari database...'):
            tourism_df = load_data(engine, "tourism_with_id")
            rating_df = load_data(engine, "tourism_rating")
            user_df = load_data(engine, "users")
            package_df = load_data(engine, "package_tourism")
            
        # Cek jika ada DataFrame yang kosong
        if tourism_df.empty:
            st.error("Tabel 'tourism_with_id' kosong atau tidak ada. Jalankan etl.py terlebih dahulu!")
            return
        if rating_df.empty:
            st.error("Tabel 'tourism_rating' kosong atau tidak ada.")
            return
        if user_df.empty:
            st.error("Tabel 'users' kosong atau tidak ada.")
            return
        if package_df.empty:
            st.error("Tabel 'package_tourism' kosong atau tidak ada.")
            return
            
        st.success("✅ Data berhasil dimuat!")
        
    except Exception as e:
        st.error(f"❌ Error memuat data: {e}")
        return

    # --- Sidebar Navigasi
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h1 style="color: white; font-size: 24px; margin-bottom: 5px;">🏝️</h1>
        <h2 style="color: white; font-size: 18px; font-weight: 700;">Tourism Data Warehouse</h2>
        <p style="color: #d9e6f2; font-size: 12px;">Analisis Data Pariwisata</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("---")

    # Navigation dengan icons yang clean
    menu_options = {
        "🏠 Dashboard Utama": "dashboard",
        "⭐ Analisis Rating": "rating", 
        "🏙️ Analisis Wisata": "wisata",
        "💼 Analisis Paket": "paket",
        "🌟 Rekomendasi": "rekomendasi",
        "🗃️ Data Viewer": "viewer"
    }
    
    selected_menu = st.sidebar.radio(
        "**NAVIGASI**",
        list(menu_options.keys()),
        label_visibility="collapsed"
    )

    st.sidebar.markdown("---")
    
    # Info tambahan di sidebar
    st.sidebar.markdown("""
    <div style="color: #d9e6f2; font-size: 12px; text-align: center;">
        <p><strong>Kelompok 1</strong></p>
        <p>Teknologi Basis Data</p>
    </div>
    """, unsafe_allow_html=True)

    # =====================================================================================
    # 🏠 DASHBOARD UTAMA
    # =====================================================================================
    if selected_menu == "🏠 Dashboard Utama":
        st.markdown('<div class="main-title">📊 Tourism Analytics Dashboard</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: linear-gradient(45deg, #2E8BC0, #145DA0); color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
            <h3 style="margin: 0; font-size: 1.2rem;">Selamat Datang di Dashboard Pariwisata</h3>
            <p style="margin: 5px 0 0 0; opacity: 0.9;">Analisis komprehensif data tempat wisata, rating, dan paket perjalanan</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Metrics dalam grid yang rapi
        st.markdown('<div class="section-title">📈 Overview Data</div>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            metric_card("Total Tempat Wisata", len(tourism_df))
        with col2:
            metric_card("Total Pengguna", len(user_df))
        with col3:
            metric_card("Total Paket Wisata", len(package_df))
        with col4:
            metric_card("Total Rating", len(rating_df))
        
        # Visualisasi dalam tabs
        st.markdown('<div class="section-title">📊 Visualisasi Data</div>', unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["🏞️ Distribusi Kategori", "🏙️ Wisata per Kota", "📈 Analisis Rating"])
        
        with tab1:
            if 'Category' in tourism_df.columns:
                col1, col2 = st.columns([2, 1])
                with col1:
                    category_counts = tourism_df['Category'].value_counts()
                    fig = px.bar(
                        x=category_counts.index,
                        y=category_counts.values,
                        title="Jumlah Tempat Wisata per Kategori",
                        color=category_counts.values,
                        color_continuous_scale='Blues'
                    )
                    fig.update_layout(
                        xaxis_title="Kategori",
                        yaxis_title="Jumlah",
                        showlegend=False
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    fig_pie = px.pie(
                        values=category_counts.values,
                        names=category_counts.index,
                        title="Persentase Kategori"
                    )
                    st.plotly_chart(fig_pie, use_container_width=True)
        
        with tab2:
            if 'City' in tourism_df.columns:
                city_counts = tourism_df['City'].value_counts().head(10)
                fig = px.bar(
                    x=city_counts.values,
                    y=city_counts.index,
                    orientation='h',
                    title="10 Kota dengan Wisata Terbanyak",
                    color=city_counts.values,
                    color_continuous_scale='Viridis'
                )
                fig.update_layout(
                    xaxis_title="Jumlah Wisata",
                    yaxis_title="Kota"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            # Cari kolom rating
            rating_column = None
            for col in rating_df.columns:
                if 'rating' in col.lower() or 'Rating' in col:
                    rating_column = col
                    break
            
            if rating_column:
                avg_rating = rating_df.groupby('Place_Id')[rating_column].mean()
                fig = px.histogram(
                    x=avg_rating.values,
                    title="Distribusi Rating Tempat Wisata",
                    nbins=20,
                    color_discrete_sequence=['#2E8BC0']
                )
                fig.update_layout(
                    xaxis_title="Rating",
                    yaxis_title="Jumlah Tempat Wisata"
                )
                st.plotly_chart(fig, use_container_width=True)

    # =====================================================================================
    # ⭐ ANALISIS RATING
    # =====================================================================================
    elif selected_menu == "⭐ Analisis Rating":
        st.markdown('<div class="main-title">⭐ Analisis Rating Tempat Wisata</div>', unsafe_allow_html=True)
        
        # Cari kolom rating
        rating_column = None
        for col in rating_df.columns:
            if 'rating' in col.lower() or 'Rating' in col:
                rating_column = col
                break
        
        if rating_column:
            # Hitung rata-rata rating
            avg_rating = rating_df.groupby('Place_Id')[rating_column].mean().reset_index()
            avg_rating = avg_rating.merge(tourism_df[['Place_Id', 'Place_Name', 'City', 'Category']], on='Place_Id', how='left')
            avg_rating = avg_rating.rename(columns={rating_column: 'Place_Ratings'})
            avg_rating = avg_rating.sort_values('Place_Ratings', ascending=False)

            col1, col2 = st.columns([3, 1])
            
            with col1:
                # Top 10 tempat wisata
                st.markdown('<div class="section-title">🏆 Top 10 Tempat Wisata Berdasarkan Rating</div>', unsafe_allow_html=True)
                top10 = avg_rating.head(10)
                
                if not top10.empty:
                    fig = px.bar(
                        top10,
                        x='Place_Name',
                        y='Place_Ratings',
                        text='Place_Ratings',
                        color='City',
                        title="",
                        color_discrete_sequence=px.colors.qualitative.Bold
                    )
                    fig.update_traces(
                        texttemplate='%{text:.2f}', 
                        textposition='outside',
                        marker_line_color='black',
                        marker_line_width=1
                    )
                    fig.update_layout(
                        xaxis_title="Nama Tempat Wisata",
                        yaxis_title="Rating Rata-rata",
                        xaxis_tickangle=-45,
                        showlegend=True
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown('<div class="section-title">📊 Statistik</div>', unsafe_allow_html=True)
                metric_card("Rating Tertinggi", f"{avg_rating['Place_Ratings'].max():.2f}")
                metric_card("Rating Terendah", f"{avg_rating['Place_Ratings'].min():.2f}")
                metric_card("Rating Rata-rata", f"{avg_rating['Place_Ratings'].mean():.2f}")
                
                # Filter by category
                if 'Category' in avg_rating.columns:
                    st.markdown("**Filter by Kategori:**")
                    selected_category = st.selectbox("Pilih kategori:", ["All"] + list(avg_rating['Category'].unique()))
                    if selected_category != "All":
                        filtered_data = avg_rating[avg_rating['Category'] == selected_category]
                        st.metric(f"Rating Rata-rata ({selected_category})", f"{filtered_data['Place_Ratings'].mean():.2f}")

            # Data table
            st.markdown('<div class="section-title">📋 Data Detail</div>', unsafe_allow_html=True)
            st.dataframe(
                avg_rating[['Place_Name', 'City', 'Category', 'Place_Ratings']].head(20),
                use_container_width=True
            )

    # =====================================================================================
    # 🏙️ ANALISIS WISATA
    # =====================================================================================
    elif selected_menu == "🏙️ Analisis Wisata":
        st.markdown('<div class="main-title">🏙️ Analisis Tempat Wisata</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            if 'City' in tourism_df.columns:
                st.markdown('<div class="section-title">🏘️ Distribusi Wisata per Kota</div>', unsafe_allow_html=True)
                wisata_per_kota = tourism_df['City'].value_counts().reset_index()
                wisata_per_kota.columns = ['City', 'Jumlah_Wisata']

                fig = px.bar(
                    wisata_per_kota.head(15),
                    x='City',
                    y='Jumlah_Wisata',
                    text='Jumlah_Wisata',
                    color='Jumlah_Wisata',
                    color_continuous_scale='Teal'
                )
                fig.update_traces(textposition='outside')
                fig.update_layout(
                    xaxis_title="Kota",
                    yaxis_title="Jumlah Tempat Wisata",
                    showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown('<div class="section-title">🎯 Filter Data</div>', unsafe_allow_html=True)
            
            # Filter by category
            if 'Category' in tourism_df.columns:
                selected_category = st.selectbox(
                    "Pilih Kategori:",
                    ["All Categories"] + sorted(tourism_df['Category'].unique())
                )
                
                if selected_category != "All Categories":
                    filtered_df = tourism_df[tourism_df['Category'] == selected_category]
                    st.metric(f"Jumlah {selected_category}", len(filtered_df))
                else:
                    filtered_df = tourism_df
                
                # Filter by city
                if 'City' in tourism_df.columns:
                    selected_city = st.selectbox(
                        "Pilih Kota:",
                        ["All Cities"] + sorted(tourism_df['City'].unique())
                    )
                    
                    if selected_city != "All Cities":
                        filtered_df = filtered_df[filtered_df['City'] == selected_city]
                        st.metric(f"Jumlah di {selected_city}", len(filtered_df))

        # Filtered data table
        st.markdown('<div class="section-title">📊 Data Tempat Wisata</div>', unsafe_allow_html=True)
        if 'filtered_df' in locals():
            display_columns = ['Place_Id', 'Place_Name', 'City', 'Category']
            # Add other available columns
            for col in ['Price', 'Rating', 'Description']:
                if col in filtered_df.columns:
                    display_columns.append(col)
            
            st.dataframe(
                filtered_df[display_columns].head(50),
                use_container_width=True
            )

    # =====================================================================================
    # 💼 ANALISIS PAKET WISATA
    # =====================================================================================
    elif selected_menu == "💼 Analisis Paket":
        st.markdown('<div class="main-title">💼 Analisis Paket Wisata</div>', unsafe_allow_html=True)
        
        if 'City' in package_df.columns:
            # Metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                metric_card("Total Paket", len(package_df))
            with col2:
                metric_card("Kota Tersedia", package_df['City'].nunique())
            with col3:
                # Hitung jumlah destinasi
                tempat_cols = [col for col in package_df.columns if any(keyword in col for keyword in ['Place', 'Tourism', 'Destinasi', 'Wisata'])]
                if tempat_cols:
                    avg_destinations = package_df[tempat_cols].notna().sum(axis=1).mean()
                    metric_card("Rata-rata Destinasi", f"{avg_destinations:.1f}")

            # Visualizations
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="section-title">🌆 Paket per Kota</div>', unsafe_allow_html=True)
                paket_kota = package_df['City'].value_counts()
                fig = px.pie(
                    values=paket_kota.values,
                    names=paket_kota.index,
                    title="Distribusi Paket Wisata per Kota",
                    hole=0.4
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown('<div class="section-title">🏝️ Jumlah Destinasi per Paket</div>', unsafe_allow_html=True)
                if tempat_cols:
                    package_df['Jumlah_Destinasi'] = package_df[tempat_cols].notna().sum(axis=1)
                    dest_count = package_df['Jumlah_Destinasi'].value_counts().sort_index()
                    
                    fig = px.bar(
                        x=dest_count.index,
                        y=dest_count.values,
                        title="Distribusi Jumlah Destinasi",
                        color=dest_count.values,
                        color_continuous_scale='Purples'
                    )
                    fig.update_layout(
                        xaxis_title="Jumlah Destinasi",
                        yaxis_title="Jumlah Paket"
                    )
                    st.plotly_chart(fig, use_container_width=True)

            # Data table
            st.markdown('<div class="section-title">📋 Daftar Paket Wisata</div>', unsafe_allow_html=True)
            st.dataframe(package_df, use_container_width=True)

    # =====================================================================================
    # 🌟 REKOMENDASI WISATA
    # =====================================================================================
    elif selected_menu == "🌟 Rekomendasi":
        st.markdown('<div class="main-title">🌟 Rekomendasi Tempat Wisata Terbaik</div>', unsafe_allow_html=True)
        
        # Cari kolom rating
        rating_column = None
        for col in rating_df.columns:
            if 'rating' in col.lower() or 'Rating' in col:
                rating_column = col
                break

        if rating_column and 'Category' in tourism_df.columns:
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown('<div class="section-title">🎯 Pilihan Kategori</div>', unsafe_allow_html=True)
                pilih_kategori = st.selectbox(
                    "Pilih kategori wisata:",
                    sorted(tourism_df['Category'].unique())
                )
                
                # Additional filters
                if 'City' in tourism_df.columns:
                    selected_city = st.selectbox(
                        "Filter by Kota:",
                        ["All Cities"] + sorted(tourism_df['City'].unique())
                    )
                
                st.markdown("""
                <div style="background: #e8f4f8; padding: 15px; border-radius: 8px; border-left: 4px solid #2E8BC0;">
                    <h4 style="margin: 0 0 10px 0; color: #145DA0;">💡 Tips</h4>
                    <p style="margin: 0; font-size: 0.9rem; color: #555;">
                    Rekomendasi berdasarkan rating tertinggi dari pengguna. Pilih kategori untuk melihat tempat terbaik.
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                # Get recommendations
                top_wisata = (
                    rating_df.groupby('Place_Id')[rating_column].mean()
                    .reset_index()
                    .merge(tourism_df, on='Place_Id')
                )
                top_wisata = top_wisata[top_wisata['Category'] == pilih_kategori]
                
                # Apply city filter if selected
                if 'selected_city' in locals() and selected_city != "All Cities":
                    top_wisata = top_wisata[top_wisata['City'] == selected_city]
                
                top_wisata = top_wisata.rename(columns={rating_column: 'Place_Ratings'})
                top_wisata = top_wisata.sort_values('Place_Ratings', ascending=False).head(10)

                if not top_wisata.empty:
                    st.markdown(f'<div class="section-title">🏅 Top 10 {pilih_kategori}</div>', unsafe_allow_html=True)
                    
                    # Display as cards
                    for idx, row in top_wisata.head(5).iterrows():
                        with st.container():
                            st.markdown(f"""
                            <div style="background: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin: 10px 0; border-left: 4px solid #2E8BC0;">
                                <div style="display: flex; justify-content: between; align-items: center;">
                                    <h4 style="margin: 0; color: #145DA0;">{row['Place_Name']}</h4>
                                    <span style="background: #2E8BC0; color: white; padding: 5px 10px; border-radius: 15px; font-size: 0.8rem;">
                                        ⭐ {row['Place_Ratings']:.2f}
                                    </span>
                                </div>
                                <p style="margin: 5px 0; color: #666; font-size: 0.9rem;">
                                    <strong>Kota:</strong> {row['City']} | <strong>Kategori:</strong> {row['Category']}
                                </p>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    # Chart for the top recommendations
                    fig = px.bar(
                        top_wisata.head(5),
                        x='Place_Name',
                        y='Place_Ratings',
                        color='Place_Ratings',
                        color_continuous_scale='Viridis',
                        title=f"Top 5 {pilih_kategori} Berdasarkan Rating"
                    )
                    fig.update_layout(
                        xaxis_title="Tempat Wisata",
                        yaxis_title="Rating"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                else:
                    st.warning(f"Tidak ada data untuk kategori {pilih_kategori}")

    # =====================================================================================
    # 🗃️ DATA VIEWER
    # =====================================================================================
    elif selected_menu == "🗃️ Data Viewer":
        st.markdown('<div class="main-title">🗃️ Data Warehouse Viewer</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.markdown('<div class="section-title">📂 Pilih Tabel</div>', unsafe_allow_html=True)
            pilihan = st.selectbox(
                "Pilih tabel yang ingin ditampilkan:",
                ["tourism_with_id", "tourism_rating", "users", "package_tourism"]
            )
            
            st.markdown("""
            <div style="background: #fff3cd; padding: 15px; border-radius: 8px; border-left: 4px solid #ffc107;">
                <h4 style="margin: 0 0 10px 0; color: #856404;">ℹ️ Informasi</h4>
                <p style="margin: 0; font-size: 0.9rem; color: #856404;">
                Tampilkan data mentah dari warehouse untuk analisis detail.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            df_map = {
                "tourism_with_id": tourism_df,
                "tourism_rating": rating_df,
                "users": user_df,
                "package_tourism": package_df
            }

            selected_df = df_map[pilihan]
            
            st.markdown(f'<div class="section-title">📊 Tabel: {pilihan}</div>', unsafe_allow_html=True)
            st.write(f"**Jumlah Record:** {len(selected_df)}")
            
            # Search functionality
            search_term = st.text_input("🔍 Cari data...")
            if search_term:
                # Search in all string columns
                mask = selected_df.astype(str).apply(lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)
                filtered_df = selected_df[mask]
                st.write(f"**Hasil pencarian:** {len(filtered_df)} record ditemukan")
                st.dataframe(filtered_df, use_container_width=True)
            else:
                st.dataframe(selected_df, use_container_width=True)

if __name__ == "__main__":
    main()