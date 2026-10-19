import streamlit as st
import pandas as pd
from datetime import date

import auth
import database
import operations
import visualizations


# Page Config
st.set_page_config(page_title="Expense Tracker Pro", page_icon="🏷️", layout="wide")


# Session State Initialization
if 'user' not in st.session_state:
    st.session_state.user = None

def login_page():
    st.title("🏷️ Expense Tracker Pro")
    st.subheader("Secure Login")
    
    col1, col2 = st.tabs(["Login", "Sign Up"])
    
    with col1:
        st.markdown("### Sign In")
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            user = auth.login_user(username, password)
            if user:
                st.session_state.user = user
                st.success(f"Welcome back, {user['name']}!")
                st.rerun()
            else:
                st.error("Invalid Username or Password")

    with col2:
        st.markdown("### New User? Sign Up")
        new_user = st.text_input("Username", key="create_user")
        new_pass = st.text_input("Password", type="password", key="create_pass")
        new_name = st.text_input("Display Name", key="create_name")
        if st.button("Create Account"):
            if auth.create_user(new_user, new_pass, new_name):
                st.success("Account created! Please log in.")
            else:
                st.error("Username already exists or error occurred.")

def dashboard_page():
    user_id = st.session_state.user['id']
    st.title(f"Dashboard - {st.session_state.user['name']}")
    
    # Key Metrics
    expenses = operations.get_expenses(user_id)
    savings = operations.get_savings(user_id)
    
    total_expense = sum(e['amount'] for e in expenses) if expenses else 0
    total_savings = sum(s['amount'] for s in savings) if savings else 0
    health_score = operations.get_financial_health_score(user_id)
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    col1.metric("Financial Health", f"{health_score}/100", delta_color="normal")
    col2.metric("Total Savings", f" ₹{total_savings:,.2f}", delta_color="normal")
    col3.metric("Total Expenses", f" ₹{total_expense:,.2f}", delta="-High" if total_expense > total_savings else "normal")

    
    st.markdown("---")
    
    # Graphs Row 1
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Spending by Category")
        visualizations.plot_category_distribution(expenses)
    with c2:
        st.subheader("Spending vs Savings")
        visualizations.plot_savings_vs_expenses(expenses, savings)
        
    # Graphs Row 2
    st.subheader("Expense Trend & Heatmap")
    visualizations.plot_expenses_over_time(expenses)
 

def transaction_page():
    st.title("Add New Transaction")
    user_id = st.session_state.user['id']
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Expense", "Saving", "Subscription", "Investment", "Goal"])
    
    with tab1:
        with st.form("expense_form"):
            name = st.text_input("Short Title")
            desc = st.text_area("Long Description (Optional)", height=100)
            category = st.selectbox("Category", ["Food", "Transport", "Utilities", "Entertainment", "Health", "Other"])
            amount = st.number_input("Amount", min_value=1)
            d = st.date_input("Date", date.today())
            if st.form_submit_button("Add Expense"):
                operations.add_expense(user_id, name, category, amount, d,desc)
                st.toast("Expense Added Successfully! 🎉", icon="✅")
                st.success("Expense Added!")

    with tab2:
        with st.form("saving_form"):
            name = st.text_input("Source/Title")
            desc = st.text_area("Details (Optional)", height=100)
            amount = st.number_input("Amount", min_value=1)
            d = st.date_input("Date", date.today())
            if st.form_submit_button("Add Saving"):
                operations.add_saving(user_id, name, amount, d, desc)
                st.toast("Saving Added Successfully! 🎉", icon="✅")
                st.success("Saving Added!")

    with tab3:
        with st.form("sub_form"):
            name = st.text_input("Service Name (e.g. Netflix)")
            amount = st.number_input("Amount", min_value=1)
            freq = st.selectbox("Frequency", ["Monthly", "Yearly"])
            due = st.date_input("Next Due Date")
            if st.form_submit_button("Add Subscription"):
                operations.add_subscription(user_id, name, amount, freq, due)
                st.success("Subscription Added!")

    with tab4:
        with st.form("inv_form"):
            name = st.text_input("Asset Name")
            type = st.selectbox("Type", ["Stock", "Crypto", "Real Estate", "Mutual Fund", "Gold"])
            amount = st.number_input("Invested Amount", min_value=1)
            d = st.date_input("Date Invested", date.today())
            if st.form_submit_button("Add Investment"):
                operations.add_investment(user_id, name, type, amount, d)
                st.success("Investment Added!")
    
    with tab5:
        with st.form("goal_form"):
            name = st.text_input("Goal Name (e.g. Vacation)")
            target = st.number_input("Target Amount", min_value=1)
            deadline = st.date_input("Deadline")
            if st.form_submit_button("Create Goal"):
                operations.add_goal(user_id, name, target, deadline)
                st.success("Goal Created!")

