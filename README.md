# Smart-Task-Manager
Built a task management backend with adaptive priority logic, recurring task scheduling, and recommendations  API for productivity enhancement.

# Smart Task Manager API

A backend API for a **Smart Task Manager** built with Flask. Features include adaptive priority logic, recurring task scheduling, and recommendations to help users manage tasks more productively.

---

## ✅ Features

- User registration and login with JWT authentication  
- Create / read / update / delete (CRUD) tasks  
- Tasks include title, description, due date, priority, status  
- Support for recurring tasks (e.g. daily, weekly)  
- Adaptive priority logic: tasks due sooner or overdue get higher priority  
- Recommendation endpoint: returns top tasks user should do now

---

## 🗂 Project Structure

   smart-task-manager/
├── app.py # main Flask application, endpoints + logic
├── models.py # SQLAlchemy models: User and Task
├── test_api.py # script to test all endpoints: register, login, create/list/recommend tasks
├── requirements.txt # dependencies
├── README.md # this file
├── .gitignore # ignore venv, DB, cache, etc.
├── database.db # SQLite database file (auto-created) - ignored by git
└── venv/ # virtual environment, ignored


## 🔧 Setup & Usage

1. Clone the repo:

   ```bash
   git clone https://github.com/<yourusername>/smart-task-manager.git
   cd smart-task-manager
2. Create and activate virtual environment (Windows):
   
   python -m venv venv
   venv\Scripts\activate

3. Install dependencies:

   pip install --upgrade pip
   pip install -r requirements.txt

4.start the server:
  
  python app.py

5.In another terminal (venv active), run test script to verify functionality:

  python test_api.py
This script will:

Register a new user (or show existing)

Login → get JWT token

Create a few tasks

List tasks (with adaptive priority logic)

Get recommendations of tasks to do now

Examples

Create Task Request

POST /tasks
Authorization: Bearer <token>
Body (JSON):
{
  "title": "Finish report",
  "description": "Complete monthly sales report",
  "due_date": "2025-09-22T18:00:00",
  "priority": 2,
  "recurrence": "daily"
}

Sample Task Listing Response

{
  "tasks": [
    {
      "id": 1,
      "title": "Finish report",
      "due_date": "2025-09-22T18:00:00",
      "priority": 2,
      "status": "pending",
      "recurrence": "daily",
      "adaptive_score": 4
    },
    {
      "id": 2,
      "title": "Clean desk",
      "due_date": null,
      "priority": 1,
      "status": "pending",
      "recurrence": null,
      "adaptive_score": 1
    }
  ]
}


⚠ Limitations & Future Improvements

Recurrence logic is basic (daily / weekly); doesn’t support complex schedules (monthly, custom intervals)

Priority logic is simple; could use more factors (user importance, categories)

No UI included; backend only

No pagination, filtering, or search in task listing

Tests / error handling are minimal — in production, more tests & validation needed


Contact & Repo

>GitHub:https://github.com/nubaid46
>Repository URL:https://github.com/nubaid46/Smart-Task-Manager

