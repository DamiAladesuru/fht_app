import streamlit as st

# Pages
tracker = st.Page("pages/tracker.py", title="Tracker", icon=":material/edit:")
entries = st.Page("pages/reports/entries.py", title="Entries", icon=":material/table_chart:")
dashboard = st.Page("pages/reports/dashboard.py", title="Dashboard", icon=":material/dashboard:", default=True)

# Navigation
pg = st.navigation({
    "Log": [tracker],
    "Reports": [entries, dashboard],
})

pg.run()