def bank_statement_page():
    st.title("Bank Statement View")
    user_id = st.session_state.user['id']
    
    st.info("Here is a consolidated text view of your finances, similar to a bank statement.")
    
    statement_text = operations.get_statement_string(user_id)
    
    st.text_area("Statement", statement_text, height=400)
    
    st.download_button(
        label="Download Statement as TXT",
        data=statement_text,
        file_name="bank_statement.txt",
        mime="text/plain"
    )

def budgeting_page():
    st.title("Budget Management")
    user_id = st.session_state.user['id']
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Set Budget")
        with st.form("budget_form"):
            cat = st.selectbox("Category", ["Food", "Transport", "Utilities", "Entertainment", "Health", "Other"])
            amt = st.number_input("Monthly Limit", min_value=1.0)
            month = st.number_input("Month", 1, 12, date.today().month)
            year = st.number_input("Year", 2020, 2030, date.today().year)
            if st.form_submit_button("Set Budget"):
                operations.set_budget(user_id, cat, amt, month, year)
                st.success("Budget Updated!")
                
    with col2:
        st.subheader("Budget vs Actuals")
        # Fetch budgets for default current month context or selected above
        current_month = date.today().month
        current_year = date.today().year
        budgets = operations.get_budgets(user_id, current_month, current_year)
        expenses = operations.get_expenses(user_id) # Should filter this inside plot or here
        visualizations.plot_budget_vs_actual(budgets, expenses)

    
def goals_page():
    st.title("Financial Goals Tracking")
    user_id = st.session_state.user['id']
    
    goals = operations.get_goals(user_id)
    if not goals:
        st.info("No goals set yet. Go to 'Add Transaction' > 'Goal' tab.")
    else:
        for g in goals:
            perc = min(1.0, float(g['current_amount']) / float(g['target_amount']))
            st.write(f"### {g['name']}")
            st.progress(perc)
            st.write(f"Progress: ${g['current_amount']} / ${g['target_amount']}")
            
            with st.expander("Update Progress"):
                new_val = st.number_input(f"New Total for {g['name']}", value=float(g['current_amount']), key=f"g_{g['id']}")
                if st.button("Update", key=f"btn_{g['id']}"):
                    operations.update_goal_progress(g['id'], new_val)
                    st.rerun()

def main():
    if st.session_state.user:
        # User is logged in, show Sidebar Navigation
        with st.sidebar:
            st.title(f"Hello, {st.session_state.user['username']}")
            menu = st.radio("Navigation", 
                ["Dashboard", "Add Transaction", "Bank Statement", "Budgeting", "Goals","Manage"])
            
            st.markdown("---")
            if st.button("Logout"):
                st.session_state.user = None
                st.rerun()
                
        if menu == "Dashboard":
            dashboard_page()
        elif menu == "Add Transaction":
            transaction_page()
        elif menu == "Bank Statement":
            bank_statement_page()
        elif menu == "Budgeting":
            budgeting_page()
        elif menu == "Goals":
            goals_page()
        elif menu == "Manage":
            st.title("Manage Records")
            st.warning("Feature to edit/delete individual records allows detailed cleanup.")
            # Simple delete implementation for demo
            user_id = st.session_state.user['id']
            expenses = operations.get_expenses(user_id)
            if expenses:
                st.subheader("Edit/Delete Transactions")
                
                # Interactive Data Editor
                df = pd.DataFrame(expenses)
                st.data_editor(df, num_rows="dynamic", key="data_editor")
                
                st.divider()
                st.write("### Quick Delete")
                
                exp_to_del = st.selectbox("Select Expense to Delete", options=expenses, format_func=lambda x: f"{x['date']} - {x['name']} ( ₹{x['amount']})")
                if st.button("Delete Selected Expense", use_container_width=True):
                    operations.delete_expense(exp_to_del['id'])
                    st.toast("Deleted! 🗑️")
                    st.rerun()
            else:
                st.info("No expenses to delete.")

    else:
        # Not logged in
        login_page()

if __name__ == "__main__":
    main()