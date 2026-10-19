import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import streamlit as st

def plot_category_distribution(expenses):
    if not expenses:
        st.info("No expenses to show.")
        return
    
    df = pd.DataFrame(expenses)
    category_sum = df.groupby('category')['amount'].sum()
    
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(category_sum, labels=category_sum.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax.set_title("Expense Distribution by Category",fontsize=15,fontweight="bold",pad=20)
    ax.legend()
    st.pyplot(fig)

def plot_expenses_over_time(expenses):
    if not expenses:
        st.info("No expenses to show.")
        return
    
    df = pd.DataFrame(expenses)
    df['date'] = pd.to_datetime(df['date'])
    daily_sum = df.groupby('date')['amount'].sum()
    
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(daily_sum.index, daily_sum.values, marker='o', linestyle='-', color='b')
    ax.set_title("Expenses Over Time",fontsize=15,fontweight="bold",pad=20)
    ax.set_xlabel("Date")
    ax.set_ylabel("Amount")
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    st.pyplot(fig)

def plot_savings_vs_expenses(expenses, savings):
    if not expenses:
        st.info("No expenses to show.")
        return
    
    total_expenses = sum(e['amount'] for e in expenses) if expenses else 0
    total_savings = sum(s['amount'] for s in savings) if savings else 0
    
    labels = ['Expenses', 'Savings']
    values = [total_expenses, total_savings]
    colors = ['#ff9999', '#66b3ff']
    
    fig, ax = plt.subplots(figsize=(6, 4.8))
    ax.bar(labels, values, color=colors)
    ax.set_title("Expenses vs. Savings",fontsize=15,fontweight="bold",pad=20)
    ax.set_ylabel("Amount")
    
    for i, v in enumerate(values):
        ax.text(i, v , str(v), ha='center')
        
    st.pyplot(fig)

def plot_budget_vs_actual(budgets, expenses):
    if not budgets:
        st.info("No budgets set.")
        return

    # Aggregate expenses by category for the current month (assumed passed expenses are filtered or we filter here)
    # For simplicity, assuming 'expenses' passed to this function are relevant to the budget period or we do a quick filter
    # Ideally, expenses passed here should be ALL expenses to match budget month, or pre-filtered. 
    # Let's assume pre-filtered for better modularity or do a quick internal summation if full list.
    
    # We will assume 'expenses' is a list of ALL expenses and we filter by month of the budget
    # Actually, simpler to pass a DF or aggregated data. Let's do aggregation here.
    
    df_exp = pd.DataFrame(expenses)
    if df_exp.empty:
        expense_map = {}
    else:
        # We need to match budget month/year. Let's pick the FIRST budget's month/year as the target for visualization
        target_month = budgets[0]['month']
        target_year = budgets[0]['year']
        
        df_exp['date'] = pd.to_datetime(df_exp['date'])
        mask = (df_exp['date'].dt.month == target_month) & (df_exp['date'].dt.year == target_year)
        df_filtered = df_exp[mask]
        expense_map = df_filtered.groupby('category')['amount'].sum().to_dict()

    categories = [b['category'] for b in budgets]
    budget_vals = [b['amount'] for b in budgets]
    actual_vals = [expense_map.get(cat, 0) for cat in categories]
    
    x = np.arange(len(categories))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(10, 5))
    rects1 = ax.bar(x - width/2, budget_vals, width, label='Budget', color='lightgreen')
    rects2 = ax.bar(x + width/2, actual_vals, width, label='Actual', color='salmon')
    
    ax.set_ylabel('Amount')
    ax.set_title('Budget vs Actual (Current Month)',fontsize=15,fontweight="bold",pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.legend()
    
    st.pyplot(fig)
