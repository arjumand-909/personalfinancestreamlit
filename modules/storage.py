
import pandas as pd
import json
from pathlib import Path
from datetime import datetime

DATA_DIR = Path("data")
TXN_PATH = DATA_DIR / "transactions.csv"
BUDGET_PATH = DATA_DIR / "budgets.json"

def ensure_storage():
    DATA_DIR.mkdir(exist_ok=True)
    if not TXN_PATH.exists():
        df = pd.DataFrame(columns=["date","type","category","description","amount","payment_method","account"])
        df.to_csv(TXN_PATH, index=False)
    if not BUDGET_PATH.exists():
        with open(BUDGET_PATH, "w", encoding="utf-8") as f:
            json.dump({}, f, indent=2)

def load_data():
    ensure_storage()
    df = pd.read_csv(TXN_PATH)
    if not df.empty:
        df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    return df

def save_data(df: pd.DataFrame):
    df.to_csv(TXN_PATH, index=False)

def load_budgets():
    ensure_storage()
    with open(BUDGET_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_budgets(budgets: dict):
    with open(BUDGET_PATH, "w", encoding="utf-8") as f:
        json.dump(budgets, f, indent=2)
