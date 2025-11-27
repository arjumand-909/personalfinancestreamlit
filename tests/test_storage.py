
import pytest
import pandas as pd
from modules import storage

def test_ensure_storage_creates_files(tmp_path, monkeypatch):
    # Monkeypatch DATA_DIR to temporary folder
    monkeypatch.setattr(storage, "DATA_DIR", tmp_path)
    storage.ensure_storage()
    assert (tmp_path / "transactions.csv").exists()
    assert (tmp_path / "budgets.json").exists()

def test_add_and_load_transaction(tmp_path, monkeypatch):
    monkeypatch.setattr(storage, "DATA_DIR", tmp_path)
    storage.ensure_storage()
    storage.add_transaction("2025-11-01", "Income", "Salary", "Monthly salary", 1000, "Bank", "Default")
    df = storage.load_data()
    assert not df.empty
    assert df.iloc[0]["category"] == "Salary"
    assert df.iloc[0]["amount"] == 1000.0
