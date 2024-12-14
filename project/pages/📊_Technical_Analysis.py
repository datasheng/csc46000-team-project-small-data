import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
from datetime import datetime

from app import load_data

st.title("📊 Technical Analysis")

data = load_data()

company = st.selectbox("Select Company", ['NVDA', 'AMD', 'INTC'])

tech_data = data['technical'][company]
price_data = data['historical'][company]

# create subplot with price, rsi, and macd
fig = make_subplots(rows=3, cols=1,
                    subplot_titles=('Price', 'RSI', 'MACD'),
                    vertical_spacing=0.1,
                    row_heights=[0.5, 0.25, 0.25])

# price plot
fig.add_trace(
    go.Scatter(
        x=price_data['Date'],
        y=price_data['Close'],
        name='Price',
        line=dict(color='#00FFFF'),
        hovertemplate="Date: %{x}<br>Price: $%{y:.2f}<extra></extra>"
    ),
    row=1, col=1
)

# rsi plot
fig.add_trace(
    go.Scatter(
        x=tech_data['Date'],
        y=tech_data['RSI'],
        name='RSI',
        line=dict(color='#FF69B4'),
        hovertemplate="Date: %{x}<br>RSI: %{y:.1f}<extra></extra>"
    ),
    row=2, col=1
)

# add overbought/oversold lines for RSI
fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)

# macd plot
fig.add_trace(
    go.Scatter(
        x=tech_data['Date'],
        y=tech_data['MACD'],
        name='MACD',
        line=dict(color='#FFA500'),
        hovertemplate="Date: %{x}<br>MACD: %{y:.2f}<extra></extra>"
    ),
    row=3, col=1
)

fig.add_hline(y=0, line_dash="dash", line_color="gray", row=3, col=1)

fig.update_layout(
    height=800,
    template='plotly_dark',
    showlegend=True,
    hovermode='x unified'
)

fig.update_xaxes(title_text="Date", row=3, col=1)
fig.update_yaxes(title_text="Price (USD)", row=1, col=1)
fig.update_yaxes(title_text="RSI", row=2, col=1)
fig.update_yaxes(title_text="MACD", row=3, col=1)

st.plotly_chart(fig, use_container_width=True)

# add technical indicator explanations
with st.expander("📚 Understanding Technical Indicators"):
    st.markdown("""
    - **RSI (Relative Strength Index)**: Momentum indicator measuring speed and magnitude of price changes
        - Above 70: Potentially overbought
        - Below 30: Potentially oversold
        
    - **MACD (Moving Average Convergence Divergence)**: Trend-following momentum indicator
        - Above 0: Bullish signal
        - Below 0: Bearish signal
    """) 