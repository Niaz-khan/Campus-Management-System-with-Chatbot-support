# **University Management System (UMS)**

## **Overview**

A modular, scalable platform to manage all aspects of a university, built with:

* **Backend:** Django + Django REST Framework (DRF) + PostgreSQL
* **Frontend:** React (SPA with JWT authentication)
* **Authentication:** JWT (access & refresh tokens)

---

## **Key Modules**

* Users & Authentication
* **Organizational Structure (Campus, Departments, Roles, Members)**
* Students & Faculty Management
* Courses & Enrollments
* Attendance
* Exams & Grades
* Fees & Payments
* Library
* Hostel
* Transport
* Sports
* Events
* Cafeteria
* Notifications
* **Dashboards (Role-based for Admin, HOD, Coordinators, Faculty, Students)**

---

## **API Authentication**

All protected endpoints require:

```http
Authorization: Bearer <access_token>
```

To obtain a token:

```http
POST /users/login/
{
  "email": "admin@example.com",
  "password": "admin123"
}
```

---

## **Organizational Structure & Roles (Updated)**

* Supports **multiple campuses** with independent departments.
* Departments are linked to campuses and can have their own faculty, students, and courses.

### **Roles & Members**

* Each department and campus can have:

  * **HOD (Head of Department)** – manages department-level operations.
  * **Coordinators (Exam Coordinator, Campus Coordinator, etc.)** – manage specialized areas.
  * **Clerks** – handle administrative tasks.
  * **Faculty Members** – teaching staff.
* Admin can assign and remove members dynamically.

### **Planned Role Management Enhancement**

* Add **CampusMember** support for campus-wide roles.
* Extend `DepartmentRole` to include fine-grained permissions:

  * `can_manage_members`
  * `can_manage_courses`
  * `can_manage_exams`
  * `can_manage_attendance`
  * `can_manage_fees`
  * etc.
* Allow **multiple roles per user** (e.g., Faculty + Exam Coordinator).
* Enable **dynamic permissions configuration** instead of hardcoding.

### **Org Structure Endpoints**

```
GET/POST      /org/campuses/
GET/PUT/DELETE /org/campuses/{id}/

GET/POST      /org/departments/
GET/PUT/DELETE /org/departments/{id}/

GET           /org/roles/
GET/POST      /org/members/
GET/PUT/DELETE /org/members/{id}/
```

---

## **Implemented Apps & APIs**

### **1. Users**

* Registration, Login (JWT), Profile fetch
* Roles: Admin, HOD, Coordinator, Faculty, Student
* Endpoints:

  * `POST /users/register/`
  * `POST /users/login/`
  * `GET /users/me/`
  * `POST /users/token/refresh/`

### **2. Students**

* Student profile management
* View/update student details
* Endpoints: `/students/`, `/students/me/`

### **3. Faculty**

* Faculty profile management
* Assign departments & courses
* Endpoints: `/faculty/`, `/faculty/me/`

### **4. Courses**

* Course creation, assignment to faculty
* Supports program, batch, campus, department linkage

### **5. Enrollments**

* Student enrollments per semester/course

### **6. Attendance**

* Faculty: Mark/update attendance
* Students: View their attendance

### **7. Exams**

* Exam scheduling, locking, publishing
* Grades & GPA calculations

### **8. Fees**

* Categories, Invoices, Payments, Overdue Reports

### **9. Library**

* Books, Borrow/Return, Fines

### **10. Hostel**

* Hostel & Room allocation, Violations, Vacate workflow

### **11. Transport**

* Routes, Vehicles, Pass issuance & revocation

### **12. Cafeteria**

* Meal plans, Attendance, Subscriptions

### **13. Sports**

* Facilities, Equipment, Memberships, Tournaments

### **14. Events**

* Event creation, Student registrations, Certificate issuance

### **15. Notifications**

* Centralized notification system for all apps

### **16. Dashboards**

* Role-based dashboards for:

  * Admin
  * HOD
  * Coordinators
  * Faculty
  * Students

---

## **Planned Next Steps**

* Fully implement **Dashboards with charts & quick actions**.
* Integrate **dynamic role permissions per campus/department**.
* Add **multi-campus reporting and analytics**.
* Develop **React frontend dashboard pages**.

---

## **How to Run**

### **Backend**

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver
```

### **Frontend (React)**

```bash
cd frontend
npm install
npm start
```

### **Default API Base URL**

```
http://localhost:8000/api/
```

