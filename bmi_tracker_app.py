{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import streamlit as st\
import pandas as pd\
import matplotlib.pyplot as plt\
from datetime import date\
from io import BytesIO\
\
# Initialize session state\
def init_session():\
    if 'data' not in st.session_state:\
        st.session_state.data = pd.DataFrame(columns=['Date', 'Weight (kg)', 'Height (m)', 'BMI'])\
\
# Calculate BMI\
def calculate_bmi(weight, height):\
    if height > 0:\
        return round(weight / (height ** 2), 2)\
    else:\
        return None\
\
# Save entry\
def save_entry(entry_date, weight, height):\
    bmi = calculate_bmi(weight, height)\
    new_entry = pd.DataFrame(\{\
        'Date': [entry_date],\
        'Weight (kg)': [weight],\
        'Height (m)': [height],\
        'BMI': [bmi]\
    \})\
    st.session_state.data = pd.concat([st.session_state.data, new_entry]).drop_duplicates(subset=['Date'], keep='last').sort_values('Date')\
\
# Export to Excel\
def export_excel():\
    output = BytesIO()\
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:\
        st.session_state.data.to_excel(writer, index=False, sheet_name='BMI Tracker')\
    processed_data = output.getvalue()\
    return processed_data\
\
# Plot the graph\
def plot_graph():\
    fig, ax1 = plt.subplots()\
\
    ax1.bar(st.session_state.data['Date'], st.session_state.data['BMI'], alpha=0.6, label='BMI (Bar)')\
    ax2 = ax1.twinx()\
    ax2.plot(st.session_state.data['Date'], st.session_state.data['Weight (kg)'], color='orange', marker='o', label='Weight (Line)')\
\
    ax1.set_xlabel('Date')\
    ax1.set_ylabel('BMI')\
    ax2.set_ylabel('Weight (kg)')\
\
    fig.legend(loc='upper left')\
    st.pyplot(fig)\
\
# App Layout\
init_session()\
st.title('Daily Weight & BMI Tracker')\
\
st.subheader('Add / Edit Daily Entry')\
with st.form('entry_form'):\
    entry_date = st.date_input('Select Date', value=date.today())\
    weight = st.number_input('Weight (kg)', min_value=0.0, step=0.1)\
    height = st.number_input('Height (m)', min_value=0.0, step=0.01)\
    submitted = st.form_submit_button('Save Entry')\
\
if submitted:\
    save_entry(entry_date, weight, height)\
    st.success('Entry Saved!')\
\
st.subheader('Data Overview')\
st.dataframe(st.session_state.data)\
\
st.download_button('Export as Excel', data=export_excel(), file_name='bmi_tracker.xlsx')\
\
st.subheader('BMI & Weight Graph')\
if not st.session_state.data.empty:\
    plot_graph()\
\
st.subheader('Calendar View')\
calendar_dates = st.session_state.data['Date'].dt.date.tolist()\
st.write('Dates with entries:', calendar_dates)\
}