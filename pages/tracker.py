import streamlit as st
import pandas as pd
from datetime import datetime
import os
import re
from src.gsheets_utils import save_to_gsheet

st.title("My Food-Health Log")

# Set column headers (needed to render table correctly even without data load)
column_headers = [
    'Date', 'Day Type', 'Work Day/Weekend', 'Meal Type', 'Meal Time', 'Item Class', 'Food',
    'Energy Level', 'Stress Level', 'Activity Type', 'Gut Feeling', 'Bowel Movement Frequency', 'Consistency',
    'Ease', 'Bristol Type', 'Gut State', 'Period Day', 'Hygiene Product', 'Menstrual Flow', 'Cramp Level',
    'Acne/Skin', 'Notes'
]


# Date and day info
date = datetime.today().strftime('%Y-%m-%d')
st.caption(f"{date}")
day_type = st.selectbox('Day Type', ['Normal Day', 'Period Day', 'Ovulation Day'])
work_or_weekend = st.selectbox('Work Day or Weekend', ['Work Day', 'Weekend/Free Day'])
    

# --- Meal Info and Raw Input ---
st.subheader("Log your meal")
meal_type = st.selectbox('Meal', ['', 'Breakfast', 'Lunch', 'Dinner', 'Snack', 'Other'])
meal_time = st.selectbox('Time', [
    '8:00 - 12:00',
    '12:00 - 16:00',
    '16:00 - 20:00',
    '20:00 - 24:00',
    '< 8:00'
])
item_class = st.selectbox('Item Class', ['', 'Food', 'Snack', 'Drink', 'Supplement', 'Medication'])

# Raw text input
food = st.text_input('What was eaten (e.g. "schoko muesli and milk")')

######################################################
# --- Load and categorize food dictionary ---
dict_path = "fooddata/food_dictionary.csv"
raw_items = pd.read_csv(dict_path)["Food List"].dropna().tolist()

# --- Auto-matching helper ---
def extract_food_items(text, dictionary_items):
    if not text:
        return []
    text = text.lower()
    matches = [item for item in dictionary_items if re.search(rf"\b{re.escape(item)}\b", text)]
    return matches

# Parse into a list with groups but only make real items selectable
selectable_options = []
display_options = []
current_group = ""

for item in raw_items:
    if item.startswith("--") and item.endswith("--"):
        current_group = item.strip("- ").strip()
        continue  # Don't include the label itself in options
    label = f"{current_group}: {item}" if current_group else item
    display_options.append(label)
    selectable_options.append(label)

# Auto-suggest from flat list
flat_food_list = [i for i in raw_items if not i.startswith("--")]
suggested = extract_food_items(food, flat_food_list)

# Map suggested to formatted labels
default_selected = []
for item in suggested:
    for group in display_options:
        if group.lower().endswith(item.lower()):
            default_selected.append(group)
            break

# Multiselect with visual groupings in label
food_item_selection = st.multiselect(
    "Select or confirm food items",
    options=display_options,
    default=default_selected
)
###########################################################
# Clean selected values (remove group prefix)
food_item = [item.split(": ", 1)[-1] for item in food_item_selection]


# Energy, stress, activity
st.subheader("Energy, Stress, and Activity")
energy = st.selectbox('Energy level after meal', ['', 'Energized', 'Balanced', 'Tired', 'Bloated', 'Irritable', 'Other'])
stress = st.selectbox('Stress level', ['', 'Low', 'Medium', 'High', 'No stress'])
activity_type = st.selectbox('Physical Activity', ['', 'Daily walk', 'Strength training', 'Fitness training', 'Cardio', 'None', 'Others'])

# Gut health
st.subheader("Gut Health")
gut = st.selectbox('Gut feeling after meal', ['', 'Settled', 'Full', 'Bloated', 'Nauseaous', 'Neutral', 'Refreshed', 'Other'])
bowel_freq = st.selectbox('Bowel Movement Frequency', ['', 'None', 'Once', 'Twice', 'Three or more'])

if bowel_freq != 'None':
    consistency = st.selectbox('Consistency', ['', 'Pellety', 'Lumpy', 'Firm', 'Soft', 'Blobby', 'Mushy', 'Watery'])
    ease = st.selectbox('Ease', ['', 'Easy', 'Difficult to pass', 'Urgent'])
