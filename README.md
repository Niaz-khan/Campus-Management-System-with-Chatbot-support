# 🎓 Smart University Management System (Smart UMS) with AI-Powered Chatbot

An AI-driven, multilingual campus management system built using Django, integrated with Hugging Face NLP models. This project automates student lifecycle management — from admissions to promotion and transcript generation — with an intelligent chatbot interface that understands English and Urdu.

---

## 🚀 Features

### 🧩 Core Functional Modules
- **Admissions Management** – Online student application and acceptance workflow.
- **Student Information System (SIS)** – Role-based access with student, faculty, and admin dashboards.
- **Student Transcript View** - Students can see their GPA, grades, and semester records.
- **Course Management** – Course creation, semester allocation, credit tracking.
- **Enrollment & Promotion** – Auto-enroll into semester courses and promote based on exam results.
- **Exam & GPA System** – Enter exam results, auto-calculate GPA & CGPA.
- **Fee & Faculty Management** – Extendable to handle financials and faculty operations.

### 🤖 AI Chatbot (Built with Hugging Face & PyTorch)
- **Natural Language Support**: Understands questions like:
  - “What is my GPA?”
  - “Show my transcript.”
  - “List my enrolled courses.”
- **Multilingual Support** (English + Urdu)
- **Smart Greeting Detection**: Responds to “hi”, “salam”, etc.
- **Floating Widget**: Always accessible on every page.
- **Connected to Live Data**: Answers using real student info from database.

---

## 🛠️ Tech Stack

| Layer         | Technology                         |
|--------------|------------------------------------|
| Framework     | Django (Python)                   |
| Frontend      | HTML5, CSS3, Bootstrap             |
| Database      | PostgreSQL / MySQL                 |
| AI/NLP        | Hugging Face Transformers + PyTorch|
| Translation   | Helsinki-NLP Models                |
| Dev Tools     | Git, Postman, PythonAnywhere       |

---

## 📁 Project Structure


CMS_PROJECT/ 
│ 
├── chatbot/ # Chatbot app (views, LLM, forms) 
├── admissions/ # Student application module 
├── enrollments/ # Handles course enrollment 
├── courses/ # Course and semester setup 
├── exams/ # Exam results, GPA, transcript logic 
├── students/ # Student model and profiles 
├── users/ # Auth and role-based access │ 
├── templates/ # Base HTML and frontend templates 
├── static/ # CSS, JS 
├── manage.py 
└── requirements.txt


---

## 💬 Sample Chatbot Intents

| Query                          | Intent      | Action                                |
|--------------------------------|-------------|---------------------------------------|
| “hi”, “salam”                  | greeting    | Sends polite welcome message          |
| “What is my GPA?”             | gpa         | Fetches and calculates real GPA       |
| “List my courses”             | courses     | Shows enrolled subjects               |
| “Am I promoted?”              | promotion   | Checks semester progression           |
| “Show my transcript”         | transcript  | Returns subject-wise marks            |
| Any other academic question    | fallback    | Uses Hugging Face QA model            |

---

## 🧠 AI Model Info

- Question Answering: `distilbert-base-cased-distilled-squad`
- Translation (English <-> Urdu): 
  - `Helsinki-NLP/opus-mt-en-ur`
  - `Helsinki-NLP/opus-mt-ur-en`
- Device: GPU if available (auto-detected)

---

## ⚙️ Setup Instructions

### ✅ 1. Clone the Repo

```bash
git clone https://github.com/yourusername/smart-ums.git
cd smart-ums

```python
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

✅ 3. Install Dependencies
bash
pip install -r requirements.txt
If using GPU:

bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
✅ 4. Run Migrations
bash

python manage.py makemigrations
python manage.py migrate
✅ 5. Create Superuser
bash

python manage.py createsuperuser
✅ 6. Run Server
bash

python manage.py runserver
Open: http://127.0.0.1:8000

🔐 Roles Supported

Role	Access Level
Admin	Full control over all modules
Faculty	Exam creation, result entry
Student	Enrollments, transcript, chatbot
📌 Future Additions
PDF transcript export

Faculty/Admin chatbot support

Chat history logging

Deployment on Render / PythonAnywhere

🧾 License
This project is for academic and demo purposes. For enterprise licensing, contact the author.

👨‍💻 Author
Niaz Khan
Computer Science Final Year Project
University of Science & Technology, Bannu.





