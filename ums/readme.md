Here’s the updated **README.md** including everything we've completed so far in your **University Management System (UMS)** — with all apps created and their current progress.

---

# **University Management System (UMS)**

A modular, scalable, and production-ready University Management System built with:

* **Backend**: Django + Django REST Framework (DRF)
* **Frontend**: React
* **Database**: PostgreSQL
* **Authentication**: JWT (SimpleJWT)

---

## **Completed Modules**

### 1. **User Management (Core)**

* Role-based authentication: **Admin, Faculty, Student**
* JWT authentication (login, refresh, profile)
* Student and faculty profiles

### 2. **Batch & Programs**

* Separate app for handling university **batches and academic programs**
* Each batch contains programs, each program has students

### 3. **Students**

* Student profile management
* Linked with user accounts and programs

### 4. **Enrollments**

* Course enrollment per student
* Linked with academic terms and programs

### 5. **Exams**

* Exam scheduling per course
* Faculty can add marks within **15–30 days after exams**
* Grade calculation rules configurable

### 6. **Notifications**

* Centralized notification system
* Supports: INFO, ALERT, REMINDER
* Integrated with other modules (exam reminders, enrollment alerts, etc.)

### 7. **Fees Management**

* Fee structure per student
* Supports discounts, fines, and penalties
* Admin can adjust percentages, waive fines

### 8. **Attendance**

* Faculty can mark attendance (PRESENT, ABSENT, LATE)
* Student and faculty separate APIs
* Daily record linked to course enrollment

### 9. **Library Management**

* Book management (add, update, delete)
* Borrow/return system
* Automatic availability update
* Student APIs to view books, borrowed history, and fines

### 10. **Hostel Management**

* Hostel & room management
* Room allocation with start/end dates
* Fee integration (optional via `fees` app)
* Violation tracking with fines
* Notifications for allocations, vacating, violations
* Student APIs for active allocation, available rooms, and violations

---

## **Next Planned Modules**

* **Transport Management**: Bus routes, student passes, fee integration
* **Cafeteria / Mess Management**: Meal plans, billing, and attendance
* **Events & Activities**: Extracurricular event registration and participation
* **Research & Thesis Tracking**: Supervisor assignments, project progress
* **Alumni Portal**: Networking, donations, events

---

## **Architecture & Best Practices**

* Each feature is developed as a **separate Django app**
* **Separate APIs for Students and Faculty/Admin**
* **Celery** planned for scheduled tasks (exam reminders, hostel end reminders, etc.)
* Uses **signals & utilities** for notifications and fees integration

---

## **Setup**

```bash
# Clone the repo
git clone <repo_url>
cd ums

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Run server
python manage.py runserver
```

---

## **Next Steps**

* Build **Transport Management app**
* Implement **Cafeteria/Mess Management**
* Add **Celery + Celery Beat for automated reminders**
* Write **unit tests (pytest + DRF)** for each module
* Integrate **React frontend**

---
