import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import sys
from pathlib import Path

# add project directory to path
project_dir = Path(__file__).parent
sys.path.append(str(project_dir))

from app import load_data, get_important_events, analyze_event_impact

st.set_page_config(
    page_title="GPU Market Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 GPU Market Analysis")
st.markdown("""
### Analyzing the Semiconductor Industry in the AI Era
Track how artificial intelligence and technological advancements influence the GPU market leaders: 
NVIDIA, AMD, and Intel
""")

data = load_data()


st.subheader("📈 Market Overview")
col1, col2, col3 = st.columns(3)

# get latest prices and calculate daily changes
with col1:
    latest_nvda = data['historical']['NVDA']['Close'].iloc[-1]
    change_nvda = latest_nvda - data['historical']['NVDA']['Close'].iloc[-2]
    st.metric(
        "NVIDIA",
        f"${latest_nvda:.2f}",
        f"{change_nvda:.2f} ({(change_nvda/latest_nvda)*100:.1f}%)"
    )

with col2:
    latest_amd = data['historical']['AMD']['Close'].iloc[-1]
    change_amd = latest_amd - data['historical']['AMD']['Close'].iloc[-2]
    st.metric(
        "AMD",
        f"${latest_amd:.2f}",
        f"{change_amd:.2f} ({(change_amd/latest_amd)*100:.1f}%)"
    )

with col3:
    latest_intc = data['historical']['INTC']['Close'].iloc[-1]
    change_intc = latest_intc - data['historical']['INTC']['Close'].iloc[-2]
    st.metric(
        "Intel",
        f"${latest_intc:.2f}",
        f"{change_intc:.2f} ({(change_intc/latest_intc)*100:.1f}%)"
    )

st.subheader("🎯 Major Events Impact Analysis")

# you can get rid of this - just spitballing here
events = get_important_events()
event_impact = st.columns(2)

with event_impact[0]:
    st.markdown("### Event Timeline")
    for date, event in events.items():
        st.markdown(f"**{date}**: {event}")

with event_impact[1]:
    st.markdown("### Stock Performance Around Events")
    selected_event = st.selectbox(
        "Select an event to analyze",
        list(events.keys()),
        format_func=lambda x: f"{x}: {events[x]}"
    )
    
    companies = {
        'NVIDIA': data['historical']['NVDA'],
        'AMD': data['historical']['AMD'],
        'Intel': data['historical']['INTC']
    }
    
    for company, hist_data in companies.items():
        impact = analyze_event_impact(hist_data, selected_event)
        if impact:
            change_color = 'green' if impact['price_change'] > 0 else 'red'
            st.markdown(f"""
            **{company}**:
            - Price Change: <span style='color:{change_color}'>{impact['price_change']:.1f}%</span>
            - Avg Price Before: ${impact['pre_price']:.2f}
            - Avg Price After: ${impact['post_price']:.2f}
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"**{company}**: No data available for this period")


st.markdown("""
## 📊 Market Summary
This dashboard provides comprehensive analysis of the three major GPU manufacturers:

- **NVIDIA**: Leading AI chip manufacturer
- **AMD**: Strong competitor in both CPU and GPU markets
- **Intel**: Traditional semiconductor giant entering discrete GPU market

The analysis includes historical price data, technical indicators, and the impact of major industry events on stock performance. The event analysis helps understand how technological advancements and industry milestones affect market valuations.
""") 