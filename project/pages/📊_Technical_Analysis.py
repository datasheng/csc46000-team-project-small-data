import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

from app import load_data

st.title("Technical Analysis")

data = load_data()

company = st.selectbox("Select Company", ['AMD', 'NVDA', 'INTC'])

tech_data = data['technical'][company]

# create RSI plot
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(tech_data['Date'], tech_data['RSI'])
ax.axhline(y=70, color='r', linestyle='--', alpha=0.5)
ax.axhline(y=30, color='g', linestyle='--', alpha=0.5)
ax.set_title(f'{company} Relative Strength Index (RSI)', fontsize=14)
ax.set_xlabel('Date')
ax.set_ylabel('RSI')
plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(fig)

# create MACD plot
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(tech_data['Date'], tech_data['MACD'])
ax.axhline(y=0, color='r', linestyle='--', alpha=0.5)
ax.set_title(f'{company} Moving Average Convergence Divergence (MACD)', fontsize=14)
ax.set_xlabel('Date')
ax.set_ylabel('MACD')
plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(fig) 