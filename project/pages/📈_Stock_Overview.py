import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
# import matplotlib.pyplot as plt
# import seaborn as sns
import pandas as pd
from datetime import datetime, timedelta

from app import load_data

st.title("📈 Stock Price Analysis")

data = load_data()

# sns.set_style("darkgrid")

# # vvv you can choose a diff style vvv
# # print(plt.style.available)
# plt.style.use("seaborn-v0_8-dark")

# # create price comparison plot
# fig, ax = plt.subplots(figsize=(12, 6))

fig = make_subplots(rows=2, cols=1, 
                    subplot_titles=('Stock Price Comparison', 'Trading Volume'),
                    vertical_spacing=0.15,
                    row_heights=[0.7, 0.3])

colors = {
    'AMD': 'rgba(255, 0, 0, 0.7)', 
    'NVDA': 'rgba(118, 185, 0, 0.7)',
    'INTC': 'rgba(0, 113, 197, 0.7)' 
}

for company in ['AMD', 'NVDA', 'INTC']:
    df = data['historical'][company]
#     ax.plot(df['Date'], df['Close'], label=company)

# ax.set_title('Stock Price Comparison', fontsize=14)
# ax.set_xlabel('Date')
# ax.set_ylabel('Price (USD)')
# ax.legend()
# plt.xticks(rotation=45)
# plt.tight_layout()

# st.pyplot(fig)
# # volume comparison
# fig, ax = plt.subplots(figsize=(12, 6))
    
    # price plot
    fig.add_trace(
        go.Scatter(
            x=df['Date'],
            y=df['Close'],
            name=f"{company} Price",
            line=dict(color=colors[company].replace('0.7', '1.0')),
            hovertemplate="Date: %{x}<br>Price: $%{y:.2f}<extra></extra>"
        ),
        row=1, col=1
    )
    
    # volume plot
    fig.add_trace(
        go.Bar(
            x=df['Date'],
            y=df['Volume'],
            name=f"{company} Volume",
            marker=dict(
                color=colors[company],
                line=dict(color=colors[company].replace('0.7', '1.0'), width=1)
            ),
            hovertemplate="Date: %{x}<br>Volume: %{y:,.0f}<extra></extra>"
        ),
        row=2, col=1
    )

fig.update_layout(
    height=800,
    template='plotly_dark',
    showlegend=True,
    hovermode='x unified',
    legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    ),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)

fig.update_xaxes(
    title_text="Date", 
    row=2, col=1,
    gridcolor='rgba(128,128,128,0.2)',
    zerolinecolor='rgba(128,128,128,0.2)'
)
fig.update_yaxes(
    title_text="Price (USD)", 
    row=1, col=1,
    gridcolor='rgba(128,128,128,0.2)',
    zerolinecolor='rgba(128,128,128,0.2)'
)
fig.update_yaxes(
    title_text="Volume", 
    row=2, col=1,
    gridcolor='rgba(128,128,128,0.2)',
    zerolinecolor='rgba(128,128,128,0.2)'
)

st.plotly_chart(fig, use_container_width=True)

# Performance metrics section
st.subheader("📊 Performance Metrics")

today = pd.Timestamp.now(tz='UTC')
year_start = pd.Timestamp(today.year, 1, 1, tz='UTC')
last_year = today - timedelta(days=365)

for company in ['NVDA', 'AMD', 'INTC']:
    df = data['historical'][company]
#     ax.plot(df['Date'], df['Volume'], label=company)

# ax.set_title('Trading Volume Comparison', fontsize=14)
# ax.set_xlabel('Date')
# ax.set_ylabel('Volume')
# ax.legend()
# plt.xticks(rotation=45)
# plt.tight_layout()

# st.pyplot(fig) 
    df['Date'] = pd.to_datetime(df['Date'], utc=True)
    
    latest_date = df['Date'].max()
    ytd_current = df.loc[df['Date'] == latest_date, 'Close'].iloc[0]
    
    ytd_mask = df['Date'] >= year_start
    if ytd_mask.any():
        ytd_start = df[ytd_mask].iloc[0]['Close']
        ytd_perf = ((ytd_current - ytd_start) / ytd_start) * 100
    else:
        ytd_perf = 0
    
    year_mask = df['Date'] >= last_year
    if year_mask.any():
        year_start_price = df[year_mask].iloc[0]['Close']
        year_perf = ((ytd_current - year_start_price) / year_start_price) * 100
    else:
        year_perf = 0
    
    tech_data = data['technical'][company]
    current_rsi = tech_data['RSI'].iloc[-1]
    current_macd = tech_data['MACD'].iloc[-1]
    
    avg_volume = df['Volume'].mean()
    current_volume = df['Volume'].iloc[-1]
    volume_ratio = (current_volume / avg_volume - 1) * 100
    
    with st.container():
        st.markdown(f"### {company}")
        st.markdown(f"""
        **Price Metrics:**
        - Current Price: ${ytd_current:.2f}
        - YTD Change: {ytd_perf:+.1f}%
        - 1-Year Change: {year_perf:+.1f}%
        
        **Technical Indicators:**
        - RSI: {current_rsi:.1f}
        - MACD: {current_macd:+.2f}
        
        **Volume Analysis:**
        - Current vs Avg Volume: {volume_ratio:+.1f}%
        """)