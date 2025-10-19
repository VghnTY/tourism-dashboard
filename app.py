import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- Konfigurasi halaman
st.set_page_config(
    page_title="Tourism Data Warehouse",
    layout="wide",
    page_icon="🏝️"
)

# --- Load data langsung dari CSV files
@st.cache_data
def load_data():
    """Load data langsung dari CSV files"""
    try:
        # Load dari CSV files
        tourism_df = pd.read_csv("data/tourism_with_id.csv")
        rating_df = pd.read_csv("data/tourism_rating.csv")
        user_df = pd.read_csv("data/user.csv")
        package_df = pd.read_csv("data/package_tourism.csv")
        
        st.sidebar.success("✅ Data loaded from CSV files")
        return tourism_df, rating_df, user_df, package_df
        
    except Exception as e:
        st.error(f"❌ Error loading CSV files: {e}")
        # Fallback ke sample data
        return load_sample_data()

def load_sample_data():
    """Sample data jika CSV tidak ada"""
    st.sidebar.warning("⚠️ Using sample data")
    
    # Sample data yang lebih lengkap
    sample_tourism = pd.DataFrame({
        'Place_Id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'Place_Name': ['Monas Jakarta', 'Taman Mini Indonesia Indah', 'Ancol Dreamland', 
                      'Candi Borobudur', 'Tanah Lot Bali', 'Prambanan', 
                      'Kuta Beach Bali', 'Malioboro Yogyakarta', 'Braga Street Bandung', 'Bunaken Manado'],
        'Category': ['Budaya', 'Taman Hiburan', 'Taman Hiburan', 'Budaya', 'Cagar Alam',
                    'Budaya', 'Bahari', 'Budaya', 'Budaya', 'Bahari'],
        'City': ['Jakarta', 'Jakarta', 'Jakarta', 'Magelang', 'Bali', 
                'Yogyakarta', 'Bali', 'Yogyakarta', 'Bandung', 'Manado'],
        'Price': [10000, 20000, 15000, 50000, 75000, 45000, 0, 0, 0, 100000],
        'Rating': [4.5, 4.2, 4.7, 4.8, 4.6, 4.5, 4.3, 4.4, 4.1, 4.9],
        'Description': [
            'Monumen Nasional icon Jakarta',
            'Taman rekreasi dan budaya Indonesia',
            'Wisata pantai dan hiburan keluarga', 
            'Candi Buddha terbesar di dunia',
            'Pura indah di atas laut Bali',
            'Kompleks candi Hindu terbesar',
            'Pantai populer untuk surfing dan sunset',
            'Jalan shopping terkenal di Jogja',
            'Jalan historik dengan arsitektur Belanda',
            'Taman laut dengan biodiversitas tinggi'
        ]
    })
    
    sample_rating = pd.DataFrame({
        'User_Id': [1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'Place_Id': [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 7, 8, 9, 10],
        'Place_Ratings': [4.5, 4.0, 4.2, 4.5, 4.7, 4.8, 4.8, 4.9, 4.6, 4.5, 4.5, 4.3, 4.4, 4.1, 4.9]
    })
    
    sample_user = pd.DataFrame({
        'User_Id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'Location': ['Jakarta', 'Bandung', 'Surabaya', 'Yogyakarta', 'Denpasar', 
                    'Medan', 'Makassar', 'Semarang', 'Malang', 'Manado'],
        'Age': [25, 30, 28, 35, 27, 32, 29, 31, 26, 33]
    })
    
    sample_package = pd.DataFrame({
        'Package_Id': [1, 2, 3, 4, 5],
        'Package_Name': ['Paket Wisata Jakarta', 'Paket Wisata Jogja', 'Paket Wisata Bali', 
                        'Paket Wisata Bandung', 'Paket Wisata Manado'],
        'City': ['Jakarta', 'Yogyakarta', 'Bali', 'Bandung', 'Manado'],
        'Place_Tourism_1': ['Monas Jakarta', 'Candi Borobudur', 'Tanah Lot Bali', 'Braga Street', 'Bunaken'],
        'Place_Tourism_2': ['Taman Mini', 'Malioboro', 'Uluwatu Temple', 'Tangkuban Perahu', 'Manado Tua'],
        'Place_Tourism_3': ['Ancol', 'Prambanan', 'Kuta Beach', 'Kawah Putih', 'Linow Lake']
    })
    
    return sample_tourism, sample_rating, sample_user, sample_package

