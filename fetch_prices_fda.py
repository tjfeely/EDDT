import requests
import pandas as pd
import time
import os

FDA_API_KEY = os.getenv("FDA_API_KEY")
FDA_PRICES_URL = "https://api.financialdatasets.ai/prices"

class FinancialDataFetcher:
    def __init__(self):
        self.headers = {"X-API-KEY": FDA_API_KEY}

    def fetch_price_history(self, ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
        params = {
            "ticker": ticker,
            "start_date": start_date,
            "end_date": end_date,
            "interval": "day",
            "interval_multiplier": 1
        }
        try:
            response = requests.get(FDA_PRICES_URL, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            if "prices" not in data:
                print(f"⚠️ No prices found for {ticker}")
                return pd.DataFrame()
            prices = pd.DataFrame(data["prices"])
            prices["ticker"] = ticker
            return prices
        except Exception as e:
            print(f"❌ Error fetching prices for {ticker}: {e}")
            return pd.DataFrame()

    def batch_fetch_prices(self, tickers: list, start_date: str, end_date: str) -> pd.DataFrame:
        all_prices = []
        for ticker in tickers:
            print(f"🔍 Fetching full price history for {ticker}")
            df = self.fetch_price_history(ticker, start_date, end_date)
            if not df.empty:
                all_prices.append(df)
            time.sleep(1)
        if all_prices:
            return pd.concat(all_prices, ignore_index=True)
        else:
            return pd.DataFrame()