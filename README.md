# Expense Tracker

A modern, responsive expense tracking web application built with Flask and MySQL. Track your daily expenses, categorize spending, and visualize your financial data with interactive charts.

## 🚀 Live Demo

**[View Live App](https://expense-tracker-1-3uu4.onrender.com/)**

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Flask](https://img.shields.io/badge/Flask-3.x-green)
![MySQL](https://img.shields.io/badge/MySQL-8.x-orange)

## Features

- **Add Expenses** - Record expenses with description, amount, category, and date
- **Edit & Delete** - Modify or remove existing expense entries
- **Filter Data** - Filter expenses by date range and category
- **Visual Analytics** - Interactive pie chart and bar chart for spending visualization
- **Responsive Design** - Modern dark-themed UI built with Tailwind CSS
- **Real-time Total** - Automatically calculates total based on applied filters

## Tech Stack

- **Backend**: Flask, SQLAlchemy
- **Database**: MySQL (via PyMySQL)
- **Frontend**: HTML, Tailwind CSS, Chart.js
- **Templating**: Jinja2

## Categories

- Food
- Transport
- Utilities
- Entertainment
- Rent
- Other

## Installation

### Prerequisites

- Python 3.x
- MySQL Server

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/csonal0947/Expense-Tracker.git
   cd Expense-Tracker
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install flask flask-sqlalchemy pymysql
   ```

4. **Set up MySQL database**
   ```sql
   CREATE DATABASE expenses_db;
   ```

5. **Configure database connection** (in `app.py`)
   ```python
   app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root@localhost:3306/expenses_db"
   ```

6. **Run the application**
   ```bash
   python3 app.py
   ```

7. **Open in browser**
   ```
   http://127.0.0.1:5000
   ```

## Project Structure

```
Expense-Tracker/
├── app.py              # Main Flask application
├── templates/
│   ├── base.html       # Base template
│   ├── index.html      # Dashboard with expense list and charts
│   └── edit.html       # Edit expense form
├── .gitignore
├── .flaskenv
└── README.md
```

## Screenshots

The application features:
- A clean dashboard with filters and expense form
- Expense table with edit/delete actions
- Pie chart showing spending by category
- Bar chart displaying spending trends

## License

This project is open source and available under the [MIT License](LICENSE).

## Author

**Sonal**

---

⭐ Star this repo if you find it helpful!
