import requests
from textblob import TextBlob
import json
import numpy as np  
import yfinance as yf

class NewsAnalyzer:
    def __init__(self, api_key, ticker):
        """
        Initializes the NewsAnalyzer instance with the provided API key and ticker symbol.

        Parameters:
        - api_key (str): The API key for accessing the NewsAPI service.
        - ticker (str): The ticker symbol for identifying the company.
        """
        self.api_key = api_key
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
    
    def display_results(self):
        """
        Outputs list of json objects for related ticker symbol: 
        {'title': '', 'description':'','source':'','url':'', 'sentiment_score':}

        Parameters:
        None
        """
        try:
            processed_articles = self.process_articles()
            mean_score, median_score, std_deviation = self.calculate_statistics()
            
            if processed_articles:
                print("\nProcessed Articles:")
                print(json.dumps(processed_articles, indent=4))
            
            if mean_score is not None:
                print(f"\nSentiment Statistics:")
                print(f"Mean Sentiment Score: {mean_score:.4f}")
                print(f"Median Sentiment Score: {median_score:.4f}")
                print(f"Standard Deviation of Sentiment Scores: {std_deviation:.4f}")
            else:
                print("No valid sentiment data to calculate statistics.")
        except ValueError as e:
            print(f"Error: {e}")

''' Sample Instantiation and method usage
api_key = 'bc2130c922b14eadb55a749f3230f54e' # Sample key
ticker = 'AAPL'

# Instantiate the NewsAnalyzer class with ticker and api_key
news_analyzer = NewsAnalyzer(api_key, ticker)

# Call methods to fetch news and results
news_analyzer.fetch_news()
news_analyzer.display_results()
'''
