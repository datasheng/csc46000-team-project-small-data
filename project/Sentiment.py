import requests
from textblob import TextBlob
import json
import numpy as np  
import yfinance as yf
import pandas as pd
import os


class NewsAnalyzer:
    def __init__(self, ticker):
        """
        Initializes the NewsAnalyzer instance with the ticker symbol.

        Parameters:
        - api_key (str): The API key for accessing the NewsAPI service.
        - ticker (str): The ticker symbol for identifying the company.
        """
        from dotenv import load_dotenv
        load_dotenv()
        self.api_key = os.getenv("NEWS_API_KEY")
        self.ticker = ticker
        self.company_name = self.get_company_name_from_ticker(ticker)
        self.articles = []
        self.sentiment_scores = []
      
    # Private method: get_company_name_from_ticker (internal use)
    def get_company_name_from_ticker(self, ticker):
        try:
            stock = yf.Ticker(ticker)
            company_name = stock.info.get('longName', None)
            if company_name is None:
                raise ValueError(f"Company name not found for ticker {ticker}")
            return company_name
        # Library cannot correlate a company to the ticker
        except Exception as e:
            print(f"Error retrieving company name for ticker {ticker}: {e}")
            return None

    # Private method: process_articles (internal use)
    def process_articles(self):
        processed_articles = []
        self.sentiment_scores = [] 

        for article in self.articles:
            if article.get("description") and "[Removed]" not in article["description"]:
                title = article.get("title", "No Title")
                description = article.get("description", "No Description")
                source = article.get("source", {}).get("name", "Unknown Source")
                url = article.get("url", "No URL")
                
                # Calculate sentiment using TextBlob
                blob = TextBlob(description)
                sentiment_score = blob.sentiment.polarity  # Polarity score: -1 to 1
            
                processed_article = {
                    "title": title,
                    "description": description,
                    "source": source,
                    "url": url,
                    "sentiment_score": sentiment_score
                }

                processed_articles.append(processed_article)
                self.sentiment_scores.append(sentiment_score)
        return processed_articles
    
    # Private method: calculate_statistics (internal use)
    def calculate_statistics(self):
        if not self.sentiment_scores:
            return None, None, None
    
        mean_score = np.mean(self.sentiment_scores)
        median_score = np.median(self.sentiment_scores)
        std_deviation = np.std(self.sentiment_scores)
        
        return mean_score, median_score, std_deviation
    # Private method: fetch_news
    def fetch_news(self):
        """
        Fetches news articles related to the company using the NewsAPI service.

        Parameters:
        None
        """
        if not self.company_name:
            raise ValueError(f"Invalid ticker or company name could not be determined for {self.ticker}.")
  
        url = 'https://newsapi.org/v2/everything'
        params = {
            'q': self.company_name,  
            'apiKey': self.api_key,   
            'language': 'en',         
            'pageSize': 100,         
            'sortBy': 'relevancy'   
        }

        
        response = requests.get(url, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            json_data = response.json()
            self.articles = json_data.get('articles', [])
        else:
            print(f"Error fetching news: {response.status_code}")
    
    def export_sentiment(self):
        """
        Converts the processed articles into a DataFrame and returns as csv string
        """
        self.fetch_news()
        try:
            processed_articles = self.process_articles()
             
            if processed_articles:
                # Convert the list of processed articles into a DataFrame
                df = pd.DataFrame(processed_articles)
                csv_string = df.to_csv(index=False)
                return csv_string
            else:
                print("No articles to display.")
        
        except ValueError as e:
            print(f"Error: {e}")

'''
api_key = '' # Sample key
ticker = 'AAPL'
# StringIO needs to be used because function export_sentiment() returns csv_string but not into file. Real file must be created by user of class.
from io import StringIO

# Instantiate the NewsAnalyzer class with ticker 
news_analyzer = NewsAnalyzer(ticker)

# Export the csv and convert
csv_data = news_analyzer.export_sentiment()
df = pd.read_csv(StringIO(csv_data))
print(df)
'''