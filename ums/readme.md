Here’s a **comprehensive README.md** for your **University Management System (UMS)** that documents everything we’ve completed so far **and outlines the remaining plan**.

---

# **University Management System (UMS)**

A robust and scalable **University Management System** built using **Django, Django REST Framework (DRF), PostgreSQL, and React** (frontend planned).
This system aims to manage all core academic operations: **user management, students, batches, programs, courses, enrollments**, and more.

---

## **Tech Stack**

* **Backend:** Django 5+ with Django REST Framework (DRF)
* **Database:** PostgreSQL
* **Authentication:** JWT (SimpleJWT)
* **Frontend:** React (to be implemented)
* **Deployment:** CI/CD planned (Docker, GitHub Actions, VPS/Cloud)
* **Future Modules:** Attendance, Exams, Grading, Fees, Chatbot

---

## **Completed Features**

### **1. Users & Authentication**

* Custom User model with roles:

  * **Admin** – Full access
  * **Faculty** – Course & enrollment management
  * **Student** – Limited access
* JWT authentication (Login, Refresh, Profile)
* Registration for Students (Admins can upgrade role)

### **2. Academics App (Batches & Programs)**

* **Batch model:** Represents academic sessions (e.g., Fall 2025)
* **Program model:** Degree programs linked to batches
* CRUD APIs with role-based permissions:

  * Admin: Full control
  * Authenticated users: Read-only

### **3. Students App**

* **StudentProfile model:** Linked to User, Batch, and Program
* Auto-creation of profile when a student registers
* APIs:

  * List all students (Admin/Faculty)
  * Retrieve/update student
  * Student self-profile endpoint

### **4. Courses App**

* **Course model:** Linked to Program, Batch, and Faculty
* Attributes: course code, credits, semester, core/elective, faculty assignment
* CRUD APIs with:

  * Admin: Full control
  * Faculty: Update assigned courses
  * Students: Read-only

### **5. Enrollments App**

* **Enrollment model:** Student ↔ Course mapping
* Attributes: status (enrolled, dropped, completed), grade
* APIs:

  * Admin: Enroll/remove/update
  * Faculty: View/update (status/grade)
  * Students: View their own enrollments

---

## **Planned Features**

### **Next Steps**

1. **Faculty Management**

   * FacultyProfile model
   * APIs for managing faculty details

2. **Attendance System**

   * Linked to enrollments
   * Mark attendance per course per session

3. **Exams & Grading**

   * Store marks/grades per enrollment
   * GPA & CGPA calculation

4. **Fees & Billing**

   * Track payments, dues, and invoices

5. **Curriculum & Semesters**

   * Define semester-wise curriculum for programs
   * Assign courses automatically

6. **AI Chatbot Integration**

   * Help desk for students and faculty
   * Status checking (admissions, grades, etc.)

7. **CI/CD & Deployment**

   * GitHub Actions for automated deployment
   * Dockerized setup for production

---

## **API Overview**

### **Authentication**

* `POST /api/users/register/` – Register user
* `POST /api/users/login/` – Login (JWT)
* `POST /api/users/token/refresh/` – Refresh token
* `GET /api/users/me/` – Current user profile

### **Academics**

* `GET/POST /api/academics/batches/`
* `GET/PUT/DELETE /api/academics/batches/<id>/`
* `GET/POST /api/academics/programs/`
* `GET/PUT/DELETE /api/academics/programs/<id>/`

### **Students**

* `GET /api/students/` – List all students
* `GET/PUT /api/students/<id>/`
* `GET /api/students/me/` – Student’s own profile

### **Courses**

* `GET /api/courses/` – List all courses
* `POST /api/courses/` – Add course (Admin)
* `GET/PUT/DELETE /api/courses/<id>/`

### **Enrollments**

* `GET/POST /api/enrollments/`
* `GET/PUT/DELETE /api/enrollments/<id>/`
* `GET /api/enrollments/my/` – Student’s enrolled courses

---

## **Project Structure**

```
UMS/
├── academics/        # Batches & Programs
├── courses/          # Courses under programs
├── enrollments/      # Student course enrollments
├── students/         # Student profiles & data
├── users/            # Custom user model & authentication
└── manage.py
```

---

## **Setup Instructions**

1. **Clone repository**

```bash
git clone <repo_url>
cd UMS
```

2. **Create virtual environment & install dependencies**

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. **Apply migrations**

```bash
python manage.py makemigrations
python manage.py migrate
```

4. **Create superuser**

```bash
python manage.py createsuperuser
```

5. **Run development server**

```bash
python manage.py runserver
```

---

## **Contributing**

* Fork the repo
* Create a feature branch
* Submit a pull request

---

## **License**

MIT License
