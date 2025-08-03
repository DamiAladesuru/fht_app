import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from src.gsheets_utils import load_gsheet_data

st.title("All Entries")

# --- Load from Google Sheet ---
try:
    df = load_gsheet_data()
except Exception as e:
    st.error("⚠️ Could not load data from Google Sheets.")
    st.exception(e)
    st.stop()

# Clean and show
columns_to_show = [
    'Date', 'Day Type', 'Work Day/Weekend',
    'Meal Type', 'Meal Time', 'Item Class', 'Food',
    'Energy Level', 'Stress Level', 'Activity Type',
    'Gut Feeling', 'Bristol Type', 'Gut State',
    'Period Day', 'Hygiene Product', 'Menstrual Flow', 'Cramp Level',
    'Acne/Skin', 'Notes'
]

st.dataframe(df[columns_to_show])
