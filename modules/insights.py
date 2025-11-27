
import pandas as pd

def monthly_summary(df: pd.DataFrame):
    if df.empty:
        return pd.DataFrame(columns=["year_month","Income","Expense","Net"])
    temp = df.copy()
    temp["year_month"] = pd.to_datetime(temp["date"]).dt.to_period("M").astype(str)
    income = temp[temp["type"]=="Income"].groupby("year_month")["amount"].sum()
    expense = temp[temp["type"]=="Expense"].groupby("year_month")["amount"].sum()
    summary = pd.DataFrame({"Income": income, "Expense": expense}).fillna(0.0)
    summary["Net"] = summary["Income"] - summary["Expense"]
    return summary.reset_index()

def category_breakdown(df: pd.DataFrame, month_filter=None):
    if df.empty:
        return pd.DataFrame(columns=["category","Income","Expense","Net"])
    temp = df.copy()
    temp["year_month"] = pd.to_datetime(temp["date"]).dt.to_period("M").astype(str)
    if month_filter:
        temp = temp[temp["year_month"] == month_filter]
    income = temp[temp["type"]=="Income"].groupby("category")["amount"].sum()
    expense = temp[temp["type"]=="Expense"].groupby("category")["amount"].sum()
    cat = pd.DataFrame({"Income": income, "Expense": expense}).fillna(0.0)
    cat["Net"] = cat["Income"] - cat["Expense"]
    return cat.reset_index().sort_values(by="Expense", ascending=False)

def savings_rate(df: pd.DataFrame, month_filter=None):
    if df.empty:
        return 0.0
    temp = df.copy()
    temp["year_month"] = pd.to_datetime(temp["date"]).dt.to_period("M").astype(str)
    if month_filter:
        temp = temp[temp["year_month"] == month_filter]
    inc = temp[temp["type"]=="Income"]["amount"].sum()
    exp = temp[temp["type"]=="Expense"]["amount"].sum()
    return (inc - exp) / inc if inc > 0 else 0.0

def budget_alerts(df: pd.DataFrame, budgets: dict, month_filter=None):
    if df.empty or not budgets:
        return pd.DataFrame(columns=["category","spent","budget","status"])
    temp = df.copy()
    temp["year_month"] = pd.to_datetime(temp["date"]).dt.to_period("M").astype(str)
    if month_filter:
        temp = temp[temp["year_month"] == month_filter]
    spent = temp[temp["type"]=="Expense"].groupby("category")["amount"].sum()
    rows = []
    for cat, b in budgets.items():
        s = float(spent.get(cat, 0.0))
        status = "OK" if s <= b else "Over"
        rows.append({"category": cat, "spent": s, "budget": float(b), "status": status})
    return pd.DataFrame(rows).sort_values(by="status", ascending=False)
