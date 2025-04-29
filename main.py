import os
import pandas as pd
from earnings_loader import load_earnings_data
from fetch_prices_fda import FinancialDataFetcher
from drift_agent import DriftAgent
from sort_agent import SortAgent
from summary_agent import SummaryAgent
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def run_pipeline():
    # Load Earnings Data
    earnings_df = load_earnings_data('wrdsearnings.csv')
    print(f"✅ Loaded {len(earnings_df)} earnings records.")

    # Extract unique tickers
    tickers = earnings_df['Ticker'].unique().tolist()
    print(f"✅ Unique tickers to fetch prices for: {tickers}")

    # Determine date range
    start_date = earnings_df['Date'].min().strftime("%Y-%m-%d")
    end_date = earnings_df['Date'].max().strftime("%Y-%m-%d")
    print(f"✅ Fetching prices from {start_date} to {end_date}")

    # Fetch full price history once per ticker
    fetcher = FinancialDataFetcher()
    prices_df = fetcher.batch_fetch_prices(tickers, start_date, end_date)

    if prices_df.empty:
        print("❌ No price data fetched. Exiting.")
        return

    # Merge earnings and prices
    merged = []
    for idx, row in earnings_df.iterrows():
        ticker = row['Ticker']
        report_date = row['Date']

        # Find prices just before and after report date
        ticker_prices = prices_df[prices_df['ticker'] == ticker].copy()
        ticker_prices['time'] = pd.to_datetime(ticker_prices['time'])
        ticker_prices['time'] = ticker_prices['time'].dt.tz_localize(None)

        before = ticker_prices[ticker_prices['time'] < report_date].sort_values('time', ascending=False).head(1)
        after = ticker_prices[ticker_prices['time'] > report_date].sort_values('time', ascending=True).head(1)

        if before.empty or after.empty:
            continue

        price_before = before.iloc[0]['close']
        price_after = after.iloc[0]['close']

        merged.append({
            'Ticker': ticker,
            'Date': report_date,
            'EPS_Actual': row['EPS_Actual'],
            'EPS_Consensus': row['EPS_Consensus'],
            'Price_Before': price_before,
            'Price_After': price_after
        })

    full_df = pd.DataFrame(merged)

    if full_df.empty:
        print("❌ No valid price matches for earnings dates. Exiting.")
        return

    print("\n📊 Earnings Drift Results:")
    print(full_df)

    # Step 1: Calculate CAR and classify surprises
    drift_agent = DriftAgent(full_df)
    data_with_car = drift_agent.process()

    # Step 2: Sort stocks by CAR
    sort_agent = SortAgent(data_with_car)
    top_stocks = sort_agent.top_by_car()

    # Step 3: Summarize using GPT
    summary_agent = SummaryAgent(data_with_car)
    summary = summary_agent.generate_summary()

    # Step 4: Print results
    print("\n🔥 Top 3 Stocks by CAR:")
    print(top_stocks)

    print("\n📈 Average CAR by Surprise Category:")
    print(data_with_car.groupby('Surprise_Category').agg(mean=('CAR', 'mean'), count=('CAR', 'count')))

    print("\n📌 GPT Summary:")
    print(summary)

    save_summary_to_file(summary)

def save_summary_to_file(summary_text):
    today = datetime.today().strftime("%Y-%m-%d")
    filename = f"summary_report_{today}.txt"
    with open(filename, "w") as f:
        f.write(summary_text)
    print(f"\n✅ GPT Summary saved to: {filename}")

if __name__ == "__main__":
    run_pipeline()
