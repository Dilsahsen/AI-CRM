AI-CRM: Intelligent Customer & Sales Management System
CS50x 2025 Final Project – by Dilşah Şen
AI-CRM is a full-stack CRM platform built using Flask, SQLite, SQLAlchemy, and Chart.js.
It includes authentication, security protections, customer management, sales tracking, and a modern dashboard with analytics.
This project was built as the final project for Harvard’s CS50x (2025).

🚀 Features

🔐 1. Authentication System

Register / Login / Logout
Remember-Me functionality
Secure password hashing
5 failed attempts lockout (5-minute block)
Automatic security email notifications
Password reset flow (email-based)

👥 2. Customer Management (CRUD)

Add customers
Edit customers
List all customers
Delete customers
Timestamp tracking (created_at)

💸 3. Sales Management (CRUD)

Add sales records
Edit sales
Delete sales
Link each sale to a customer
Track amount, currency, status, date, and notes

📊 4. Analytics Dashboard

Total number of customers
Total revenue
Sales in last 30 days
Win rate (%)
Recent customer list
Failed logins & security logs
Interactive line chart (Chart.js) showing last 7 days of sales

🧱 5. Clean Architecture (Blueprints + Forms + Models)

Modular Flask structure:

/routes
/models
/forms
/utils
/templates
/static

🗂 Project Structure

AI-CRM/
│
├── app.py
├── config.py
├── extensions.py
│
├── models/
│   ├── user.py
│   ├── customer.py
│   ├── sale.py
│
├── routes/
│   ├── auth.py
│   ├── dashboard.py
│   ├── customers.py
│   ├── sales.py
│
├── forms/
│   ├── auth_forms.py
│   ├── customer_forms.py
│   ├── sale_forms.py
│
├── utils/
│   └── email.py
│
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── auth/
│   ├── sales/
│   ├── email/
│
└── static/
    ├── styles.css
    ├── js/main.js


🧪 How to Run Locally

1️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Run the App
python app.py

4️⃣ Open in Browser
http://127.0.0.1:5000


📌 Why This Project? 

I built AI-CRM to learn how real-world CRM systems work and to deepen my knowledge of backend development, user authentication, relational databases, blueprints, forms, and security. It allowed me to turn a real business idea into a full-stack Flask application.


🌟 Technologies Used

Python
Flask
SQLite
SQLAlchemy ORM
WTForms
Jinja2
Chart.js
HTML/CSS
Werkzeug security

🙏 Acknowledgements
Special thanks to the CS50 staff and to everyone who supported this project 💙