else:
    consistency = None
    ease = None

# Compute Bristol Type and Gut State
bristol_gut_map = {
    'Pellety - Difficult to pass': {'Bristol Type': 1, 'Gut State': 'Constipated'},
    'Lumpy - Difficult to pass': {'Bristol Type': 2, 'Gut State': 'Constipated'},
    'Pellety - Easy': {'Bristol Type': 2, 'Gut State': 'Dehydrated'},
    'Lumpy - Easy': {'Bristol Type': 2, 'Gut State': 'Dehydrated'},
    'Firm - Easy': {'Bristol Type': 3, 'Gut State': 'Healthy'},
    'Soft - Easy': {'Bristol Type': 4, 'Gut State': 'Healthy'},
    'Blobby - Easy': {'Bristol Type': 5, 'Gut State': 'Diarrhea'},
    'Mushy - Urgent': {'Bristol Type': 6, 'Gut State': 'Diarrhea'},
    'Watery - Urgent': {'Bristol Type': 7, 'Gut State': 'Diarrhea'}
}
combined_key = f"{consistency} - {ease}"
bristol_type = bristol_gut_map.get(combined_key, {}).get('Bristol Type', None)
gut_state = bristol_gut_map.get(combined_key, {}).get('Gut State', None)

# Period tracking
if day_type == 'Period Day':
    st.subheader("Period Tracking")
    period_day = st.selectbox('What day of your period is it?', ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Day 7+'])
    st.write(f"**Current Period Day:** {period_day}")
    hygiene_product = st.multiselect(
        'Hygiene product used',
        ['', 'Super tampon', 'Normal tampon', 'Mini tampon', 'Night pad', 'Day pad']
    )
    flow = st.selectbox('Menstrual Flow', ['', 'Light', 'Medium', 'Heavy'])
    cramp_level = st.selectbox('Cramp Level', ['None', 'Mild', 'Moderate', 'More intense', 'Severe'])
else:
    period_day = 'N/A'
    hygiene_product = []
    flow = 'N/A'
    cramp_level = 'N/A'
    
    
# Skin health
st.subheader("Skin Health")
skin_status = st.selectbox('Acne / Skin', ['', 
    'No issues',
    'Single pimple (non-inflamed)',
    'Inflamed pimple (painful, with content)',
    'Clustered breakouts',
    'Rough skin',
    'Dry patches',
    'Other (Note)'
])

# Notes
st.subheader("Additional")
notes = st.text_area('Other notes')

# Save button
if st.button('Save entry'):
    new_row = {
        'Date': date,
        'Day Type': day_type,
        'Work Day/Weekend': work_or_weekend,
        'Meal Type': meal_type,
        'Meal Time': meal_time,
        'Item Class': item_class,
        'Food': food,
        'Food Item': ', '.join(food_item),
        'Energy Level': energy,
        'Stress Level': stress,
        'Activity Type': activity_type,
        'Gut Feeling': gut,
        'Bowel Movement Frequency': bowel_freq,
        'Consistency': consistency,
        'Ease': ease,
        'Bristol Type': bristol_type,
        'Gut State': gut_state,
        'Period Day': period_day,
        'Hygiene Product': ', '.join(hygiene_product) if hygiene_product else '',
        'Menstrual Flow': flow,
        'Cramp Level': cramp_level,
        'Acne/Skin': skin_status,
        'Notes': notes
    }

    save_to_gsheet(new_row)

    st.success('✅ Entry saved!')

# Columns to show in the Streamlit table (excluding helpers like 'Consistency' and 'Ease')
columns_to_show = [
    'Date', 'Day Type', 'Work Day/Weekend', 'Meal Type', 'Meal Time',
    'Item Class', 'Food', 'Energy Level', 'Stress Level',
    'Activity Type', 'Gut Feeling', 'Bristol Type', 'Gut State',
    'Hygiene Product', 'Menstrual Flow', 'Cramp Level', 'Acne/Skin', 'Notes'
]

st.page_link("pages/reports/entries.py", label="See Previous Entries")
