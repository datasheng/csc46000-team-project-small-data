import requests
import json
from datetime import datetime

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

    # Public method: get_rsi
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

    # Public method: get_atr
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

    # Public method: get_adx
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

    # Public method: get_macd
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
''' This is a sample of instantiation and usage
if __name__ == "__main__":
    technical_indicators = TechnicalIndicators(ticker='AAPL', api_key = "NTOX75FCMPTPTGTI")

    start_date = "2024-11-06"
    macd_data = technical_indicators.get_macd_values(start_date=start_date, interval="daily")

    print("Filtered MACD Data:", macd_data)
'''