# কারাগার — Jail Management System (JMS)

A Flask-based web application for managing a prison/jail facility. Built with Python, Flask, MySQL, and Bootstrap.

---

## Prerequisites

Before running this project, make sure the following are installed on your system:

1. **Python 3.10+** — Download from [python.org](https://www.python.org/downloads/)
   > ⚠️ During installation, **check the box that says "Add Python to PATH"**. This is critical.

2. **MySQL Server** — You can use any of these:
   - [XAMPP](https://www.apachefriends.org/) (easiest — comes with MySQL + phpMyAdmin)
   - [MySQL Community Server](https://dev.mysql.com/downloads/mysql/)
   - [WAMP](https://www.wampserver.com/)

---

## Step-by-Step Setup Guide

### Step 1: Start MySQL Server

- If using **XAMPP**: Open the XAMPP Control Panel → Click **Start** next to **MySQL**.
- If using standalone MySQL: Make sure the MySQL service is running.

> The app connects to MySQL with these defaults (defined in `app/config.py`):
> - Host: `localhost`
> - User: `root`
> - Password: *(empty — no password)*
> - Database: `JMS`
>
> If your MySQL has a different root password, edit `app/config.py` before proceeding.

---

### Step 2: Open Terminal in the Project Folder

Open **Command Prompt** or **PowerShell**, then navigate to the project folder:

```bash
cd "path\to\JMS"
```

For example, if you unzipped it to your Desktop:
```bash
cd "C:\Users\YourName\Desktop\JMS"
```

---

### Step 3: Create a Virtual Environment

```bash
python -m venv venv
```

This creates an isolated Python environment inside a `venv` folder.

---

### Step 4: Activate the Virtual Environment

**On Windows (CMD):**
```bash
venv\Scripts\activate
```

**On Windows (PowerShell):**
```bash
.\venv\Scripts\activate
```

**On Mac/Linux:**
```bash
source venv/bin/activate
```

You should see `(venv)` appear at the beginning of your terminal prompt.

---

### Step 5: Install Dependencies

```bash
pip install flask flask-mysqldb apscheduler werkzeug
```

---

### Step 6: Set Up the Database

You need to create the database and all its tables. Run this command:

```bash
python -c "import MySQLdb; db=MySQLdb.connect(host='localhost', user='root', password=''); cursor=db.cursor(); cursor.execute('CREATE DATABASE IF NOT EXISTS JMS'); db.commit(); sql=open('app/models/JMS.sql','r').read(); db.select_db('JMS'); [cursor.execute(stmt) for stmt in sql.split(';') if stmt.strip()]; db.commit(); cursor.close(); db.close(); print('Database and tables created successfully!')"
```

Or manually:
1. Open **phpMyAdmin** (http://localhost/phpmyadmin) or **MySQL Workbench**
2. Create a new database called `JMS`
3. Import the file `app/models/JMS.sql`

---

### Step 7: Create the Default Admin User

```bash
python create_admin.py
```

This creates an admin account with:
- **Username:** `admin`
- **Password:** `admin_password`

---

### Step 8: Run the Application

```bash
python run.py
```

You should see output like:
```
 * Serving Flask app 'app'
 * Running on http://127.0.0.1:5000
```

---

### Step 9: Open in Browser

Go to **http://127.0.0.1:5000** in your web browser.

Log in with:

| Role | Username | Password |
|------|----------|----------|
| Admin (full access) | `admin` | `admin_password` |

---

## Creating Additional Users

After logging in as admin, you can create more users by running:

```bash
python -c "from app import create_app, mysql; from werkzeug.security import generate_password_hash; app=create_app(); app.app_context().push(); cur=mysql.connection.cursor(); cur.execute('INSERT INTO users (username, password, role) VALUES (%s, %s, %s)', ('jailer', generate_password_hash('jailer_password'), 'jailer')); mysql.connection.commit(); cur.close(); print('Jailer user created!')"
```

This creates:

| Role | Username | Password |
|------|----------|----------|
| Jailer (limited access) | `jailer` | `jailer_password` |

---

## User Roles

| Role | Can Access |
|------|-----------|
| **Admin** | Dashboard, Visitors, Search, Notifications, Visit Requests, Assign Cell, Cells, Inmates, Transfers, Work Assignments, Punishments |
| **Jailer** | Dashboard, Visitors, Search, Notifications, Visit Requests, Assign Cell |
| **Public (no login)** | Visit Request form (`/visit_request`) — accessible from the login page |

---

## Project Structure

```
JMS/
├── app/
│   ├── __init__.py          # App factory & blueprint registration
│   ├── config.py            # Database configuration
│   ├── models/
│   │   └── JMS.sql          # Database schema
│   ├── routes/
│   │   ├── auth.py          # Login/logout & decorators
│   │   ├── dashboard.py     # Dashboard with stats & charts
│   │   ├── inmates.py       # Inmate CRUD
│   │   ├── visitors.py      # Visitor records
│   │   ├── visit_request.py # Public visit request system
│   │   ├── cells.py         # Cell management
│   │   ├── transfers.py     # Inmate transfers
│   │   ├── punishments.py   # Punishment records
│   │   ├── work_assignments.py # Work assignment tracking
│   │   ├── notifications.py # System notifications
│   │   ├── alerts.py        # Auto-generated release alerts
│   │   └── search.py        # Search across records
│   ├── static/
│   │   └── css/
│   │       ├── style.css
│   │       └── images/
│   │           └── jail_logo.png
│   └── templates/           # All HTML templates
├── run.py                   # Entry point
├── create_admin.py          # Script to create default admin
├── hash_passwords.py        # Script to hash existing passwords
└── README.md                # This file
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: No module named 'flask'` | Make sure venv is activated and run `pip install flask flask-mysqldb apscheduler werkzeug` |
| `Can't connect to MySQL server` | Make sure MySQL is running (start it in XAMPP) |
| `Access denied for user 'root'@'localhost'` | Edit `app/config.py` and set your MySQL password |
| `Table doesn't exist` | Run Step 6 again to create the database tables |
| `Login fails with correct password` | Run `python hash_passwords.py` to rehash passwords |

---

## Quick Start (TL;DR)

```bash
cd JMS
python -m venv venv
.\venv\Scripts\activate
pip install flask flask-mysqldb apscheduler werkzeug
python -c "import MySQLdb; db=MySQLdb.connect(host='localhost', user='root', password=''); cursor=db.cursor(); cursor.execute('CREATE DATABASE IF NOT EXISTS JMS'); db.commit(); sql=open('app/models/JMS.sql','r').read(); db.select_db('JMS'); [cursor.execute(stmt) for stmt in sql.split(';') if stmt.strip()]; db.commit(); cursor.close(); db.close(); print('Done!')"
python create_admin.py
python run.py
```

Then open **http://127.0.0.1:5000** and log in with `admin` / `admin_password`.
