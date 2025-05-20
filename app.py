import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

# Connect to DB and load data
@st.cache_data
def load_data():
    conn = sqlite3.connect('expenses.db')
    query = """
        SELECT * FROM (
            SELECT * FROM expenses_01
            UNION ALL SELECT * FROM expenses_02
            UNION ALL SELECT * FROM expenses_03
            UNION ALL SELECT * FROM expenses_04
            UNION ALL SELECT * FROM expenses_05
            UNION ALL SELECT * FROM expenses_06
            UNION ALL SELECT * FROM expenses_07
            UNION ALL SELECT * FROM expenses_08
            UNION ALL SELECT * FROM expenses_09
            UNION ALL SELECT * FROM expenses_10
            UNION ALL SELECT * FROM expenses_11
            UNION ALL SELECT * FROM expenses_12
        )
    """
    df = pd.read_sql_query(query, conn, parse_dates=['date'])
    conn.close()
    return df

df = load_data()

st.title("Expense Tracking and Financial Analysis Dashboard")

# Sidebar filters
months = sorted(df['date'].dt.strftime('%Y-%m').unique())
categories = sorted(df['category'].unique())
payment_modes = sorted(df['payment_mode'].unique())

selected_month = st.sidebar.selectbox("Select Month (YYYY-MM)", options=["All"] + months)
selected_category = st.sidebar.selectbox("Select Category", options=["All"] + categories)
selected_payment_mode = st.sidebar.selectbox("Select Payment Mode", options=["All"] + payment_modes)

# Filtering dataframe based on user input
filtered_df = df.copy()

if selected_month != "All":
    filtered_df = filtered_df[filtered_df['date'].dt.strftime('%Y-%m') == selected_month]

if selected_category != "All":
    filtered_df = filtered_df[filtered_df['category'] == selected_category]

if selected_payment_mode != "All":
    filtered_df = filtered_df[filtered_df['payment_mode'] == selected_payment_mode]

# Show key metrics
total_spent = filtered_df['amount_paid'].sum()
total_cashback = filtered_df['cashback'].sum()
transaction_count = filtered_df.shape[0]

st.metric("Total Spent", f"${total_spent:,.2f}")
st.metric("Total Cashback Received", f"${total_cashback:,.2f}")
st.metric("Number of Transactions", transaction_count)

# Visualizations

# 1. Spending by category (bar chart)
st.subheader("Spending by Category")
category_spend = filtered_df.groupby('category')['amount_paid'].sum().sort_values(ascending=False)
fig1, ax1 = plt.subplots()
sns.barplot(x=category_spend.values, y=category_spend.index, palette='viridis', ax=ax1)
ax1.set_xlabel("Amount Spent")
ax1.set_ylabel("Category")
st.pyplot(fig1)

# 2. Spending over time (line chart by month)
st.subheader("Monthly Spending Trend")
monthly_spend = df.groupby(df['date'].dt.to_period('M'))['amount_paid'].sum()
monthly_spend.index = monthly_spend.index.astype(str)
fig2, ax2 = plt.subplots()
sns.lineplot(x=monthly_spend.index, y=monthly_spend.values, marker='o', ax=ax2)
ax2.set_xlabel("Month")
ax2.set_ylabel("Total Amount Spent")
ax2.tick_params(axis='x', rotation=45)
st.pyplot(fig2)

# 3. Payment mode distribution (pie chart)
st.subheader("Payment Mode Distribution")
payment_counts = filtered_df['payment_mode'].value_counts()
fig3, ax3 = plt.subplots()
ax3.pie(payment_counts, labels=payment_counts.index, autopct='%1.1f%%', startangle=140)
ax3.axis('equal')
st.pyplot(fig3)

# 4. Top 10 highest transactions
st.subheader("Top 10 Highest Transactions")
top_transactions = filtered_df.nlargest(10, 'amount_paid')[['date', 'category', 'payment_mode', 'description', 'amount_paid', 'cashback']]
st.dataframe(top_transactions)

# 5. Transactions with cashback > 0
st.subheader("Transactions with Cashback")
cashback_transactions = filtered_df[filtered_df['cashback'] > 0].sort_values(by='cashback', ascending=False)
st.dataframe(cashback_transactions.head(10))

st.markdown("---")
st.markdown("Developed by YourName | Powered by Streamlit")

