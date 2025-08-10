# etl/load.py

import os
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

# read from config or fallback
DB_URL = os.getenv('DB_URL', 'postgresql://user:pass@localhost:5432/mydb')

def get_engine(db_url: str = DB_URL):
    """Create and return a SQLAlchemy engine."""
    return create_engine(db_url)

def load_dataframe(
    df,
    table_name: str,
    engine,
    if_exists: str = 'append',
    chunksize: int = 1000
):
    """
    Bulk‐load a pandas DataFrame into a single table.
    """
    try:
        df.to_sql(
            name=table_name,
            con=engine,
            if_exists=if_exists,
            index=False,
            method='multi',
            chunksize=chunksize
        )
        print(f"[OK]   Loaded {len(df)} rows into `{table_name}`")
    except SQLAlchemyError as e:
        print(f"[ERROR] Failed to load `{table_name}`: {e}")
        raise
