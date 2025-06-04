import pandas as pd
from textblob import TextBlob
import seaborn as sns
import matplotlib.pyplot as plt


class CorrelationAnalysis:
    
    def __init__(self,df_news,df_stock):
        self.df_news = df_news
        self.df_stock = df_stock
        self.merged_df = None
    
    def normalize_date(self):
        # Convert to datetime format
        self.df_stock['Date'] = pd.to_datetime(self.df_stock['Date'])

        # Convert to datetime without specifying a format
        self.df_news['date'] = pd.to_datetime(self.df_news['date'], errors='coerce')

        # Remove timezone info if it exists
        self.df_news['date'] = self.df_news['date'].dt.tz_localize(None, ambiguous='NaT', nonexistent='NaT')

        # Normalize to keep only the date (drop time component)
        self.df_news['date'] = self.df_news['date'].dt.normalize()

    def align_date(self):
        self.merged_df = pd.merge(self.df_news, self.df_stock, left_on='date', right_on='Date', how='inner')
        self.merged_df = self.merged_df.drop(columns=['date'])
        return self.merged_df
    
    def sentiment_analysis(self):
        def get_sentiment(text):
            polarity = TextBlob(text).sentiment.polarity
            return polarity

        # Apply the function to the headline column
        self.df_news['sentiment'] = self.df_news['headline'].apply(get_sentiment)
        # self.merged_df['sentiment'] = self.merged_df['headline'].apply(get_sentiment)
        
    
    def aggregate_sentiment(self):
        # Group by date and compute average sentiment
        daily_avg_sentiment = self.df_news.groupby('date')['sentiment'].mean().reset_index()

        # Rename column for clarity
        daily_avg_sentiment.rename(columns={'sentiment': 'avg_sentiment'}, inplace=True)

        # Merge back into the original df_news if needed
        self.df_news = self.df_news.merge(daily_avg_sentiment, on='date', how='left')
        return self.df_news.head()
    
    def calculate_correlation(self):
        self.merged_df['daily_return'] = self.merged_df['Close'].pct_change()
        self.merged_df.dropna(subset=['daily_return', 'avg_sentiment'], inplace=True)
        correlation = self.merged_df['daily_return'].corr(self.merged_df['avg_sentiment'])
        print("Correlation between avg_sentiment and daily return:", correlation)


    def plot_sentiment_vs_daily(self):
        plt.figure(figsize=(10, 6))
        sns.regplot(x='sentiment', y='daily_return', data=self.merged_df, scatter_kws={'alpha':0.5})
        plt.title('Sentiment Score vs Daily Stock Return (with Regression Line)')
        plt.xlabel('Sentiment Score')
        plt.ylabel('Daily Stock Return')
        plt.grid(True)
        plt.show()

    def plot_change(self):
        import matplotlib.pyplot as plt

        fig, ax1 = plt.subplots(figsize=(12, 6))

        # Plot stock price (Close)
        ax1.plot(self.merged_df['Date'], self.merged_df['Close'], color='blue', label='Stock Price')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Stock Price', color='blue')
        ax1.tick_params(axis='y', labelcolor='blue')

        # Plot sentiment on secondary axis
        ax2 = ax1.twinx()
        ax2.plot(self.merged_df['Date'], self.merged_df['avg_sentiment'], color='red', label='Avg Daily Sentiment')
        ax2.set_ylabel('Avg Sentiment Score', color='red')
        ax2.tick_params(axis='y', labelcolor='red')

        plt.title('Stock Price vs. News Sentiment Over Time')
        plt.grid(True)
        fig.tight_layout()
        plt.show()


                


    