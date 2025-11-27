
import pandas as pd
from modules import insights

def sample_df():
    return pd.DataFrame([
        {"date":"2025-11-01","type":"Income","category":"Salary","description":"Monthly","amount":1000,"payment_method":"Bank","account":"Default"},
        {"date":"2025-11-02","type":"Expense","category":"Food","description":"Lunch","amount":200,"payment_method":"Cash","account":"Wallet"},
    ])

def test_monthly_summary():
    df = sample_df()
    summary = insights.monthly_summary(df)
    assert "Income" in summary.columns
    assert "Expense" in summary.columns
    assert summary.iloc[0]["Net"] == 800

def test_savings_rate():
    df = sample_df()
    rate = insights.savings_rate(df)
    assert round(rate,2) == 0.80  # 800/1000
