import requests
import json
from datetime import datetime
import os 
from dotenv import load_dotenv
load_dotenv()
import pandas as pd

# Each ticker should use the class once per day (limit of 5) since data will not change afterwards.
class TechnicalIndicators:
    def __init__(self, ticker: str, api_key: str):
        """
        Initializes the TechnicalIndicators class with a stock ticker symbol and an Alpha Vantage API key.
        
        Parameters:
        - ticker (str): The stock symbol (e.g., 'AAPL' for Apple).
        - api_key (str): Your Alpha Vantage API key.
        """
        self.ticker = ticker
        self.api_key = api_key

    # Private method: _get_technical_data (intended for internal use)
    def _get_technical_data(self, function: str, interval: str, start_date: str, time_period):
        if function == 'RSI':
            url = f'https://www.alphavantage.co/query?function={function}&symbol={self.ticker}&interval={interval}&time_period={time_period}&series_type=open&apikey={self.api_key}'
        else:
            url = f'https://www.alphavantage.co/query?function={function}&symbol={self.ticker}&interval={interval}&time_period={time_period}&apikey={self.api_key}'
        
        r = requests.get(url)
        data = r.json()
        key = f"Technical Analysis: {function}"
        technical_data = data.get(key, {})

        data_tuples = []
        if function == 'RSI':
            data_tuples = [(date, float(value['RSI'])) for date, value in technical_data.items()]
        elif function == 'ATR':
            data_tuples = [(date, float(value['ATR'])) for date, value in technical_data.items()]
        elif function == 'ADX':
            data_tuples = [(date, float(value['ADX'])) for date, value in technical_data.items()]

        data_tuples.sort(key=lambda x: datetime.strptime(x[0], "%Y-%m-%d"), reverse=True)
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
        filtered_data = [entry for entry in data_tuples if datetime.strptime(entry[0], "%Y-%m-%d") >= start_date_obj]

        return filtered_data

    # Private method: _get_technical_data (intended for internal use)
    def get_ema_data(self, interval: str, time_period: int):
        url = f'https://www.alphavantage.co/query?function=EMA&symbol={self.ticker}&interval={interval}&time_period={time_period}&series_type=close&apikey={self.api_key}'
        r = requests.get(url)
        data = r.json()
        return data

    # Public method: get_rsi (not recommended for direct use)
    def get_rsi(self, start_date: str, interval: str = 'daily', time_period: int = 14):
        """
        Fetches the Relative Strength Index (RSI)
        
        Parameters:
        - start_date (str): The start date in 'YYYY-MM-DD' format. End date is current by default
        - interval (str): The time interval between data points (default is 'daily').
        - time_period (int): The number of periods used for the RSI calculation (default is 14).
        
        Returns:
        - list of tuples: A list of tuples where each tuple contains the date and RSI value, sorted by date in descending order.
        """
        return self._get_technical_data('RSI', interval, start_date, time_period)

    # Public method: get_atr (not recommended for direct use)
    def get_atr(self, start_date: str, interval: str = 'daily', time_period: int = 14):
        """
        Fetches the Average True Range (ATR) for a given stock ticker.
        
        Parameters:
        - start_date (str): The start date in 'YYYY-MM-DD' format. End date is current by default
        - interval (str): The time interval between data points (default is 'daily').
        - time_period (int): The number of periods used for the RSI calculation (default is 14).
        
        Returns:
        - list of tuples: A list of tuples where each tuple contains the date and ATR value, sorted by date in descending order.
        """
        return self._get_technical_data('ATR', interval, start_date, time_period)

    # Public method: get_adx (not recommended for direct use)
    def get_adx(self, start_date: str, interval: str = 'daily', time_period: int = 14):
        """
        Fetches the Average Directional Index (ADX) for a given stock ticker, filtered by the start date.
        
        Parameters:
        - start_date (str): The start date in 'YYYY-MM-DD' format. End date is current by default
        - interval (str): The time interval between data points (default is 'daily').
        - time_period (int): The number of periods used for the RSI calculation (default is 14).
        
        Returns:
        - list of tuples: A list of tuples where each tuple contains the date and ADX value, sorted by date in descending order.
        """
        return self._get_technical_data('ADX', interval, start_date, time_period)

    # Public method: get_macd (not recommended for direct use)
    def get_macd(self, start_date: str, interval: str = 'daily'):
        """
        Fetches the MACD (Moving Average Convergence Divergence) values, which are the difference between the EMA 12 and EMA 26,
        for a given stock ticker, filtered by the start date.
        
        Parameters:
        - start_date (str): The start date in 'YYYY-MM-DD' format to filter the data.
        - interval (str): The time interval between data points (default is 'daily').
        
        Returns:
        - list of tuples: A list of tuples where each tuple contains the date and the MACD value (EMA 12 - EMA 26),
          sorted by date in descending order and filtered by the start date.
        """
        ema12_data = self.get_ema_data(interval, 12)
        ema26_data = self.get_ema_data(interval, 26)

        ema12_tuples = [(date, float(value['EMA'])) for date, value in ema12_data["Technical Analysis: EMA"].items()]
        ema26_tuples = [(date, float(value['EMA'])) for date, value in ema26_data["Technical Analysis: EMA"].items()]

        ema12_tuples.sort(key=lambda x: datetime.strptime(x[0], "%Y-%m-%d"), reverse=True)
        ema26_tuples.sort(key=lambda x: datetime.strptime(x[0], "%Y-%m-%d"), reverse=True)

        macd_values = []

        for ema12, ema26 in zip(ema12_tuples, ema26_tuples):
            date_ema12, value_ema12 = ema12
            date_ema26, value_ema26 = ema26

            if date_ema12 == date_ema26:
                macd_value = value_ema12 - value_ema26
                macd_values.append((date_ema12, macd_value))

        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
        filtered_macd_values = [entry for entry in macd_values if datetime.strptime(entry[0], "%Y-%m-%d") >= start_date_obj]

        return filtered_macd_values

    # Public method: get_indicators
    def get_indicators(self, start_date: str, interval: str = 'daily', time_period: int = 14):
        """
        Fetches all technical indicator data (RSI, ATR, ADX, MACD) and returns it as a DataFrame.
        
        Parameters:
        - start_date (str): The start date in 'YYYY-MM-DD' format.
        - interval (str): The time interval between data points (default is 'daily').
        - time_period (int): The number of periods used for calculations (default is 14).

        Returns:
        - pandas DataFrame in CSV format: Please convert csv to DataFrame to read data
        """
        try:
          # Obtain individual technical indicators
          rsi_data = self.get_rsi(start_date, interval, time_period)
          atr_data = self.get_atr(start_date, interval, time_period)
          adx_data = self.get_adx(start_date, interval, time_period)
          macd_data = self.get_macd(start_date, interval)

          # Create a dictionary of lists to convert to DataFrame later.
          all_data = {
              'Date': [],
              'RSI': [],
              'ATR': [],
              'ADX': [],
              'MACD': []
          }

          dates = sorted(set([entry[0] for entry in rsi_data + atr_data + adx_data + macd_data]), reverse=True)

          for date in dates:
              all_data['Date'].append(datetime.strptime(date, "%Y-%m-%d"))
              all_data['RSI'].append(next((rsi for rsi_date, rsi in rsi_data if rsi_date == date), None))
              all_data['ATR'].append(next((atr for atr_date, atr in atr_data if atr_date == date), None))
              all_data['ADX'].append(next((adx for adx_date, adx in adx_data if adx_date == date), None))
              all_data['MACD'].append(next((macd for macd_date, macd in macd_data if macd_date == date), None))

          # Create DataFrame
          df = pd.DataFrame(all_data)
          df.set_index('Date', inplace=True)

          csv_string = df.to_csv(index=True)
          return csv_string
        # If API request fails, must have reached daily limit (5)
        except Exception as e:
          print("API Key Failed")
          return None

'''
technical_indicators = TechnicalIndicators(ticker='AMD', api_key="")

# StringIO needs to be used because function get_indicators() returns csv_string but not into file. Real file must be created by user of class.
from io import StringIO

start_date = "YYYY-MM-DD"
csv_data = technical_indicators.get_indicators(start_date, "daily")
df = pd.read_csv(StringIO(csv_data), index_col='Date')
print(df)
'''
