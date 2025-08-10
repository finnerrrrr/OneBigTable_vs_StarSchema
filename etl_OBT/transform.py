# etl/transform.py

import pandas as pd

def build_final_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Assemble the single wide DataFrame matching recipes_array schema.
    """
    # rename id → recipe_id and select your core columns
    load_df = df.rename(columns={'id':'recipe_id'})[[
        'recipe_id','user_id','version_no','name','description',
        'created_at','updated_at','runnable','running',
        'job_succeeded_count','job_failed_count','parent_id'
    ]].copy()

    # attach the list‐columns directly
    load_df['applications']     = df['applications_list']
    load_df['categories']       = df['categories_list']
    load_df['business_objects'] = df['business_objects_list']

    return load_df
