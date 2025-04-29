import pandas as pd

def load_earnings_data(filepath: str) -> pd.DataFrame:
    """
    Loads earnings data from WRDS CSV file.
    Keeps and renames required columns.
    Also generates a dummy EPS Consensus if needed.
    """
    df = pd.read_csv(filepath)

    # Select only necessary columns
    df = df[['tic', 'rdq', 'epspxq']].copy()

    # Rename columns for standardization
    df.rename(columns={
        'tic': 'Ticker',
        'rdq': 'Date',
        'epspxq': 'EPS_Actual'
    }, inplace=True)

    # Create dummy EPS_Consensus (e.g., 95% of Actual)
    df['EPS_Consensus'] = df['EPS_Actual'] * 0.95

    # Ensure Date is datetime
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # Drop any rows with missing data
    df.dropna(subset=['Ticker', 'Date', 'EPS_Actual', 'EPS_Consensus'], inplace=True)

    return df
