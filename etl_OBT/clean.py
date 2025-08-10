# etl/clean.py

import pandas as pd

def read_raw(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    # parse timestamps
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['updated_at'] = pd.to_datetime(df['updated_at'])
    # preserve nulls in parent_id
    df['parent_id']  = df['parent_id'].astype(pd.StringDtype())
    return df

def clean_multivalue_fields(df: pd.DataFrame) -> pd.DataFrame:
    """
    Turn your delimited strings into Python lists of unique, stripped values.
    """
    df['applications_list'] = (
        df['applications']
          .str.strip('{}')
          .str.split(';')
          .apply(lambda lst: sorted({x.strip() for x in lst if x.strip()}))
    )

    df['categories_list'] = (
        df['categories']
          .str.strip('{}')
          .str.split(',')
          .apply(lambda lst: sorted({x.strip() for x in lst if x.strip()}))
    )

    df['business_objects_list'] = (
        df['business_objects']
          .str.strip('{}')
          .str.split(',')
          .apply(lambda lst: sorted({x.strip() for x in lst if x.strip()}))
    )

    return df

def clean_all(path: str) -> pd.DataFrame:
    """
    Read raw CSV and apply all cleaning steps.
    """
    df = read_raw(path)
    df = clean_multivalue_fields(df)
    return df
