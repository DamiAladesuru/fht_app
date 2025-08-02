# 1. ner_utils.py - Named Entity Recognition helper for food items
# You will need to install spaCy and download a model: `python -m spacy download en_core_web_sm`
import pandas as pd
import spacy
nlp = spacy.load("en_core_web_sm")

def extract_ingredients(text):
    doc = nlp(text.lower())
    ingredients = [ent.text for ent in doc.ents if ent.label_ in ["FOOD", "PRODUCT", "NOUN"]]
    keywords = [token.text for token in doc if token.pos_ in ["NOUN"] and len(token.text) > 2]
    return list(set(ingredients + keywords))

def extract_gut_period_keys(row):
    columns = [
        'Energy Level', 'Stress Level', 'Activity Type',
        'Gut Feeling', 'Bristol Type', 'Gut State',
        'Period Day', 'Hygiene Product', 'Menstrual Flow', 'Cramp Level',
        'Acne/Skin'
    ]
    keys = set()
    for col in columns:
        val = row.get(col)
        if isinstance(val, list):
            keys.update([str(v) for v in val if v])
        elif pd.notna(val):
            keys.add(str(val))
    return keys

def check_symptom_present(series, keyword):
    """Check if keyword is present in a string series (case-insensitive, handles non-strings)."""
    return series.fillna("").astype(str).str.lower().str.contains(keyword.lower())

def check_key_present(key_set_series, keyword):
    """Check if keyword is in each set in the series (case-insensitive)."""
    return key_set_series.apply(lambda keys: keyword.lower() in [k.lower() for k in keys] if isinstance(keys, (list, set)) else False)
