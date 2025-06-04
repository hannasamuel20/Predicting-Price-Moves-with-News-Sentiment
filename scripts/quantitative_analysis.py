import pandas as pd
import matplotlib.pyplot as plt
import os
import talib
import yfinance as yf
import pandas as pd

# project_root = os.path.abspath("..")


class QuantitativeAnalysis:
    def __init__(self,df,ticker):
        self.df = df
        self.ticker = ticker

    def change_to_datetime(self):
        self.df['Date'] = pd.to_datetime(self.df['Date'])
    def calculate_indicators(self):
        # SMA (Simple Moving Average)
        self.df['SMA_20'] = talib.SMA(self.df['Close'], timeperiod=20)

        # RSI (Relative Strength Index)
        self.df['RSI'] = talib.RSI(self.df['Close'], timeperiod=14)

        # MACD (Moving Average Convergence Divergence)
        self.df['MACD'], self.df['MACD_Signal'], self.df['MACD_Hist'] = talib.MACD(self.df['Close'], 
                                                                    fastperiod=12, 
                                                                    slowperiod=26, 
                                                                    signalperiod=9)
    def get_financial_metrics(self):
        # Download the ticker data
        data = yf.Ticker(self.ticker)
        info = data.info
        metrics = {
            "Market Cap": info.get("marketCap"),
            "Trailing P/E": info.get("trailingPE"),
            "Forward P/E": info.get("forwardPE"),
            "Beta": info.get("beta"),
            "Dividend Yield": info.get("dividendYield")
        }

        metrics_df = pd.DataFrame.from_dict(metrics, orient='index', columns=['Value'])
        return metrics_df


    def plot_close_and_SMA(self):
        plt.figure(figsize=(14, 6))
        plt.plot(self.df['Date'], self.df['Close'], label='Close Price')
        plt.plot(self.df['Date'], self.df['SMA_20'], label='SMA 20', color='orange')
        plt.title('Stock Price and SMA')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.grid(True)
        plt.show()

    def plot_RSI(self):
        plt.figure(figsize=(14, 4))
        plt.plot(self.df['Date'], self.df['RSI'], label='RSI', color='purple')
        plt.axhline(70, color='red', linestyle='--')
        plt.axhline(30, color='green', linestyle='--')
        plt.title('RSI')
        plt.legend()
        plt.grid(True)
        plt.show()

    def plot_MACD(self):
        plt.figure(figsize=(14, 4))
        plt.plot(self.df['Date'], self.df['MACD'], label='MACD', color='blue')
        plt.plot(self.df['Date'], self.df['MACD_Signal'], label='Signal Line', color='orange')
        plt.bar(self.df['Date'], self.df['MACD_Hist'], label='Histogram', color='grey')
        plt.title('MACD')
        plt.legend()
        plt.grid(True)
        plt.show()

