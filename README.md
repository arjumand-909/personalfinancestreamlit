# Personal Finance Tracking Application

A Streamlit-based application that allows users to record, track, and analyze their personal financial transactions with persistent storage using CSV/JSON files.

---

## 🚀 Features

* **Add Transactions** (Income/Expenses)
* **Persistent Storage** (CSV & JSON)
* **Monthly Summary**
* **Category-wise Breakdown**
* **Savings Rate Calculation**
* **Budget Alerts** (Spending vs Budget)
* **Clean UI using Streamlit Widgets**
* **Modular Project Structure**

---

## 📁 Project Structure

```
project/
│── app.py
│── requirements.txt
│── data/
│   ├── transactions.csv
│   └── budgets.json
│── modules/
│   ├── __init__.py
│   ├── storage.py
│   ├── insights.py
│   └── ui_components.py
```

---

## 🛠 Installation

1. Clone or download this project folder.
2. Open terminal inside the project directory.
3. Install required packages:

```bash
pip install -r requirements.txt
```

If you don't have a requirements file, install manually:

```bash
pip install streamlit pandas
```

---

## ▶ Run the Application

Inside the project directory, run:

```bash
streamlit run app.py
```

---

## 📚 Module Descriptions

### `app.py`

Main Streamlit application file that controls UI, navigation, and integrates all modules.

### `modules/storage.py`

Handles:

* Loading & saving transactions
* Loading & saving budgets

### `modules/insights.py`

Contains:

* Monthly summary logic
* Category breakdown logic
* Savings rate calculation
* Budget alert generation

### `modules/ui_components.py`

Includes:

* Transaction input form
* Summary cards & metrics UI

---

## 📦 Data Files

### `transactions.csv`

Stores all recorded transactions:

```
Date,Category,Description,Amount,Type
```

### `budgets.json`

Stores user-defined budgets:

```json
{
  "Food": 30000,
  "Transport": 10000,
  "Shopping": 15000
}
```

---

## 🔍 How the App Works

1. User enters transaction data.
2. Data is stored in CSV.
3. Budgets are updated in JSON.
4. Insights are refreshed dynamically.
5. Visual breakdowns and alerts are shown.

---

## 🧩 Future Improvements

* Add authentication
* Add database support (SQLite / Firebase)
* Add visualization charts
* Export monthly reports (PDF/CSV)

---

## 👨‍💻 Author

Personal Finance Tracker — Python + Streamlit Project.

Agar aap documentation ko aur detail mein chahte hain, batayen — main README ko mazeed improve kar dunga!
