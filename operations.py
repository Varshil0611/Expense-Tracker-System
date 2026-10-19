import database
import numpy as np
import pandas as pd
from datetime import datetime
import streamlit as st


# ==========================================
# EXPENSES
# ==========================================
def add_expense(user_id, name, category, amount, date, description=""):
    query = "INSERT INTO expenses (user_id, name, category, amount, date, description) VALUES (%s, %s, %s, %s, %s, %s)"
    return database.run_query(query, (user_id, name, category, amount, date, description))

def get_expenses(user_id):
    query = "SELECT * FROM expenses WHERE user_id = %s ORDER BY date DESC"
    return database.run_query(query, (user_id,))

def delete_expense(expense_id):
    query = "DELETE FROM expenses WHERE id = %s"
    return database.run_query(query, (expense_id,))

def update_expense(expense_id, name, category, amount, date, time):
    query = "UPDATE expenses SET name=%s, category=%s, amount=%s, date=%s, time=%s WHERE id=%s"
    return database.run_query(query, (name, category, amount, date, time, expense_id))

# ==========================================
# SAVINGS
# ==========================================
def add_saving(user_id, name, amount, date, description=""):
    query = "INSERT INTO savings (user_id, name, amount, date, description) VALUES (%s, %s, %s, %s, %s)"
    return database.run_query(query, (user_id, name, amount, date, description))

def get_savings(user_id):
    query = "SELECT * FROM savings WHERE user_id = %s ORDER BY date DESC"
    return database.run_query(query, (user_id,))

def delete_saving(saving_id):
    query = "DELETE FROM savings WHERE id = %s"
    return database.run_query(query, (saving_id,))

# ==========================================
# BUDGETS
# ==========================================
def set_budget(user_id, category, amount, month, year):
    # Check if budget exists, if so update, else insert
    query = "INSERT INTO budgets (user_id, category, amount, month, year) VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE amount=%s"
    return database.run_query(query, (user_id, category, amount, month, year, amount))

def get_budgets(user_id, month, year):
    query = "SELECT * FROM budgets WHERE user_id = %s AND month = %s AND year = %s"
    return database.run_query(query, (user_id, month, year))

# ==========================================
# SUBSCRIPTIONS
# ==========================================
def add_subscription(user_id, name, amount, frequency, next_due_date):
    query = "INSERT INTO subscriptions (user_id, name, amount, frequency, next_due_date) VALUES (%s, %s, %s, %s, %s)"
    return database.run_query(query, (user_id, name, amount, frequency, next_due_date))

def get_subscriptions(user_id):
    query = "SELECT * FROM subscriptions WHERE user_id = %s"
    return database.run_query(query, (user_id,))

def delete_subscription(sub_id):
    query = "DELETE FROM subscriptions WHERE id = %s"
    return database.run_query(query, (sub_id,))

# ==========================================
# INVESTMENTS
# ==========================================
def add_investment(user_id, name, type, amount, date):
    query = "INSERT INTO investments (user_id, name, type, amount_invested, date_invested) VALUES (%s, %s, %s, %s, %s)"
    return database.run_query(query, (user_id, name, type, amount, date))

def get_investments(user_id):
    query = "SELECT * FROM investments WHERE user_id = %s ORDER BY date_invested DESC"
    return database.run_query(query, (user_id,))

# ==========================================
# GOALS
# ==========================================
def add_goal(user_id, name, target_amount, deadline):
    query = "INSERT INTO goals (user_id, name, target_amount, deadline) VALUES (%s, %s, %s, %s)"
    return database.run_query(query, (user_id, name, target_amount, deadline))

def update_goal_progress(goal_id, current_amount):
    query = "UPDATE goals SET current_amount = %s WHERE id = %s"
    return database.run_query(query, (current_amount, goal_id))

def get_goals(user_id):
    query = "SELECT * FROM goals WHERE user_id = %s"
    return database.run_query(query, (user_id,))


# ==========================================
# ANALYTICS & INSIGHTS
# ==========================================
def get_financial_health_score(user_id):
    """
    Calculates a score (0-100) based on savings vs expenses ratio using numpy.
    """
    
    expenses = get_expenses(user_id)
    savings = get_savings(user_id)
    
    total_expense = sum(float(e['amount']) for e in expenses) if expenses else 0
    total_savings = sum(float(s['amount']) for s in savings) if savings else 0
    
    if total_expense == 0 and total_savings == 0:
        st.info("No expenses to show.")
        return 50 # Neutral start
        
    income = total_expense + total_savings
    if income == 0: return 50
    
    savings_rate = (total_savings / income) * 100
    
    # Simple logic: 20% savings is good (score 80), 0% is bad (score 20)
    score = np.interp(savings_rate, [0, 10, 20, 50], [20, 50, 80, 100])
    return round(score)

    """
    Predicts next month's expense usage using linear regression.
    """
    expenses = get_expenses(user_id)
    if not expenses:
        return 0
    
    df = pd.DataFrame(expenses)
    df['date'] = pd.to_datetime(df['date'])
    df['month_int'] = df['date'].dt.month + (df['date'].dt.year * 12)
    
    monthly_totals = df.groupby('month_int')['amount'].sum().reset_index()
    
    if len(monthly_totals) < 2:
        return monthly_totals['amount'].iloc[0] if not monthly_totals.empty else 0
        
    X = monthly_totals['month_int'].values
    y = monthly_totals['amount'].values
    
    # Linear Regression: y = mx + c
    A = np.vstack([X, np.ones(len(X))]).T
    m, c = np.linalg.lstsq(A, y, rcond=None)[0]
    
    next_month = X[-1] + 1
    prediction = m * next_month + c
    return max(0, round(prediction, 2))

def get_statement_string(user_id):
    expenses = get_expenses(user_id)
    savings = get_savings(user_id)
    
    lines = ["EXPENSE TRACKER - ACCOUNT STATEMENT", "="*40, ""]
    
    lines.append("--- EXPENSES ---")
    if expenses:
        for ex in expenses:
            lines.append(f"{ex['date']} | {ex['name']} ({ex['category']}): -{ex['amount']}")
    else:
        lines.append("No expenses recorded.")
        
    lines.append("")
    lines.append("--- SAVINGS ---")
    if savings:
        for sv in savings:
            lines.append(f"{sv['date']} | {sv['name']}: +{sv['amount']}")
    else:
        lines.append("No savings recorded.")
    
    return "\n".join(lines)
