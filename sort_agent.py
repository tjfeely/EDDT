import pandas as pd

class SortAgent:
    def __init__(self, df: pd.DataFrame):
        """
        Initialize with the output of DriftAgent.
        Expected columns: ['Ticker', 'CAR', 'Surprise_Category', ...]
        """
        self.df = df.copy()

    def top_by_car(self, n=5, ascending=False):
        """
        Return top N stocks sorted by CAR.
        """
        return self.df.sort_values(by="CAR", ascending=ascending).head(n)

    def filter_by_surprise(self, category="Positive"):
        """
        Filter stocks by surprise category: 'Positive', 'Negative', or 'Neutral'.
        """
        return self.df[self.df["Surprise_Category"] == category].sort_values(by="CAR", ascending=False)

    def summary_stats(self):
        """
        Provide a quick summary of average CAR by category.
        """
        return self.df.groupby("Surprise_Category")["CAR"].agg(["mean", "count"]).reset_index()
