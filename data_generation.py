import sqlite3
from faker import Faker
import random
from datetime import datetime, timedelta

# Initialize Faker and DB connection
fake = Faker()
conn = sqlite3.connect('expenses.db')
cursor = conn.cursor()

# Expense categories and payment modes
categories = ['Food', 'Transportation', 'Bills', 'Groceries', 'Subscriptions', 'Entertainment', 'Travel', 'Gifts', 'Personal Care', 'Health']
payment_modes = ['Cash', 'Online']

# Create tables for each month
for month in range(1, 13):
    table_name = f'expenses_{month:02d}'
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            category TEXT,
            payment_mode TEXT,
            description TEXT,
            amount_paid REAL,
            cashback REAL
        )
    ''')
conn.commit()

def random_date(month):
    """Generate a random date in 2024 for the given month."""
    start_date = datetime(2024, month, 1)
    if month == 12:
        end_date = datetime(2024, 12, 31)
    else:
        end_date = datetime(2024, month + 1, 1) - timedelta(days=1)
    delta = end_date - start_date
    random_day = random.randint(0, delta.days)
    return (start_date + timedelta(days=random_day)).strftime('%Y-%m-%d')

def generate_expenses(month, num_records=100):
    """Generate a list of fake expenses for a given month."""
    expenses = []
    for _ in range(num_records):
        date = random_date(month)
        category = random.choice(categories)
        payment_mode = random.choice(payment_modes)
        description = fake.sentence(nb_words=5)
        amount_paid = round(random.uniform(5, 500), 2)
        cashback = round(amount_paid * random.choice([0, 0, 0.01, 0.02, 0.05]), 2)  # 0% to 5% cashback mostly zero
        expenses.append((date, category, payment_mode, description, amount_paid, cashback))
    return expenses

# Insert data into tables
for month in range(1, 13):
    table_name = f'expenses_{month:02d}'
    expenses = generate_expenses(month, num_records=100)
    cursor.executemany(f'''
        INSERT INTO {table_name} (date, category, payment_mode, description, amount_paid, cashback)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', expenses)
    conn.commit()

print("Data generation and insertion completed successfully!")

# Close connection
conn.close()
