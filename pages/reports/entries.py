import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.title("All Entries")

# --- Load from Google Sheet ---
#@st.cache_data
def load_gsheet_data():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(
        st.secrets["gcp_service_account"],
        scopes=scope
    )
    client = gspread.authorize(creds)
    sheet = client.open("fh tracker").sheet1
    records = sheet.get_all_records()
    return pd.DataFrame(records)

try:
    df = load_gsheet_data()
except Exception as e:
    st.error("⚠️ Could not load data from Google Sheets.")
    st.exception(e)
    st.stop()

# Clean and show
columns_to_show = [
    'Date', 'Day Type', 'Work Day/Weekend',
    'Meal Type', 'Meal Time', 'Item Class', 'Food Item',
    'Energy Level', 'Stress Level', 'Activity Type',
    'Gut Feeling', 'Bristol Type', 'Gut State',
    'Period Day', 'Hygiene Product', 'Menstrual Flow', 'Cramp Level',
    'Acne/Skin', 'Notes'
]

st.dataframe(df[columns_to_show])
