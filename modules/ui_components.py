
import streamlit as st

def transaction_form(add_transaction_callback):
    st.sidebar.header("Add transaction")
    with st.sidebar.form("add_form", clear_on_submit=True):
        date = st.date_input("Date")
        typ = st.selectbox("Type", ["Expense","Income"])
        category = st.text_input("Category")
        description = st.text_input("Description")
        amount = st.number_input("Amount (PKR)", min_value=0.0, step=100.0, format="%.2f")
        payment_method = st.selectbox("Payment method", ["Cash","Card","Bank"])
        account = st.selectbox("Account", ["Default","Bank A","Wallet"])
        submitted = st.form_submit_button("Save")
        if submitted:
            if category.strip() and amount > 0:
                add_transaction_callback(date, typ, category, description, amount, payment_method, account)
                st.success("Transaction added.")
            else:
                st.warning("Category and amount required.")

def show_metrics(df, savings_rate_func, month_filter=None):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Income (PKR)", f"{df[df['type']=='Income']['amount'].sum():,.0f}")
    with col2:
        st.metric("Total Expense (PKR)", f"{df[df['type']=='Expense']['amount'].sum():,.0f}")
    with col3:
        sr = savings_rate_func(df, month_filter)
        st.metric("Savings Rate", f"{sr*100:.1f}%")
