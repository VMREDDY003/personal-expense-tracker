# Personal Expense Tracker and Financial Analysis

## Project Overview

This project simulates a personal expense tracker using Python, SQL, and Streamlit. It generates realistic monthly expense data with the Faker library, stores the data in an SQLite database, and performs SQL-based analysis to uncover spending habits. The project culminates in an interactive Streamlit web app that visualizes spending patterns and provides actionable financial insights.

---

## Features

- **Data Simulation**: Generates realistic monthly expenses across multiple categories (e.g., Food, Travel, Bills, Subscriptions) using Faker.
- **SQL Database**: Stores simulated data in an SQLite database with 12 monthly tables.
- **Exploratory Data Analysis (EDA)**: Runs SQL queries to analyze spending by category, payment mode, cashback received, and monthly trends.
- **Interactive Streamlit App**:
  - Filter expenses by month, category, and payment mode.
  - Visualize spending distribution with bar charts, pie charts, and line charts.
  - View detailed transaction tables including cashback details.
- **Insight Generation**: Identifies top spending categories, monthly expenditure trends, cashback earnings, and more.

---

## Tech Stack

- Python (Pandas, Faker, SQLite3, Matplotlib, Seaborn)
- SQL (SQLite)
- Streamlit (Web Application Framework)

---

## Dataset Description

The dataset is a simulated collection of personal expenses with the following fields:

| Column       | Description                                |
|--------------|--------------------------------------------|
| `date`       | Transaction date (YYYY-MM-DD)              |
| `category`   | Expense category (e.g., Food, Travel)      |
| `payment_mode` | Mode of payment (Cash or Online)           |
| `description`| Details about the expense                   |
| `amount_paid`| Total amount paid for the transaction      |
| `cashback`   | Cashback received (if any)                  |

---

## Installation & Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/personal-expense-tracker.git
   cd personal-expense-tracker
## Create a virtual environment and activate it (optional but recommended):

python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

## Install dependencies:
pip install -r requirements.txt

## Run the data generation and database setup script:

python data_generation.py

## Launch the Streamlit app:

streamlit run app.py
# Usage
- Use the sidebar filters in the app to select the desired month, category, or payment mode.

- Explore various charts and tables to analyze spending habits.

Gain insights into top spending areas, cashback trends, and monthly financial behavior.

# SQL Queries
- The project includes over 20 SQL queries that analyze:

- Total amount spent per category and payment mode.

- Monthly spending and cashback trends.

- Top 5 most expensive categories.

- Recurring expenses.

- Spending patterns on weekends vs. weekdays.

- And many more insights tailored to personal finance.

# Project Structure
| ├── app.py                   # Streamlit application code \
| ├── data_generation.py       # Script for data simulation and database population \
| ├── expenses.db              # SQLite database with expense data \
| ├── requirements.txt         # Python dependencies \
| ├── README.md                # Project documentation (this file) \
| └── sql_queries.sql          # All SQL queries used for analysis

