#  IT Company Task Manager
Task manager for resolving potential problems during product development by your team

## Features
- User authentication
- Admin panel /admin/
- Managing projects, tasks, users
- Dashboard with list of hot tasks
- Adding tasks with binding to project
- Tasks have priority and deadline
- Filtering tasks by name

## Installation
```
git clone https://github.com/ansicat/task-manager.git
cd task-manager
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
Use `.env_sample` as template and create file `.env` with your settings
```
python manage.py init_db
python manage.py runserver
```

## Getting access with Render
Open https://task-manager-t7eg.onrender.com

Use credentials for login:
  - user: admin
  - password: asdf7890