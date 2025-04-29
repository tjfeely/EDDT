import os
import openai
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

class SummaryAgent:
    def __init__(self, df):
        self.df = df

    def generate_summary(self):
        if self.df.empty:
            return "No data available for summary."

        try:
            text_data = self.df.to_string(index=False)

            prompt = f"""
You are a financial analyst assistant.

Given the following earnings drift data (with columns: Ticker, Date, EPS_Actual, EPS_Consensus, Price_Before, Price_After, CAR, Surprise_Category):

{text_data}

Write a professional, concise summary for a financial report including:
- General insights about CAR
- How different Surprise Categories performed
- Any notable company mentions
- Mention average CAR trends if possible
"""

            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a financial analyst specialized in earnings reports."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )

            summary = response.choices[0].message.content.strip()
            return summary

        except Exception as e:
            return f"❌ GPT generation failed: {e}"
