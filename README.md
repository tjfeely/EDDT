📊 Earnings Drift Detection Toolkit (EDDT)
EDDT is a Python-based toolkit that analyzes the market impact of earnings surprises by computing the Cumulative Abnormal Return (CAR) around earnings announcements. It integrates real price data from FinancialDatasets.ai and earnings data manually pulled from WRDS/Compustat. The project uses a modular agent-based architecture to perform fetching, calculations, sorting, and summarization.

🧠 Project Purpose
This tool is built to help researchers or investors:

Identify earnings drift effects for individual stocks

Classify earnings surprises as Positive, Negative, or Neutral

Compute CAR using before-and-after prices around earnings announcements

Generate summaries to interpret how surprise categories affect stock behavior

📂 Project Structure
EDDT/
├── main.py                  # Main pipeline entry point
├── drift_agent.py           # Computes CAR and classifies surprises
├── sort_agent.py            # Ranks stocks based on CAR
├── summary_agent.py         # GPT-powered natural language summary
├── earnings_loader.py       # Loads earnings data from WRDS export
├── price_fetcher.py         # Pulls historical price data from FinancialDatasets.ai
├── requirements.txt         # Required Python packages
├── wrdsearnings.csv         # Exported WRDS earnings data (EPS + dates)

⚙️ Installation
Clone the repo and create a virtual environment:
git clone https://github.com/yourusername/EDDT.git
cd EDDT
python3 -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

Install required dependencies:
pip install -r requirements.txt

🔐 API Key Setup
This project uses FinancialDatasets.ai to fetch real price data. Set your API key as an environment variable or directly in the price_fetcher.py file:
export FDA_API_KEY="your_real_api_key_here"
Alternatively, open price_fetcher.py and set the key manually:
FDA_API_KEY = os.getenv("FDA_API_KEY", "your_real_api_key_here")

🚀 Running the Project
Ensure your wrdsearnings.csv file (downloaded from WRDS/Compustat) is placed in the root directory. Then run:
python3 main.py
This will:

Load the earnings data from the CSV.

Fetch stock price data for each ticker from FinancialDatasets.ai.

Compute CAR for each event.

Classify the surprise.

Rank the top stocks by drift.

Output a GPT-based textual summary (if OpenAI API is configured).

🧾 Example Terminal Output
✅ Loaded 242 earnings records.
✅ Unique tickers to fetch prices for: ['AAPL', 'MSFT', 'NVDA']
✅ Fetching prices from 2010-02-17 to 2025-04-11

📊 Earnings Drift Results:
  Ticker       Date  EPS_Actual  EPS_Consensus  Price_Before  Price_After       CAR Surprise_Category
   AAPL 2010-04-20        3.39         3.22         8.82         8.74     -0.0091        Neutral
   NVDA 2024-05-22        6.04         5.74        95.39        94.95     -0.0046        Neutral

🔥 Top 3 Stocks by CAR:
  Ticker       Date       CAR
   NVDA    2022-05-25   0.0514
   AAPL    2022-04-28   0.0451
   MSFT    2020-04-29   0.0448

💬 Notes
EPS Consensus values are not available via WRDS. In this project, we simulate them as 95% of actual EPS unless you manually import real consensus estimates.
