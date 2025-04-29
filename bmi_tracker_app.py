import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
from io import BytesIO

# Initialize session state
def init_session():
    if 'data' not in st.session_state:
        st.session_state['data'] = pd.DataFrame(columns=['Date', 'Weight (kg)', 'Height (m)', 'BMI'])

# Calculate BMI
def calculate_bmi(weight, height):
    try:
        if height > 0:
            return round(weight / (height ** 2), 2)
        else:
            return None
    except Exception as e:
        st.error(f"Error calculating BMI: {e}")
        return None

# Save entry
def save_entry(entry_date, weight, height):
    bmi = calculate_bmi(weight, height)
    new_entry = pd.DataFrame({
        'Date': [pd.to_datetime(entry_date)],
        'Weight (kg)': [weight],
        'Height (m)': [height],
        'BMI': [bmi]
    })
    df = st.session_state['data']
    df = df[df['Date'] != pd.to_datetime(entry_date)]
    st.session_state['data'] = pd.concat([df, new_entry], ignore_index=True).sort_values('Date')

# Export to Excel
def export_excel():
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        st.session_state['data'].to_excel(writer, index=False, sheet_name='BMI Tracker')
    processed_data = output.getvalue()
    return processed_data

# Plot the graph
def plot_graph():
    df = st.session_state['data']
    if df.empty:
        st.info("No data to plot yet.")
        return

    fig, ax1 = plt.subplots(figsize=(10, 5))
    
    ax1.bar(df['Date'], df['BMI'], alpha=0.6, label='BMI (Bar)')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('BMI', color='blue')

    ax2 = ax1.twinx()
    ax2.plot(df['Date'], df['Weight (kg)'], color='orange', marker='o', label='Weight (Line)')
    ax2.set_ylabel('Weight (kg)', color='orange')

    fig.tight_layout()
    st.pyplot(fig)

# App Layout
init_session()
st.title('Daily Weight & BMI Tracker')

st.subheader('Add / Edit Daily Entry')
with st.form('entry_form'):
    entry_date = st.date_input('Select Date', value=date.today())
    weight = st.number_input('Weight (kg)', min_value=0.0, step=0.1, format="%0.1f")
    height = st.number_input('Height (m)', min_value=0.0, step=0.01, format="%0.2f")
    submitted = st.form_submit_button('Save Entry')

if submitted:
    save_entry(entry_date, weight, height)
    st.success('Entry Saved!')

st.subheader('Data Overview')
if not st.session_state['data'].empty:
    st.dataframe(st.session_state['data'])
else:
    st.info("No entries yet. Please add your first measurement.")

st.download_button('Export as Excel', data=export_excel(), file_name='bmi_tracker.xlsx')

st.subheader('BMI & Weight Graph')
plot_graph()

st.subheader('Calendar View')
if not st.session_state['data'].empty:
    calendar_dates = st.session_state['data']['Date'].dt.date.tolist()
    st.write('Dates with entries:', calendar_dates)
else:
    st.info("No dates to show yet.")
