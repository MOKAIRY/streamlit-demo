import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💷",
    layout="wide"
)

st.title("💷 Personal Expense Tracker")
st.caption("Intermediate Python + Streamlit Demo By Meshal Okairy")

# -----------------------------
# SESSION STATE
# -----------------------------

if "expenses" not in st.session_state:
    st.session_state.expenses = [
        {
            "Date": "2026-08-20",
            "Category": "Food",
            "Description": "Lunch",
            "Amount": 12.50
        },
        {
            "Date": "2026-08-21",
            "Category": "Transport",
            "Description": "Train ticket",
            "Amount": 18.00
        },
        {
            "Date": "2026-08-22",
            "Category": "Shopping",
            "Description": "Python book",
            "Amount": 29.99
        }
    ]


# -----------------------------
# FUNCTIONS
# -----------------------------

def add_expense(expense_date, category, description, amount):
    expense = {
        "Date": str(expense_date),
        "Category": category,
        "Description": description,
        "Amount": amount
    }

    st.session_state.expenses.append(expense)


def calculate_total(expenses):
    return sum(expense["Amount"] for expense in expenses)


def get_dataframe():
    return pd.DataFrame(st.session_state.expenses)


# -----------------------------
# SIDEBAR FORM
# -----------------------------

st.sidebar.header("Add Expense")

with st.sidebar.form("expense_form"):

    expense_date = st.date_input(
        "Date",
        value=date.today()
    )

    category = st.selectbox(
        "Category",
        [
            "Food",
            "Transport",
            "Shopping",
            "Bills",
            "Entertainment",
            "Other"
        ]
    )

    description = st.text_input(
        "Description"
    )

    amount = st.number_input(
        "Amount (£)",
        min_value=0.01,
        step=1.00
    )

    submitted = st.form_submit_button(
        "Add Expense",
        use_container_width=True
    )

    if submitted:

        if not description.strip():
            st.error("Please enter a description.")

        else:
            add_expense(
                expense_date,
                category,
                description,
                amount
            )

            st.success("Expense added successfully.")


# -----------------------------
# DATA
# -----------------------------

df = get_dataframe()

if df.empty:
    st.warning("No expenses available.")
    st.stop()


# -----------------------------
# FILTER
# -----------------------------

st.subheader("Filter Expenses")

selected_category = st.selectbox(
    "Select category",
    ["All"] + sorted(df["Category"].unique().tolist())
)

if selected_category != "All":
    filtered_df = df[
        df["Category"] == selected_category
    ]
else:
    filtered_df = df


# -----------------------------
# METRICS
# -----------------------------

total_spent = calculate_total(
    filtered_df.to_dict("records")
)

average_expense = filtered_df["Amount"].mean()

largest_expense = filtered_df["Amount"].max()

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Spent",
    f"£{total_spent:.2f}"
)

col2.metric(
    "Average Expense",
    f"£{average_expense:.2f}"
)

col3.metric(
    "Largest Expense",
    f"£{largest_expense:.2f}"
)


# -----------------------------
# TABLE
# -----------------------------

st.divider()

st.subheader("Expense History")

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)


# -----------------------------
# CATEGORY ANALYSIS
# -----------------------------

st.divider()

st.subheader("Spending by Category")

category_summary = (
    filtered_df
    .groupby("Category")["Amount"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(category_summary)


# -----------------------------
# MOST EXPENSIVE CATEGORY
# -----------------------------

if not category_summary.empty:

    most_expensive_category = category_summary.idxmax()

    most_expensive_amount = category_summary.max()

    st.info(
        f"Highest spending category: "
        f"{most_expensive_category} "
        f"(£{most_expensive_amount:.2f})"
    )


# -----------------------------
# CLEAR DATA
# -----------------------------

st.divider()

if st.button("Clear All Expenses"):
    st.session_state.expenses = []
    st.rerun()