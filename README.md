## 📂 Project Structure (Simplified)

# 📘 Student Attendance Tracker

## 📌 Overview

**Student Attendance Tracker** is a Django-based web application that allows educational institutions to manage students and track daily attendance with **role-based access control**.

### Key Roles
- **Admin**: Manages teachers, students, assignments, and views all reports
- **Teacher**: Marks attendance, views assigned students, and edits previous attendance

---

## ✨ Features

### Authentication & Authorization
- Secure login/logout
- Role-based access (Admin / Teacher)

### Admin Features
- Create / Edit / Delete Teachers
- Create / Edit / Delete Students
- Assign students to teachers
- View attendance reports for all students

### Teacher Features
- View assigned students
- Mark daily attendance
- Edit previous day’s attendance
- View reports filtered by date, student, or class

### Reporting
- Date-wise attendance (default: today)
- Student-wise attendance report
- Class-wise filtering
- Monthly summary (present % / absent %)
- Export student attendance as CSV

---

## 🛠️ Tech Stack

- **Backend**: Django
- **Database**: PostgreSQL
- **Frontend**: Django Templates (HTML)
- **Auth**: Django Authentication System

---

## 📂 Project Structure (Simplified)
```bash
attendance-tracker/
├── attendance/ # Core app
    ├── templates/ # HTML templates
├── tracker/ # Project settings
├── manage.py
├── README.md
```
---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/MohamedWazeemJassir/attendance-tracker.git
cd attendance-tracker
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv myenv
myenv\Scripts\activate      # Windows
source myenv/bin/activate   # Mac/Linux
```
### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```
If requirements.txt is not present:
```bash
pip install django psycopg2-binary
```

### 4️⃣ Configure PostgreSQL Database

Create the database manually (required once):

```bash
CREATE DATABASE attendance_db;
```

### 5️⃣ Update settings.py

```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'attendance_db',
        'USER': 'postgres',
        'PASSWORD': 'your_postgres_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 6️⃣ Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate

👤 Create Admin User (IMPORTANT)

Admins are created manually via Django shell.

python manage.py shell

from django.contrib.auth.models import User
from attendance.models import UserProfile

user = User.objects.create_user(
    username="admin",
    password="admin123"
)

UserProfile.objects.create(
    user=user,
    role="ADMIN"
)
```

Exit shell:
```bash
exit()
```

## ▶️ Run the Application
```bash
python manage.py runserver
```

Open in browser:
```bash
http://127.0.0.1:8000/
```

## 🔑 Login Credentials (Demo)

| Role  | Username | Password |
|------|----------|----------|
| Admin | admin    | admin123 |

> ℹ️ **Note:** Teachers are created by the Admin inside the application.

---

## 📤 Exporting Reports

- Student-wise attendance reports can be exported as **CSV**
- The **Export CSV** button is available on the **Student Attendance Report** page
