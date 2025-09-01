Here’s the **updated `README.md`** including **everything we have built so far in the University Management System (UMS)** — with all apps, their features, and the planned roadmap.

---

# **University Management System (UMS)**

A modular, scalable, and production-grade University Management System built using **Django, Django REST Framework (DRF), PostgreSQL, and React (frontend planned)**.

---

## **Current Features Implemented**

### **1. Users App**

* JWT Authentication (login, refresh, logout)
* Role-based access:

  * **Admin** – Full control
  * **Faculty** – Course & exam management
  * **Student** – Enrollment & results access
* User registration & profile API

---

### **2. Programs & Batches App**

* Define **Programs** (e.g., BS Computer Science, MBA)
* Manage **Batches** per program with start & end year
* Link students to batches
* Fully RESTful API for CRUD operations

---

### **3. Students App**

* Student profile management:

  * Roll number
  * Semester
  * Linked user account
  * CGPA (auto-calculated)
  * Credits completed (auto-updated)
* APIs for listing, creating, and updating students

---

### **4. Enrollments App**

* Enroll students into courses
* Track enrollment status (`ENROLLED`, `DROPPED`)
* CRUD endpoints with permissions

---

### **5. Exams App**

* **Exam Management**

  * Schedule exams (Midterm, Final, Quiz, Assignment)
  * Set grading deadlines (e.g., 15–30 days after exam)
  * Faculty & Admin create exams
* **Grades Management**

  * Add/update grades within grading window
  * Publish & Lock results workflow:

    * **DRAFT** → Faculty editing
    * **PUBLISHED** → Students can view
    * **LOCKED** → Finalized, no edits
* **GPA/CGPA Calculation**

  * Automated calculation based on grades & credit hours
  * Auto-updates via signals on grade changes
  * Endpoint: `/api/exams/grades/my/gpa/`
* **Student View**

  * Students can only see grades after publication

---

### **6. Notifications App**

* Centralized notification management
* Features:

  * In-app notifications stored in DB
  * Notification types: INFO, WARNING, ALERT, REMINDER
  * Related object tracking (e.g., Exam, Fee)
  * APIs:

    * `GET /api/notifications/` – List user notifications
    * `PATCH /api/notifications/<id>/read/` – Mark as read
* Integrated with Exams:

  * New exam scheduled → notify enrolled students
  * Results published → notify students
  * Grading deadline reminders → notify faculty (via task/cron)
  * Results locked → notify students & faculty

---

## **Upcoming Features (Planned)**

1. **Fees & Billing Module**

   * Tuition invoices
   * Payment tracking
   * Automated due date reminders
2. **Attendance Module**

   * Daily attendance
   * Low attendance alerts via Notifications app
3. **Library Management**

   * Book issue/return
   * Overdue alerts
4. **Dashboard & Analytics**

   * Admin: University-wide overview
   * Faculty: Course & grading analytics
   * Student: Grades & fees overview
5. **Frontend (React + Tailwind)**

   * Admin panel
   * Faculty dashboard
   * Student self-service portal

---

## **Tech Stack**

* **Backend:** Django 5, Django REST Framework (DRF)
* **Database:** PostgreSQL
* **Authentication:** JWT (SimpleJWT)
* **Notifications:** Custom app (DB-based, extendable to email/SMS)
* **Frontend:** React (planned)
* **Async Tasks (planned):** Celery + Redis

---

## **Setup Instructions**

