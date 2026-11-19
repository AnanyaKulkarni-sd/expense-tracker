
import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💰",
    layout="centered"
)

st.title("💰 My Expense Tracker")
st.write("Track your daily expenses easily!")

# Initialize expense data
if "expenses" not in st.session_state:
    st.session_state.expenses = []

# Add expense section
st.subheader("➕ Add a New Expense")

with st.form("expense_form"):
    expense_name = st.text_input("Expense Name")

    amount = st.number_input(
        "Amount (₹)",
        min_value=0.0,
        step=10.0
    )

    category = st.selectbox(
        "Category",
        ["Food", "Travel", "Shopping", "Bills", "Education", "Other"]
    )

    date = st.date_input("Date")

    submitted = st.form_submit_button("Add Expense")

    if submitted:
        if expense_name and amount > 0:
            st.session_state.expenses.append({
                "Name": expense_name,
                "Amount": amount,
                "Category": category,
                "Date": date
            })
            st.success("Expense added successfully!")
        else:
            st.warning("Please enter a name and valid amount.")

# Display expenses
st.subheader("📋 Your Expenses")

if st.session_state.expenses:

    df = pd.DataFrame(st.session_state.expenses)

    # Total expenses
    total = df["Amount"].sum()

    st.metric("Total Expenses", f"₹{total:.2f}")

    # Expense table
    st.dataframe(df, use_container_width=True)

    # Category-wise expenses
    st.subheader("📊 Spending by Category")

    category_total = df.groupby("Category")["Amount"].sum()

    st.bar_chart(category_total)

    # Delete expenses
    st.subheader("🗑️ Delete an Expense")

    expense_to_delete = st.selectbox(
        "Select expense to delete",
        range(len(df)),
        format_func=lambda x: df.iloc[x]["Name"]
    )

    if st.button("Delete Selected Expense"):
        st.session_state.expenses.pop(expense_to_delete)
        st.rerun()

else:
    st.info("No expenses added yet. Start by adding one above!")

st.caption("Made with Python and Streamlit ❤️")
