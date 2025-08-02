# --- 3. visualize.py ---
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from src.datacleaning import clean_food_items, gut_period_keys
from src.ner_utils import check_symptom_present, check_key_present


def count_days_with_ingredient(df, ingredient):
    df = clean_food_items(df)
    df["has_ingredient"] = df["ingredients"].apply(lambda x: ingredient.lower() in x)
    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.to_period("M")
    return df[df["has_ingredient"]].groupby("Month")["Date"].nunique()

def plot_ingredient_trend(df, ingredient):
    trend = count_days_with_ingredient(df, ingredient)
    fig, ax = plt.subplots()
    trend.plot(kind="bar", ax=ax, title=f"Days with {ingredient.title()} per Month")
    ax.set_ylabel("Days")
    ax.set_xlabel("Month")
    fig.tight_layout()
    return fig

def plot_relationship_scatter(df, col1, val1, col2, val2):
    """
    Plot a scatterplot showing days and months where rows have both
    selected values in their respective columns.

    Args:
        df (pd.DataFrame): The data frame with at least columns col1 and col2 and a 'Date' column.
        col1 (str): Name of the first column.
        val1 (str): Value to filter in the first column (case-insensitive).
        col2 (str): Name of the second column.
        val2 (str): Value to filter in the second column (case-insensitive).

    Returns:
        matplotlib.figure.Figure: The generated scatter plot figure.
    """
    # Normalize case & trim if values or columns have string content
    df_filtered = df[
        df[col1].astype(str).str.strip().str.lower() == val1.lower()
    ].copy()

    df_filtered = df_filtered[
        df_filtered[col2].astype(str).str.strip().str.lower() == val2.lower()
    ].copy()

    if df_filtered.empty:
        # Create empty plot with message
        fig, ax = plt.subplots(figsize=(8,5))
        ax.text(0.5, 0.5, "No data matching selected values", ha='center', va='center')
        ax.axis('off')
        return fig

    # Parse Date column to datetime if not already
    if not pd.api.types.is_datetime64_any_dtype(df_filtered["Date"]):
        df_filtered["Date"] = pd.to_datetime(df_filtered["Date"])

    df_filtered["Day"] = df_filtered["Date"].dt.day
    df_filtered["Month"] = df_filtered["Date"].dt.strftime("%Y-%m")

    fig, ax = plt.subplots(figsize=(8,5))
    sns.scatterplot(
        data=df_filtered,
        x="Day",
        y="Month",
        color="green",
        s=100,
        ax=ax
    )
    ax.set_xlabel("Day of Month")
    ax.set_ylabel("Month")
    ax.set_title(f"Occurrences of {col1}: {val1} AND {col2}: {val2}")
    fig.tight_layout()
    return fig