```bash
# Clone the repository
git clone <repo_url>
cd ums

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

---

## **API Overview**

* **Users:** `/api/users/`
* **Programs:** `/api/programs/`
* **Students:** `/api/students/`
* **Enrollments:** `/api/enrollments/`
* **Exams:** `/api/exams/`
* **Notifications:** `/api/notifications/`

---
Perfect — let's **upgrade the README with:**

1. **Architecture Diagram (apps & interactions)**
2. **Database ERD (Entity Relationship Diagram)**
3. **Detailed API Documentation (with example requests & responses)**

---

## **1. Architecture Diagram**

We'll create a simple architecture visualization:

* **Users** → Authentication & Roles
* **Programs & Batches** → Academic structure
* **Students** → Student profile & academic progress
* **Enrollments** → Linking students with courses
* **Exams & Grades** → Assessments & GPA
* **Notifications** → Cross-app alerts
* (Planned: Fees, Attendance, Library, Frontend)

```plaintext
          +------------------+
          |      Users       |
          +--------+---------+
                   |
                   v
       +-----------+-----------+
       | Programs & Batches    |
       +-----------+-----------+
                   |
                   v
       +-----------+-----------+
       |     Students          |
       +-----------+-----------+
                   |
                   v
       +-----------+-----------+
       |   Enrollments         |
       +-----------+-----------+
                   |
                   v
       +-----------+-----------+
       | Exams & Grades        |
       +-----------+-----------+
                   |
                   v
       +-----------+-----------+
       | Notifications         |
       +-----------------------+
```

---

## **2. Database ERD**

### Entities:

* **User (Custom)**: `id, username, email, role`
* **Program**: `id, name`
* **Batch**: `id, program_id, start_year, end_year`
* **Student**: `id, user_id, roll_no, semester, cgpa`
* **Course**: `id, program_id, title, credit_hours`
* **Enrollment**: `id, student_id, course_id, status`
* **Exam**: `id, course_id, title, exam_type, date, grading_deadline_days, result_status`
* **Grade**: `id, exam_id, enrollment_id, marks_obtained, remarks`
* **Notification**: `id, user_id, title, message, type, is_read`

Relationships:

* **User → Student (One-to-One)**
* **Program → Batch (One-to-Many)**
* **Batch → Student (Many-to-Many via enrollment)**
* **Course → Enrollment (One-to-Many)**
* **Exam → Grade (One-to-Many)**
* **Notification → User (One-to-Many)**

(We can generate a **graphical ERD** using `django-extensions graph_models` if needed.)

---

## **3. Detailed API Documentation**

Here’s a concise version for the main modules.

### **Users**

* **Register User**

  * `POST /api/users/register/`

  ```json
  {
    "username": "john123",
    "email": "john@example.com",
    "password": "secret123",
    "role": "STUDENT"
  }
  ```
* **Login**

  * `POST /api/users/login/`

  ```json
  { "username": "john123", "password": "secret123" }
  ```

### **Programs & Batches**

* **Create Program**

  * `POST /api/programs/`

  ```json
  { "name": "BS Computer Science" }
  ```
* **Create Batch**

  * `POST /api/programs/batches/`

  ```json
  { "program": 1, "start_year": 2023, "end_year": 2027 }
  ```

### **Students**

* **Create Student**

  * `POST /api/students/`

  ```json
  {
    "user": 2,
    "roll_no": "BSCS-23-01",
    "semester": 1
  }
  ```

### **Enrollments**

* **Enroll Student in Course**

  * `POST /api/enrollments/`

  ```json
  {
    "student": 5,
    "course": 10,
    "status": "ENROLLED"
  }
  ```

### **Exams & Grades**

* **Create Exam**

  * `POST /api/exams/`

  ```json
  {
    "course": 10,
    "title": "Midterm Exam",
    "exam_type": "MIDTERM",
    "total_marks": 50,
    "date": "2025-10-15"
  }
  ```

* **Add Grade**

  * `POST /api/exams/grades/`

  ```json
  {
    "exam": 3,
    "enrollment": 25,
    "marks_obtained": 42,
    "remarks": "Good work"
  }
  ```

* **Publish Results**

  * `POST /api/exams/3/publish/`

* **View GPA/CGPA**

  * `GET /api/exams/grades/my/gpa/`

  ```json
  {
    "GPA": 3.5,
    "CGPA": 3.4,
    "credits_completed": 45
  }
  ```

### **Notifications**

* **View Notifications**

  * `GET /api/notifications/`
* **Mark as Read**

  * `PATCH /api/notifications/1/read/`

  ```json
  { "is_read": true }
  ```

---

## **Contributing**

* Fork the repo
* Create a new branch
* Submit a pull request

