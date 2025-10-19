import pandas as pd
from sqlalchemy import create_engine, inspect
import os

def run_etl():
    print("🚀 Memulai proses ETL...")
    
    # === 1. EXTRACT ===
    print("📥 Extract: Membaca file CSV...")
    try:
        package_df = pd.read_csv(r"C:\bahan tbd\package_tourism.csv")
        rating_df = pd.read_csv(r"C:\bahan tbd\tourism_rating.csv")
        tourism_df = pd.read_csv(r"C:\bahan tbd\tourism_with_id.csv")
        user_df = pd.read_csv(r"C:\bahan tbd\user.csv")
        
        print(f"   ✅ package_tourism: {len(package_df)} records")
        print(f"   ✅ tourism_rating: {len(rating_df)} records")
        print(f"   ✅ tourism_with_id: {len(tourism_df)} records")
        print(f"   ✅ user: {len(user_df)} records")
        
    except Exception as e:
        print(f"❌ Error membaca file CSV: {e}")
        return

    # === 2. TRANSFORM ===
    print("🔄 Transform: Memproses data...")
    
    # Pastikan kolom yang diperlukan ada
    print("   Kolom tourism_rating:", list(rating_df.columns))
    print("   Kolom user:", list(user_df.columns))
    print("   Kolom tourism_with_id:", list(tourism_df.columns))
    
    # Gabungkan data
    try:
        merged_df = rating_df.merge(user_df, on="User_Id", how="left") \
                             .merge(tourism_df, on="Place_Id", how="left")
        
        # Hitung rata-rata rating
        avg_rating = merged_df.groupby(['Place_Id', 'Place_Name'])['Rating'].mean().reset_index()
        avg_rating.rename(columns={'Rating': 'avg_rating'}, inplace=True)
        
        # Gabungkan dengan package
        warehouse_df = package_df.merge(avg_rating, left_on="Package", right_on="Place_Id", how="left")
        
        print("   ✅ Transformasi data berhasil")
        
    except Exception as e:
        print(f"❌ Error transformasi data: {e}")
        return

    # === 3. LOAD ===
    print("📤 Load: Menyimpan ke PostgreSQL...")
    
    # Konfigurasi database - SESUAIKAN PASSWORD
    DB_USER = "postgres"
    DB_PASSWORD = "vaughn"  # GANTI dengan password PostgreSQL Anda
    DB_HOST = "localhost"
    DB_PORT = "5432"
    DB_NAME = "tourism_warehouse"

    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(DATABASE_URL)

    try:
        # Test koneksi
        with engine.connect() as conn:
            print("   ✅ Terhubung ke PostgreSQL")
        
        # Simpan semua tabel
        print("   💾 Menyimpan package_tourism...")
        package_df.to_sql("package_tourism", con=engine, if_exists="replace", index=False)
        
        print("   💾 Menyimpan tourism_rating...")
        rating_df.to_sql("tourism_rating", con=engine, if_exists="replace", index=False)
        
        print("   💾 Menyimpan tourism_with_id...")
        tourism_df.to_sql("tourism_with_id", con=engine, if_exists="replace", index=False)
        
        print("   💾 Menyimpan users...")
        user_df.to_sql("users", con=engine, if_exists="replace", index=False)
        
        print("   💾 Menyimpan warehouse_tourism...")
        warehouse_df.to_sql("warehouse_tourism", con=engine, if_exists="replace", index=False)
        
        # Verifikasi
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"\n🎉 ETL Selesai! Tabel yang dibuat: {tables}")
        
        # Tampilkan jumlah data per tabel
        for table in tables:
            count = pd.read_sql(f"SELECT COUNT(*) as count FROM {table}", engine).iloc[0]['count']
            print(f"   📊 {table}: {count} records")
            
    except Exception as e:
        print(f"❌ Error menyimpan ke database: {e}")

if __name__ == "__main__":
    run_etl()