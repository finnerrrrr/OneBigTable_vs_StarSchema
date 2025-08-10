# etl/transform.py
import pandas as pd

def build_users(df: pd.DataFrame) -> pd.DataFrame:
    return df[['user_id']].drop_duplicates()

def build_recipes(df: pd.DataFrame) -> pd.DataFrame:
    return (
      df.rename(columns={'id':'recipe_id'})[[
        'recipe_id','user_id','version_no','name','description',
        'created_at','updated_at','runnable','running',
        'job_succeeded_count','job_failed_count','parent_id'
      ]]
    )

def build_apps(df: pd.DataFrame) -> pd.DataFrame:
    apps = (
      pd.DataFrame(df['applications_list'].explode(), columns=['name'])
        .drop_duplicates()
        .reset_index(drop=True)
    )
    apps['app_id'] = 'app_' + apps.index.astype(str)
    return apps

def build_cats(df: pd.DataFrame) -> pd.DataFrame:
    cats = (
      pd.DataFrame(df['categories_list'].explode(), columns=['name'])
        .drop_duplicates()
        .reset_index(drop=True)
    )
    cats['category_id'] = 'cat_' + cats.index.astype(str)
    return cats

def build_objs(df: pd.DataFrame) -> pd.DataFrame:
    objs = (
      pd.DataFrame(df['business_objects_list'].explode(), columns=['name'])
        .drop_duplicates()
        .reset_index(drop=True)
    )
    objs['obj_id'] = 'obj_' + objs.index.astype(str)
    return objs

def build_recipe_app_bridge(df: pd.DataFrame, apps_df: pd.DataFrame) -> pd.DataFrame:
    return (
      df[['id','applications_list']]
        .explode('applications_list')
        .rename(columns={'id':'recipe_id','applications_list':'app_name'})
        .merge(apps_df, how='left', left_on='app_name', right_on='name')
        [['recipe_id','app_id']]
    )

def build_app_obj_bridge(df: pd.DataFrame, apps_df: pd.DataFrame, objs_df: pd.DataFrame) -> pd.DataFrame:
    return (
      df[['applications_list','business_objects_list']]
        .explode('applications_list')
        .explode('business_objects_list')
        .rename(columns={'applications_list':'app_name','business_objects_list':'obj_name'})
        .merge(apps_df, how='left', left_on='app_name', right_on='name')
        .merge(objs_df, how='left', left_on='obj_name', right_on='name')
        [['app_id','obj_id']]
    )

def build_app_cat_bridge(df: pd.DataFrame, apps_df: pd.DataFrame, cats_df: pd.DataFrame) -> pd.DataFrame:
    return (
      df[['applications_list','categories_list']]
        .explode('applications_list')
        .explode('categories_list')
        .rename(columns={'applications_list':'app_name','categories_list':'cat_name'})
        .merge(apps_df, how='left', left_on='app_name', right_on='name')
        .merge(cats_df, how='left', left_on='cat_name', right_on='name')
        [['app_id','category_id']]
    )
