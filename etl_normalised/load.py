# etl/load.py

import os
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

# -------------------------------------------------------------------
# Configuration: read the database URL from an environment variable
# -------------------------------------------------------------------
DB_URL = os.getenv('DB_URL', 'postgresql://user:pass@localhost:5432/mydb')

def get_engine(db_url: str = DB_URL):
    """
    Create and return a SQLAlchemy engine.
    """
    return create_engine(db_url)

def load_dataframe(
    df,
    table_name: str,
    engine,
    if_exists: str = 'append',
    chunksize: int = 1000
):
    """
    Write a pandas DataFrame to the given table using SQLAlchemy.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame to load.
    table_name : str
        The target table name in the database.
    engine : sqlalchemy.Engine
        The SQLAlchemy engine.
    if_exists : {'fail', 'replace', 'append'}, default 'append'
        Behavior when the table already exists.
    chunksize : int, default 1000
        Number of rows to write at a time (helps with large DataFrames).

    Raises
    ------
    SQLAlchemyError
        If the to_sql call fails.
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

def load_all(dfs: dict):
    """
    Given a dict of {'table_name': DataFrame}, load each to the database.
    """
    engine = get_engine()
    for table, df in dfs.items():
        load_dataframe(df, table, engine)

if __name__ == "__main__":
    from transform import (
        build_users, build_recipes, build_apps,
        build_cats, build_objs,
        build_recipe_app_bridge,
        build_app_obj_bridge, build_app_cat_bridge
    )
    from clean import clean
    from config import RAW_CSV

    # 1) Clean & transform
    df = clean(RAW_CSV)
    users_df   = build_users(df)
    recipes_df = build_recipes(df)
    apps_df    = build_apps(df)
    cats_df    = build_cats(df)
    objs_df    = build_objs(df)
    rab_df     = build_recipe_app_bridge(df, apps_df)
    aob_df     = build_app_obj_bridge(df, apps_df, objs_df)
    acb_df     = build_app_cat_bridge(df, apps_df, cats_df)

    # 2) Load everything
    tables = {
        'users':                    users_df,
        'recipe':                   recipes_df,
        'application':              apps_df,
        'category':                 cats_df,
        'business_obj':             objs_df,
        'recipe_application_bridge':rab_df,
        'application_obj_bridge':   aob_df,
        'application_cat_bridge':   acb_df,
    }
    load_all(tables)
