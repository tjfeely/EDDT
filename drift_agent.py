import pandas as pd

class DriftAgent:
    def __init__(self, df: pd.DataFrame):
        """
        Initialize with a DataFrame containing earnings and price data.
        Required columns:
        ['Ticker', 'Date', 'EPS_Actual', 'EPS_Consensus', 'Price_Before', 'Price_After']
        """
        self.df = df.copy()
    
    def compute_car(self) -> pd.DataFrame:
        """
        Compute Cumulative Abnormal Return (CAR) as:
        CAR = (Price_After - Price_Before) / Price_Before
        """
        self.df['CAR'] = (self.df['Price_After'] - self.df['Price_Before']) / self.df['Price_Before']
        return self.df

    def classify_surprise(self, threshold: float = 0.01) -> pd.DataFrame:
        """
        Classify earnings surprises into 'Positive', 'Negative', or 'Neutral'.
        A threshold (default = 1%) defines the boundary for neutral surprises.
        """
        surprise = (self.df['EPS_Actual'] - self.df['EPS_Consensus']) / self.df['EPS_Consensus']
        self.df['Surprise_Category'] = surprise.apply(
            lambda x: 'Positive' if x > threshold else 'Negative' if x < -threshold else 'Neutral'
        )
        return self.df

    def process(self) -> pd.DataFrame:
        """
        Run the full DriftAgent pipeline:
        - Compute CAR
        - Classify EPS surprise
        Returns the processed DataFrame.
        """
        self.compute_car()
        self.classify_surprise()
        return self.df


# --- Optional: Example usage below for testing ---

if __name__ == "__main__":
    # Sample mock data
    mock_data = pd.DataFrame({
        'Ticker': ['AAPL', 'GOOG', 'MSFT'],
        'Date': ['2024-11-01', '2024-11-01', '2024-11-01'],
        'EPS_Actual': [1.25, 14.1, 2.25],
        'EPS_Consensus': [1.10, 14.3, 2.25],
        'Price_Before': [180.0, 2800.0, 300.0],
        'Price_After': [190.0, 2790.0, 310.0]
    })

    agent = DriftAgent(mock_data)
    result_df = agent.process()
    print(result_df)
