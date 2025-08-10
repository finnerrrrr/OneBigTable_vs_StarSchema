
from config import RAW_CSV
from clean import clean
from transform import (
    build_users, build_recipes, build_apps,
    build_cats, build_objs,
    build_recipe_app_bridge,
    build_app_obj_bridge,
    build_app_cat_bridge
)
# ① import the helper that bulk‐loads a dict of tables…
from load import load_all

def main():
    df = clean(RAW_CSV)

    users_df   = build_users(df)
    recipes_df = build_recipes(df)
    apps_df    = build_apps(df)
    cats_df    = build_cats(df)
    objs_df    = build_objs(df)

    rab_df = build_recipe_app_bridge(df, apps_df)
    aob_df = build_app_obj_bridge(df, apps_df, objs_df)
    acb_df = build_app_cat_bridge(df, apps_df, cats_df)

    tables = {
        'users':                     users_df,
        'recipe':                    recipes_df,
        'application':               apps_df,
        'category':                  cats_df,
        'business_obj':              objs_df,
        'recipe_application_bridge': rab_df,
        'application_obj_bridge':    aob_df,
        'application_cat_bridge':    acb_df,
    }
    load_all(tables)


    print("✅ ETL complete!")

if __name__ == "__main__":
    main()