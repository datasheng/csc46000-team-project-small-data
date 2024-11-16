import yfinance as yf
import pandas as pd
import numpy as np

class DataRetrieval:
    """
    Initializes DataRetrieva instance.
    Takes in a ticker list for companies.
    """
    def __init__(self, ticker_list):
        self.ticker_list = ticker_list
        self.data_frames = []
        self.data_csv = []

    def retrieve_data(self):
        """
        Retrieves historical data of AMD, NVIDIA, and Intel. Calculates
        metrics for P/E Ratio, Dividend Yield, and Market Cap for each 
        month of every year. Also gathers other historical data like Open,
        Close, High, Low, etc.
        """
        for ticker in self.ticker_list:
            company_stock = yf.Ticker(ticker)
            history = company_stock.history(period="max")
            stock_info = company_stock.info

            # Group Data By year
            history["Year"] = history.index.year
            grouped_history = history.groupby("Year")
            data = []

            for year, row in grouped_history:
                trailing_eps = stock_info.get("trailingEps")
                shares_outstanding = stock_info.get("sharesOutstanding")

                # Calculate basic metrics
                row["P/E Ratio"] = row["Close"] / trailing_eps
                row["Dividend Yield"] = row["Dividends"] / row["Close"]
                row["Market Cap"] = shares_outstanding * row["Close"]

                data.append(row)

            yearly_data = pd.concat(data)
            yearly_data["Ticker"] = ticker

            self.data_frames.append(yearly_data)

    def get_current_info(self):
        """
        Gets the more recent data of AMD, NVIDIA, and Intel. Specifically,
        Retrieves current price, 52 week high, 52 week low, sector, market
        cap, trailing pe, forward pe, dividend yield, trailing eps, forward
        eps, and average volume. Returns a dataframe consisting of each ticker
        and the data.
        """
        current_info = []
        for ticker in self.ticker_list:
            company_stock = yf.Ticker(ticker)
            stock_info = company_stock.info

            current_price = stock_info.get("currentPrice")
            fifty_two_week_high = stock_info.get("fiftyTwoWeekHigh")
            fifty_two_week_low = stock_info.get("fiftyTwoWeekLow")
            sector =  stock_info.get("sector")
            market_cap = stock_info.get("marketCap")
            trailing_pe =  stock_info.get("trailingPE")
            forward_pe =  stock_info.get("forwardPE")
            dividend_yield =  stock_info.get("dividendYield")
            trailing_eps =  stock_info.get("trailingEps")
            forward_eps =  stock_info.get("forwardEps")
            average_volume =  stock_info.get("averageVolume")

            current_info.append({
                "Ticker" : ticker,
                "Sector" : sector,
                "52-Week-High" : fifty_two_week_high,
                "52-Week-Low" : fifty_two_week_low,
                "Market Cap" : market_cap,
                "Trailing PE" : trailing_pe,
                "Forward PE" : forward_pe,
                "Dividend Yield" : dividend_yield,
                "Trailing_EPS" : trailing_eps,
                "Forward EPS" : forward_eps,
                "Average Volume" : average_volume
            })

        current_info_df = pd.DataFrame(current_info)
        return current_info_df

    def get_dataframe(self, ticker):
        """
        Retrieves and returns a dataframe given a ticker (AMD, NVDA, or INTC)
        """
        combined_df = pd.concat(self.data_frames)
        filtered_df = combined_df[combined_df["Ticker"] == ticker]
        return filtered_df

    def save_csv(self):
        """
        Saves all dataframe in the object as a CSV file
        """
        for df in self.data_frames:
            ticker = df["Ticker"].iloc[0]
            filename = f"{ticker}_data_retrieval.csv"
            csv = df.to_csv(filename)
            self.data_csv.append(csv)
    
    def show_data(self):
        """
        Prints the data of each dataframe in the object
        """
        for df in self.data_frames:
            print(df)


#Example usage:
tickers = ["AMD", "NVDA", "INTC"]
dataRetrieval = DataRetrieval(tickers)
dataRetrieval.retrieve_data()
dataRetrieval.show_data()
dataRetrieval.save_csv()

curr = dataRetrieval.get_current_info()
print(curr)
