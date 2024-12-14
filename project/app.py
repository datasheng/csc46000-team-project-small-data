import pandas as pd
import numpy as np
from datetime import datetime

def load_data():
    """
    loads and preprocesses all data files
    returns: dictionary containing historical, technical, and sentiment data
    """
    # load all data files
    amd_hist = pd.read_csv('data/AMD_data_retrieval.csv')
    nvda_hist = pd.read_csv('data/NVDA_data_retrieval.csv')
    intc_hist = pd.read_csv('data/INTC_data_retrieval.csv')
    
    # load technical indicators
    amd_tech = pd.read_csv('data/AMD_technical_indicators.csv')
    nvda_tech = pd.read_csv('data/NVDA_technical_indicators.csv')
    intc_tech = pd.read_csv('data/INTC_technical_indicators.csv')
    
    # load sentiment data
    amd_sent = pd.read_csv('data/AMD_sentiments.csv')
    nvda_sent = pd.read_csv('data/NVDA_sentiments.csv')
    intc_sent = pd.read_csv('data/INTC_sentiments.csv')
    
    for df in [amd_hist, nvda_hist, intc_hist, amd_tech, nvda_tech, intc_tech]:
        df['Date'] = pd.to_datetime(df['Date'], utc=True)
    
    return {
        'historical': {'AMD': amd_hist, 'NVDA': nvda_hist, 'INTC': intc_hist},
        'technical': {'AMD': amd_tech, 'NVDA': nvda_tech, 'INTC': intc_tech},
        'sentiment': {'AMD': amd_sent, 'NVDA': nvda_sent, 'INTC': intc_sent}
    }

def get_important_events():
    """Returns a dictionary of important AI/GPU industry events"""
    return {
        '2006-07-24': 'AMD acquires ATI for $5.6B',
        '2006-11-06': 'NVIDIA releases CUDA platform',
        '2009-08-28': 'OpenCL released by Apple',
        '2012-09-30': 'AlexNet CNN wins ImageNet Challenge',
        '2017-05-10': 'NVIDIA Volta architecture announced',
        '2017-05-23': 'AlphaGo beats world champion Ke Jie',
        '2020-09-13': 'NVIDIA announces ARM acquisition (later cancelled)',
        '2020-10-27': 'AMD announces Xilinx acquisition for $35B',
        '2022-02-15': 'Intel announces Tower Semiconductor acquisition for $5.4B',
        '2022-11-30': 'ChatGPT public release',
        '2023-03-24': 'NVIDIA announces H100 Transformer Dashboards',
        '2023-05-30': 'NVIDIA reaches $1T market cap',
        '2023-12-06': 'AMD announces MI300X AI accelerator'
    }

def analyze_event_impact(historical_data, event_date, window=30):
    """
    Analyzes stock performance around important events
    """
    try:
        historical_data = historical_data.copy()
        
        historical_data['Date'] = pd.to_datetime(historical_data['Date'], utc=True)
        

        event_date = pd.to_datetime(event_date, utc=True)
        
        # data around event
        mask = (historical_data['Date'] >= event_date - pd.Timedelta(days=window)) & \
               (historical_data['Date'] <= event_date + pd.Timedelta(days=window))
        
        event_period = historical_data.loc[mask]
        
        if len(event_period) == 0:
            print(f"No data found around event date: {event_date}")
            return None
            
        pre_event = event_period[event_period['Date'] < event_date]
        post_event = event_period[event_period['Date'] > event_date]
        
        if len(pre_event) == 0 or len(post_event) == 0:
            print(f"Insufficient data around event date: {event_date}")
            return None
            
        pre_price = pre_event['Close'].mean()
        post_price = post_event['Close'].mean()
        price_change = ((post_price - pre_price) / pre_price) * 100
        
        return {
            'price_change': price_change,
            'pre_price': pre_price,
            'post_price': post_price
        }
    except Exception as e:
        print(f"Error analyzing event impact: {e}")
        return None