

import pytest
from modules import storage, insights

def test_budget_alerts_ok():
    df = storage.load_data()
    budgets = {"Food": 500}
    alerts = insights.budget_alerts(df, budgets)
    assert "status" in alerts.columns

def test_budget_alerts_over():
    df = storage.load_data()
    # Add expense more than budget
    storage.add_transaction("2025-11-03","Expense","Food","Dinner",600,"Cash","Wallet")
    budgets = {"Food": 500}
    alerts = insights.budget_alerts(df, budgets)
    assert "Over" in alerts["status"].values
