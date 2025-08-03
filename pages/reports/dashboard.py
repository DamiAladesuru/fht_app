# --- dashboard.py ---
import streamlit as st
import pandas as pd

from src.visualize import plot_ingredient_trend, plot_relationship_scatter
from src.datacleaning import clean_food_items
from src.ner_utils import check_symptom_present
from src.gsheets_utils import load_gsheet_data

st.title("📊 Health Tracker Reports")

# Load data from Google Sheets
try:
    df = load_gsheet_data()
except Exception as e:
    st.error("❌ Could not load data from Google Sheets.")
    st.exception(e)
    st.stop()


analysis_type = st.selectbox("Choose variable type to analyze", ["Food", "Gut", "Period"])

if analysis_type == "Food":
    st.subheader("Trend Analysis")
    ingredient = st.text_input("Enter food item to analyze (e.g. milk)", value="milk", key="food_trend")
    if st.button("Show bar plot of days with ingredient", key="food_trend_btn"):
        fig_bar = plot_ingredient_trend(df, ingredient)
        st.pyplot(fig_bar)


st.subheader("Relationship Analysis")
# Select first column
first_column = st.selectbox("Choose first column", df.columns, key="rel_first_col")

# Get unique original-cased values deduped case-insensitive from first_column
def get_unique_original_values(series):
    seen = {}
    for val in series.dropna():
        val_str = str(val).strip()
        val_lower = val_str.lower()
        if val_lower and val_lower not in seen:
            seen[val_lower] = val_str
    return [seen[k] for k in sorted(seen)]

first_values = get_unique_original_values(df[first_column])

if first_values:
    default_first = first_values[0]  # or any logic to set a default
    first_value = st.selectbox(
        f"Value from {first_column} to check",
        first_values,
        index=0,
        key="rel_first_value"
    )
else:
    st.info(f"No valid values found in {first_column}")
    first_value = None

# Select second column
second_column = st.selectbox("Choose second column", df.columns, key="rel_second_col")

# Get unique original-cased values from second_column similarly
second_values = get_unique_original_values(df[second_column])

if second_values:
    default_second = second_values[0]
    second_value = st.selectbox(
        f"Value from {second_column} to check",
        second_values,
        index=0,
        key="rel_second_value"
    )
else:
    st.info(f"No valid values found in {second_column}")
    second_value = None

# Proceed to perform analysis only if valid selections
if first_value and second_value:
    if st.button("Show relationship scatterplot"):
        # Your plotting function should be adapted to accept columns and values for filtering,
        # e.g., filter df where first_column == first_value AND second_column == second_value (case-insensitive)
        fig = plot_relationship_scatter(df, first_column, first_value, second_column, second_value)
        st.pyplot(fig)
else:
    st.warning("Please select valid values from both columns.")
