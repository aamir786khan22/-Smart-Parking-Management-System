# Smart Parking Management System

## Overview
The **Smart Parking Management System** is a computer vision–based web application that automates parking slot detection, booking, and management. It provides real-time information about available and occupied parking slots, making parking easier and efficient for users.

---

## Tech Stack
- **Backend:** Python, Django  
- **Frontend:** HTML, CSS  
- **Database:** MySQL  
- **Computer Vision:** OpenCV  

---

## Features
- Detects occupied and vacant parking slots using **OpenCV**.  
- User account creation, login, and secure **OTP email verification**.  
- Real-time slot availability and booking interface.  
- Booking history management.  
- Admin panel integration for slot management and monitoring.  
- Accurate object detection for car detection and slot status automation.  

---

## Installation & Setup

1. **Clone the repository**  
```bash
git clone <your-repo-link>
cd SMART_PARKING_MANAGEMENT_SYSTEM
```
2. **Create a virtual environment and activate it**
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

3.**Install required packages**
pip install -r requirements.txt

4.**Create a .env file (based on credentials.env)**
# Example .env (DO NOT upload to GitHub)
SECRET_KEY=<your_django_secret_key>
DB_NAME=<your_database_name>
DB_USER=<your_database_user>
DB_PASSWORD=<your_database_password>
DB_HOST=localhost
DB_PORT=3306
EMAIL_HOST=<your_email_host>
EMAIL_PORT=<your_email_port>
EMAIL_HOST_USER=<your_email>
EMAIL_HOST_PASSWORD=<your_email_password>

5.**Apply migrations**
python manage.py makemigrations
python manage.py migrate

6.**Run the development server**
python manage.py runserver

7.**Open the browser and go to:**
http://127.0.0.1:8000/

# Usage

Sign up and log in with a verified email.
Check available parking slots in real-time.
Book a slot and view booking history.
Admin can manage slots and monitor bookings.

# Security & Best Practices
Do not upload .env or credentials.env to GitHub.
Use a .gitignore file to exclude sensitive files:
All sensitive information (email, database credentials, secret key) must remain local.
OTP verification ensures secure login and account validation.

# Author
Aamir Khan – B.Tech CSE (AI/ML)
