# 💰 Expense Tracker Pro

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
  <img src="https://img.shields.io/badge/MySQL-Database-4479A1?style=for-the-badge&logo=mysql&logoColor=white"/>
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge"/>
</p>

<p align="center">
  A comprehensive, all-in-one personal finance management application built with <strong>Python</strong> and <strong>Streamlit</strong>.<br/>
  Track expenses, manage savings, plan budgets, monitor investments, and set financial goals — in one clean interface.
</p>

---

## ✨ Features

| Feature | Description |
|---|---|
| 📊 **Dashboard** | Financial health score, key metrics & interactive charts |
| 📝 **Transactions** | Log Expenses, Savings, Subscriptions, Investments & Goals |
| 📅 **Budgeting** | Set monthly category limits and track adherence |
| 📉 **Analytics** | Heatmaps, trend lines & spending predictions |
| 🏦 **Bank Statement** | Downloadable TXT statement of your full history |
| 🎯 **Goals Tracker** | Visual progress bars for your financial goals |
| 🔒 **Authentication** | Secure login/signup with hashed passwords |

---

## 🛠️ Tech Stack

- **Frontend / UI** — [Streamlit](https://streamlit.io/)
- **Backend** — Python 3.8+
- **Database** — MySQL
- **Data Analysis** — Pandas, NumPy
- **Visualization** — Matplotlib

---

## 🚀 Getting Started

### Prerequisites

- Python **3.8+**
- **MySQL Server** installed and running locally

### 1. Clone the Repository

```bash
git clone https://github.com/Varshil0611/Expense-Tracker-System.git
cd Expense-Tracker-System
```

### 2. Create a Virtual Environment (Recommended)

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Database

The app connects to a local MySQL server with these **default** credentials:

| Setting | Default Value |
|---|---|
| Host | `localhost` |
| User | `root` |
| Password | *(empty)* |
| Database | `expense_tracker_db` *(auto-created)* |

> **⚠️ Note:** If your MySQL setup uses a different username or password, update the `create_connection()` function in [`database.py`](database.py).

The database schema (tables) is **automatically created** on first run. Alternatively, you can run it manually:

```bash
mysql -u root -p < schema.sql
```

### 5. Run the Application

```bash
streamlit run main.py
```

The app will open automatically at **http://localhost:8501** 🎉

---

## 📂 Project Structure

```
Expense-Tracker-System/
│
├── main.py            # App entry point & all page UI logic
├── auth.py            # User authentication (login / signup)
├── database.py        # MySQL connection & query helper
├── operations.py      # Core business logic & CRUD operations
├── visualizations.py  # Matplotlib chart functions
├── schema.sql         # SQL schema for manual DB setup
├── requirements.txt   # Python dependencies
└── README.md
```

---

## 📸 Screenshots

> *Run the app locally and explore the Dashboard, Transactions, and Goals pages!*

---

## 🤝 Contributing

Contributions, issues and feature requests are welcome!

1. Fork the repo
2. Create a new branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a **Pull Request**

---

## 📄 License

This project is licensed under the **MIT License** — feel free to use and modify it.

---

<p align="center">Made with ❤️ using Python & Streamlit</p>
