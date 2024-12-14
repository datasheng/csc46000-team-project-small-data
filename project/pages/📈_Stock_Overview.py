import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

from app import load_data

st.title(" Stock Price Analysis")

data = load_data()

sns.set_style("darkgrid")

# vvv you can choose a diff style vvv
# print(plt.style.available)
plt.style.use("seaborn-v0_8-dark")

# create price comparison plot
fig, ax = plt.subplots(figsize=(12, 6))

for company in ['AMD', 'NVDA', 'INTC']:
    df = data['historical'][company]
    ax.plot(df['Date'], df['Close'], label=company)

ax.set_title('Stock Price Comparison', fontsize=14)
ax.set_xlabel('Date')
ax.set_ylabel('Price (USD)')
ax.legend()
plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(fig)

# volume comparison
fig, ax = plt.subplots(figsize=(12, 6))

for company in ['AMD', 'NVDA', 'INTC']:
    df = data['historical'][company]
    ax.plot(df['Date'], df['Volume'], label=company)

ax.set_title('Trading Volume Comparison', fontsize=14)
ax.set_xlabel('Date')
ax.set_ylabel('Volume')
ax.legend()
plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(fig) 