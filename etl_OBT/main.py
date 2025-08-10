# etl/main.py

from config import RAW_CSV
from clean import clean_all
from transform import build_final_df
from load import get_engine, load_dataframe

def main():
    # 1️⃣ Clean & parse your CSV
    df = clean_all(RAW_CSV)

    # 2️⃣ Build the final wide DataFrame
    load_df = build_final_df(df)

    # 3️⃣ Push into Postgres one shot
    engine = get_engine()
    load_dataframe(load_df, table_name='recipes_array', engine=engine)

    print("✅ ETL complete!")

if __name__ == "__main__":
    main()
