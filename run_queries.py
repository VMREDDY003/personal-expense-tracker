import sqlite3
import pandas as pd

conn = sqlite3.connect('expenses.db')

# We'll union all months into one view for easier queries
union_all_months = """
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
"""

# Create a temporary view in SQLite
conn.execute("DROP VIEW IF EXISTS all_expenses")
conn.execute(f"CREATE VIEW all_expenses AS {union_all_months}")

# Helper function to run and print queries with pandas
def run_query(query, description):
    print(f"\n--- {description} ---")
    df = pd.read_sql_query(query, conn)
    print(df)
    return df

# 1. Total amount spent in each category
query1 = "SELECT category, ROUND(SUM(amount_paid), 2) as total_spent FROM all_expenses GROUP BY category ORDER BY total_spent DESC"
run_query(query1, "Total amount spent in each category")

# 2. Total amount spent using each payment mode
query2 = "SELECT payment_mode, ROUND(SUM(amount_paid), 2) as total_spent FROM all_expenses GROUP BY payment_mode"
run_query(query2, "Total amount spent using each payment mode")

# 3. Total cashback received across all transactions
query3 = "SELECT ROUND(SUM(cashback), 2) as total_cashback FROM all_expenses"
run_query(query3, "Total cashback received across all transactions")

# 4. Top 5 most expensive categories by spending
query4 = "SELECT category, ROUND(SUM(amount_paid), 2) as total_spent FROM all_expenses GROUP BY category ORDER BY total_spent DESC LIMIT 5"
run_query(query4, "Top 5 most expensive categories")

# 5. Amount spent on transportation using different payment modes
query5 = """
    SELECT payment_mode, ROUND(SUM(amount_paid), 2) as total_spent
    FROM all_expenses WHERE category = 'Transportation'
    GROUP BY payment_mode
"""
run_query(query5, "Amount spent on Transportation by payment mode")

# 6. Transactions that resulted in cashback
query6 = "SELECT * FROM all_expenses WHERE cashback > 0 LIMIT 10"
run_query(query6, "Sample transactions with cashback")

# 7. Total spending in each month
query7 = """
    SELECT substr(date, 6, 2) as month, ROUND(SUM(amount_paid), 2) as total_spent
    FROM all_expenses GROUP BY month ORDER BY month
"""
run_query(query7, "Total spending in each month")

# 8. Months with highest spending in Travel, Entertainment, Gifts
query8 = """
    SELECT substr(date, 6, 2) as month, category, ROUND(SUM(amount_paid), 2) as total_spent
    FROM all_expenses
    WHERE category IN ('Travel', 'Entertainment', 'Gifts')
    GROUP BY month, category ORDER BY total_spent DESC
"""
run_query(query8, "Monthly spending in Travel, Entertainment, Gifts")

# 9. Recurring expenses during specific months (e.g. insurance premiums, property taxes)
# Our dataset may not have those exact descriptions, so simulate recurring by description with multiple entries in different months
query9 = """
    SELECT description, COUNT(DISTINCT substr(date, 6, 2)) as months_occured
    FROM all_expenses
    GROUP BY description HAVING months_occured > 1 ORDER BY months_occured DESC LIMIT 10
"""
run_query(query9, "Recurring expenses across months")

# 10. Cashback or rewards earned in each month
query10 = """
    SELECT substr(date, 6, 2) as month, ROUND(SUM(cashback), 2) as total_cashback
    FROM all_expenses GROUP BY month ORDER BY month
"""
run_query(query10, "Monthly cashback earned")

# 11. Overall spending trend over time (month-wise total)
query11 = """
    SELECT substr(date, 6, 2) as month, ROUND(SUM(amount_paid), 2) as total_spent
    FROM all_expenses GROUP BY month ORDER BY month
"""
run_query(query11, "Overall spending trend over time")

# 12. Typical costs associated with travel types (Assuming descriptions contain keywords like flight, hotel, taxi)
query12 = """
    SELECT 
        CASE
            WHEN description LIKE '%flight%' THEN 'Flight'
            WHEN description LIKE '%hotel%' THEN 'Accommodation'
            WHEN description LIKE '%taxi%' OR description LIKE '%cab%' THEN 'Transportation'
            ELSE 'Other'
        END as travel_type,
        ROUND(AVG(amount_paid), 2) as avg_cost
    FROM all_expenses
    WHERE category = 'Travel'
    GROUP BY travel_type
"""
run_query(query12, "Typical costs by travel types")

# 13. Grocery spending patterns (weekends vs weekdays)
query13 = """
    SELECT 
        CASE 
            WHEN strftime('%w', date) IN ('0','6') THEN 'Weekend'
            ELSE 'Weekday'
        END as day_type,
        ROUND(SUM(amount_paid), 2) as total_spent
    FROM all_expenses
    WHERE category = 'Groceries'
    GROUP BY day_type
"""
run_query(query13, "Grocery spending on weekends vs weekdays")

# 14. Define high and low priority categories by spending thresholds
query14 = """
    SELECT category,
    ROUND(SUM(amount_paid), 2) as total_spent,
    CASE 
        WHEN SUM(amount_paid) > (SELECT SUM(amount_paid)*0.1 FROM all_expenses) THEN 'High Priority'
        ELSE 'Low Priority'
    END as priority
    FROM all_expenses
    GROUP BY category
    ORDER BY total_spent DESC
"""
run_query(query14, "High vs Low Priority Categories")

# 15. Category contributing highest percentage of total spending
query15 = """
    SELECT category,
        ROUND(SUM(amount_paid), 2) as total_spent,
        ROUND((SUM(amount_paid)*100.0) / (SELECT SUM(amount_paid) FROM all_expenses), 2) as percent_total
    FROM all_expenses
    GROUP BY category
    ORDER BY total_spent DESC
    LIMIT 1
"""
run_query(query15, "Category with highest % of total spending")

# 10 Additional Insightful Queries:

# 16. Average transaction amount per category
query16 = """
    SELECT category, ROUND(AVG(amount_paid), 2) as avg_transaction
    FROM all_expenses GROUP BY category ORDER BY avg_transaction DESC
"""
run_query(query16, "Average transaction amount per category")

# 17. Number of transactions per payment mode
query17 = """
    SELECT payment_mode, COUNT(*) as transaction_count
    FROM all_expenses GROUP BY payment_mode
"""
run_query(query17, "Number of transactions per payment mode")

# 18. Largest single transaction in each category
query18 = """
    SELECT category, MAX(amount_paid) as largest_transaction
    FROM all_expenses GROUP BY category ORDER BY largest_transaction DESC
"""
run_query(query18, "Largest single transaction per category")

# 19. Total cashback as percentage of total spending per category
query19 = """
    SELECT category,
        ROUND(SUM(cashback), 2) as total_cashback,
        ROUND((SUM(cashback)*100.0)/SUM(amount_paid), 2) as cashback_percent
    FROM all_expenses
    GROUP BY category
    ORDER BY cashback_percent DESC
"""
run_query(query19, "Cashback % of spending by category")

# 20. Months with zero cashback received
query20 = """
    SELECT substr(date,6,2) as month
    FROM all_expenses
    GROUP BY month
    HAVING SUM(cashback) = 0
"""
run_query(query20, "Months with zero cashback received")

conn.close()
