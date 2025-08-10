# etl/clean.py
import pandas as pd

def read_and_coerce(raw_csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(raw_csv_path)

    # parse dates
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['updated_at'] = pd.to_datetime(df['updated_at'])

    # keep parent_id as string (preserve nulls)
    df['parent_id'] = df['parent_id'].astype(pd.StringDtype())

    return df

def explode_lists(df: pd.DataFrame) -> pd.DataFrame:
    # applications
    df['applications_list'] = (
      df['applications']
        .str.strip('{}')
        .str.split(';')
        .apply(lambda lst: sorted({x.strip() for x in lst if x.strip()}))
    )

    # categories
    df['categories_list'] = (
      df['categories']
        .str.strip('{}')
        .str.split(',')
        .apply(lambda lst: sorted({x.strip() for x in lst if x.strip()}))
    )

    # business objects (flat strings)
    df['business_objects_list'] = (
      df['business_objects']
        .str.strip('{}')
        .str.split(',')
        .apply(lambda lst: sorted({x.strip() for x in lst if x.strip()}))
    )

    return df

def clean(raw_csv_path: str) -> pd.DataFrame:
    df = read_and_coerce(raw_csv_path)
    df = explode_lists(df)
    return df
