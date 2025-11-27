#Arjumand Afreen Tabinda
#Roll number 411210

import streamlit as st
import pandas as pd
import json
from pathlib import Path
from datetime import datetime

# ------------------------------
# Storage Paths
# ------------------------------
DATA_DIR = Path("data")
TXN_PATH = DATA_DIR / "transactions.csv"
BUDGET_PATH = DATA_DIR / "budgets.json"

# ------------------------------
# Ensure storage exists
# ------------------------------
def ensure_storage():
    DATA_DIR.mkdir(exist_ok=True)

    if not TXN_PATH.exists():
        df = pd.DataFrame(columns=[
            "date", "type", "category", "description", "amount", "payment_method", "account"
        ])
        df.to_csv(TXN_PATH, index=False)

    if not BUDGET_PATH.exists():
        with open(BUDGET_PATH, "w", encoding="utf-8") as f:
            json.dump({}, f, indent=2)

# ------------------------------
# Load / Save
# ------------------------------
def load_data():
    ensure_storage()
    df = pd.read_csv(TXN_PATH)

    if not df.empty:
        df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    return df

def save_data(df):
    df.to_csv(TXN_PATH, index=False)

def load_budgets():
    ensure_storage()
    with open(BUDGET_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_budgets(budgets):
    with open(BUDGET_PATH, "w", encoding="utf-8") as f:
        json.dump(budgets, f, indent=2)

# ------------------------------
# Add / Update / Delete
# ------------------------------
def add_transaction(date, typ, category, description, amount, payment_method, account):
    df = load_data()
    new_row = {
        "date": pd.to_datetime(date).date(),
        "type": typ,
        "category": category.strip(),
        "description": description.strip(),
        "amount": float(amount),
        "payment_method": payment_method,
        "account": account,
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    save_data(df)

# ------------------------------
# Insights Functions
# ------------------------------
def monthly_summary(df):
    if df.empty:
        return pd.DataFrame(columns=["year_month", "Income", "Expense", "Net"])

    temp = df.copy()
    temp["year_month"] = pd.to_datetime(temp["date"]).dt.to_period("M").astype(str)

    income = temp[temp["type"] == "Income"].groupby("year_month")["amount"].sum()
    expense = temp[temp["type"] == "Expense"].groupby("year_month")["amount"].sum()

    summary = pd.DataFrame({"Income": income, "Expense": expense}).fillna(0.0)
    summary["Net"] = summary["Income"] - summary["Expense"]
    return summary.reset_index()

def category_breakdown(df, month_filter=None):
    if df.empty:
        return pd.DataFrame(columns=["category", "Income", "Expense", "Net"])

    temp = df.copy()
    temp["year_month"] = pd.to_datetime(temp["date"]).dt.to_period("M").astype(str)

    if month_filter:
        temp = temp[temp["year_month"] == month_filter]

    income = temp[temp["type"] == "Income"].groupby("category")["amount"].sum()
    expense = temp[temp["type"] == "Expense"].groupby("category")["amount"].sum()

    cat = pd.DataFrame({"Income": income, "Expense": expense}).fillna(0.0)
    cat["Net"] = cat["Income"] - cat["Expense"]

    return cat.reset_index().sort_values(by="Expense", ascending=False)

def savings_rate(df, month_filter=None):
    if df.empty:
        return 0.0

    temp = df.copy()
    temp["year_month"] = pd.to_datetime(temp["date"]).dt.to_period("M").astype(str)

    if month_filter:
        temp = temp[temp["year_month"] == month_filter]

    inc = temp[temp["type"] == "Income"]["amount"].sum()
    exp = temp[temp["type"] == "Expense"]["amount"].sum()

    return (inc - exp) / inc if inc > 0 else 0.0

def budget_alerts(df, budgets, month_filter=None):
    if df.empty or not budgets:
        return pd.DataFrame(columns=["category", "spent", "budget", "status"])

    temp = df.copy()
    temp["year_month"] = pd.to_datetime(temp["date"]).dt.to_period("M").astype(str)

    if month_filter:
        temp = temp[temp["year_month"] == month_filter]

    spent = temp[temp["type"] == "Expense"].groupby("category")["amount"].sum()

    rows = []
    for cat, b in budgets.items():
        s = float(spent.get(cat, 0.0))
        status = "OK" if s <= b else "Over"
        rows.append({"category": cat, "spent": s, "budget": b, "status": status})

    return pd.DataFrame(rows)

# ------------------------------
# Streamlit UI
# ------------------------------
st.set_page_config(page_title="Personal Finance Tracker", page_icon="💸", layout="wide")
st.title("Personal Finance Tracker")

# Sidebar - Add Transaction
st.sidebar.header("Add Transaction")
with st.sidebar.form("add_form", clear_on_submit=True):
    date = st.date_input("Date", value=datetime.today())
    typ = st.selectbox("Type", ["Expense", "Income"])
    category = st.text_input("Category")
    description = st.text_input("Description")
    amount = st.number_input("Amount (PKR)", min_value=0.0, step=100.0)
    payment_method = st.selectbox("Payment method", ["Cash", "Card", "Bank"])
    account = st.selectbox("Account", ["Default", "Bank A", "Wallet"])

    if st.form_submit_button("Save"):
        if category.strip() and amount > 0:
            add_transaction(date, typ, category, description, amount, payment_method, account)
            st.success("Transaction added.")
        else:
            st.warning("Category and amount required.")

# Sidebar - Budgets
st.sidebar.header("Budgets")
budgets = load_budgets()

with st.sidebar.expander("Edit Budgets"):
    new_cat = st.text_input("New Category")
    new_amt = st.number_input("Budget Amount (PKR)", min_value=0.0)

    if st.button("Add/update"):
        if new_cat.strip():
            budgets[new_cat] = new_amt
            save_budgets(budgets)
            st.success("Saved")

    if budgets:
        rem = st.selectbox("Remove Budget", ["(none)"] + list(budgets.keys()))
        if st.button("Delete") and rem in budgets:
            del budgets[rem]
            save_budgets(budgets)
            st.info("Removed")

# ------------------------------
# Filters
# ------------------------------
df = load_data()

col1, col2, col3 = st.columns(3)
with col1:
    months = sorted(pd.to_datetime(df["date"]).dt.to_period("M").astype(str).unique()) if not df.empty else []
    month_filter = st.selectbox("Month", ["(All)"] + months)
    month_filter = None if month_filter == "(All)" else month_filter

with col2:
    type_filter = st.selectbox("Type Filter", ["(All)", "Expense", "Income"])

with col3:
    category_filter = st.selectbox("Category Filter", ["(All)"] + sorted(df["category"].dropna().unique().tolist()) if not df.empty else [])

filtered = df.copy()
if month_filter:
    filtered["year_month"] = pd.to_datetime(filtered["date"]).dt.to_period("M").astype(str)
    filtered = filtered[filtered["year_month"] == month_filter]

if type_filter != "(All)":
    filtered = filtered[filtered["type"] == type_filter]

if category_filter != "(All)":
    filtered = filtered[filtered["category"] == category_filter]

# ------------------------------
# Transactions Table
# ------------------------------
st.subheader("Transactions")

if filtered.empty:
    st.info("No transactions found.")
else:
    edited_df = st.data_editor(filtered, width="stretch")

    if st.button("Apply Edits"):
        original = df.copy()

        mask = original.apply(tuple, 1).isin(filtered.apply(tuple, 1))
        original = original[~mask]

        original = pd.concat([original, edited_df], ignore_index=True)
        save_data(original)
        st.success("Changes saved.")

    to_delete = st.multiselect("Select rows to delete", edited_df.index)

    if st.button("Delete Selected"):
        original = load_data()
        for idx in to_delete:
            row = edited_df.loc[idx]
            cond = (original == row).all(axis=1)
            original = original[~cond]
        save_data(original)
        st.warning("Deleted.")

# ------------------------------
# Insights
# ------------------------------
st.subheader("Insights")

ms = monthly_summary(df)
cb = category_breakdown(df, month_filter)
sr = savings_rate(df, month_filter)
ba = budget_alerts(df, budgets, month_filter)

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Total Income", f"{df[df['type']=='Income']['amount'].sum():,.0f}")

with c2:
    st.metric("Total Expense", f"{df[df['type']=='Expense']['amount'].sum():,.0f}")

with c3:
    st.metric("Savings Rate", f"{sr*100:.1f}%")

st.write("### Monthly Summary")
st.dataframe(ms, width="stretch")
if not ms.empty:
    st.line_chart(ms.set_index("year_month")[["Income", "Expense", "Net"]])

st.write("### Category Breakdown")
st.dataframe(cb, width="stretch")
if not cb.empty:
    st.bar_chart(cb.set_index("category")[["Expense", "Income"]])

st.write("### Budget Alerts")
if ba.empty:
    st.info("No budgets / no expenses.")
else:
    st.dataframe(ba, width="stretch")

# ------------------------------
# Export
# ------------------------------
st.subheader("Export")
colA, colB = st.columns(2)

with colA:
    st.download_button("Download CSV", TXN_PATH.read_bytes(), "transactions.csv")

with colB:
    st.download_button("Download Budgets", BUDGET_PATH.read_bytes(), "budgets.json")

st.caption("Developed for PKR users - keep categories consistent for better insights.")
