# data cleaning
import pandas as pd
from src.ner_utils import extract_ingredients
from src.ner_utils import extract_gut_period_keys

# Known food synonyms mapping (extend this as needed)
FOOD_SYNONYMS = {
    "milch": "milk",
    "oatmilk": "milk",
    "schoko": "chocolate",
    "schokomuesli": "müsli",
    "schokomüsli": "müsli",
    "musli": "müsli",
    "muesli": "müsli",
    "haferflocken": "oats",
    "hafer": "oats",
    "brot": "bread",
    "broetchen": "bread",
    "brötchen": "bread",
}

def clean_food_items(df):
    df = df.copy()
    df["food_item_clean"] = df["Food Item"].fillna("").str.lower()
    df["food_item_clean"] = df["food_item_clean"].replace(FOOD_SYNONYMS, regex=True)
    df["ingredients"] = df["food_item_clean"].apply(extract_ingredients)
    return df

def gut_period_keys(df):
    df['keys'] = df.apply(extract_gut_period_keys, axis=1)
    return df