# --- Custom CSS
st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    [data-testid="stSidebar"] { 
        background: linear-gradient(180deg, #2E8BC0 0%, #145DA0 100%); 
    }
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
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #2E8BC0;
        margin-bottom: 10px;
    }
    .stButton button {
        background: linear-gradient(45deg, #2E8BC0, #145DA0);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Load data
    tourism_df, rating_df, user_df, package_df = load_data()
    
    # --- Sidebar Navigation
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h1 style="color: white; font-size: 24px; margin-bottom: 5px;">🏝️</h1>
        <h2 style="color: white; font-size: 18px; font-weight: 700;">Tourism Data Warehouse</h2>
        <p style="color: #d9e6f2; font-size: 12px;">Analisis Data Pariwisata</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    
    menu_options = [
        "🏠 Dashboard Utama",
        "⭐ Analisis Rating", 
        "🏙️ Analisis Wisata",
        "💼 Analisis Paket",
        "🌟 Rekomendasi",
        "🗃️ Data Viewer"
    ]
    
    selected_menu = st.sidebar.radio("**NAVIGASI**", menu_options, label_visibility="collapsed")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <div style="color: #d9e6f2; font-size: 12px; text-align: center;">
        <p><strong>Kelompok 1</strong></p>
        <p>Data Warehouse & Business Intelligence</p>
    </div>
    """, unsafe_allow_html=True)

    # =====================================================================================
    # 🏠 DASHBOARD UTAMA
    # =====================================================================================
    if selected_menu == "🏠 Dashboard Utama":
        st.markdown('<div class="main-title">📊 Tourism Analytics Dashboard</div>', unsafe_allow_html=True)
        
        st.info("🔍 **Data Source**: CSV Files - Real Tourism Data")
        
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Tempat Wisata", len(tourism_df))
        with col2:
            st.metric("Total Pengguna", len(user_df))
        with col3:
            st.metric("Total Paket Wisata", len(package_df))
        with col4:
            st.metric("Total Rating", len(rating_df))
        
        # Visualizations
        st.markdown('<div class="section-title">📈 Visualisasi Data</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Grafik kategori wisata
            if 'Category' in tourism_df.columns:
                category_counts = tourism_df['Category'].value_counts()
                fig1 = px.pie(
                    values=category_counts.values,
                    names=category_counts.index,
                    title="Distribusi Kategori Wisata",
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Grafik kota
            if 'City' in tourism_df.columns:
                city_counts = tourism_df['City'].value_counts().head(10)
                fig2 = px.bar(
                    x=city_counts.values,
                    y=city_counts.index,
                    orientation='h',
                    title="Top 10 Kota dengan Wisata Terbanyak",
                    color=city_counts.values,
                    color_continuous_scale='Blues'
                )
                fig2.update_layout(
                    xaxis_title="Jumlah Wisata",
                    yaxis_title="Kota"
                )
                st.plotly_chart(fig2, use_container_width=True)

        # Row 2
        col1, col2 = st.columns(2)
        
        with col1:
            # Rating distribution
            if 'Rating' in tourism_df.columns:
                fig3 = px.histogram(
                    tourism_df,
                    x='Rating',
                    nbins=10,
                    title="Distribusi Rating Tempat Wisata",
                    color_discrete_sequence=['#2E8BC0']
                )
                st.plotly_chart(fig3, use_container_width=True)
        
        with col2:
            # Package distribution
            if 'City' in package_df.columns:
                package_city = package_df['City'].value_counts()
                fig4 = px.bar(
                    x=package_city.index,
                    y=package_city.values,
                    title="Paket Wisata per Kota",
                    color=package_city.values,
                    color_continuous_scale='Viridis'
                )
                fig4.update_layout(
                    xaxis_title="Kota",
                    yaxis_title="Jumlah Paket"
                )
                st.plotly_chart(fig4, use_container_width=True)

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
                st.metric("Rating Tertinggi", f"{avg_rating['Place_Ratings'].max():.2f}")
                st.metric("Rating Terendah", f"{avg_rating['Place_Ratings'].min():.2f}")
                st.metric("Rating Rata-rata", f"{avg_rating['Place_Ratings'].mean():.2f}")

            # Data table
            st.markdown('<div class="section-title">📋 Data Detail Top 20</div>', unsafe_allow_html=True)
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
                st.metric("Total Paket", len(package_df))
            with col2:
                st.metric("Kota Tersedia", package_df['City'].nunique())
            with col3:
                # Hitung jumlah destinasi
                tempat_cols = [col for col in package_df.columns if any(keyword in col for keyword in ['Place', 'Tourism', 'Destinasi', 'Wisata'])]
                if tempat_cols:
                    avg_destinations = package_df[tempat_cols].notna().sum(axis=1).mean()
                    st.metric("Rata-rata Destinasi", f"{avg_destinations:.1f}")

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
                st.markdown('<div class="section-title">🎯 Pilihan Filter</div>', unsafe_allow_html=True)
                pilih_kategori = st.selectbox(
                    "Pilih kategori wisata:",
                    sorted(tourism_df['Category'].unique())
                )
                
                # Additional filters
                if 'City' in tourism_df.columns:
                    selected_city = st.selectbox(
                        "Filter by Kota:",
                        ["Semua Kota"] + sorted(tourism_df['City'].unique())
                    )
                
                st.markdown("""
                <div style="background: #e8f4f8; padding: 15px; border-radius: 8px; border-left: 4px solid #2E8BC0;">
                    <h4 style="margin: 0 0 10px 0; color: #145DA0;">💡 Tips</h4>
                    <p style="margin: 0; font-size: 0.9rem; color: #555;">
                    Rekomendasi berdasarkan rating tertinggi dari data CSV.
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
                if 'selected_city' in locals() and selected_city != "Semua Kota":
                    top_wisata = top_wisata[top_wisata['City'] == selected_city]
                
                top_wisata = top_wisata.rename(columns={rating_column: 'Place_Ratings'})
                top_wisata = top_wisata.sort_values('Place_Ratings', ascending=False).head(10)

                if not top_wisata.empty:
                    st.markdown(f'<div class="section-title">🏅 Top Rekomendasi {pilih_kategori}</div>', unsafe_allow_html=True)
                    
                    # Display as cards
                    for idx, row in top_wisata.head(5).iterrows():
                        with st.container():
                            st.markdown(f"""
                            <div style="background: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin: 10px 0; border-left: 4px solid #2E8BC0;">
                                <div style="display: flex; justify-content: space-between; align-items: center;">
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
            st.markdown('<div class="section-title">📂 Pilih Data</div>', unsafe_allow_html=True)
            pilihan = st.selectbox(
                "Pilih dataset:",
                ["Tempat Wisata", "Data Rating", "Data User", "Paket Wisata"]
            )
            
            st.markdown("""
            <div style="background: #fff3cd; padding: 15px; border-radius: 8px; border-left: 4px solid #ffc107;">
                <h4 style="margin: 0 0 10px 0; color: #856404;">ℹ️ Informasi</h4>
                <p style="margin: 0; font-size: 0.9rem; color: #856404;">
                Data di-load langsung dari file CSV.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            df_map = {
                "Tempat Wisata": tourism_df,
                "Data Rating": rating_df,
                "Data User": user_df,
                "Paket Wisata": package_df
            }

            selected_df = df_map[pilihan]
            
            st.markdown(f'<div class="section-title">📊 Dataset: {pilihan}</div>', unsafe_allow_html=True)
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