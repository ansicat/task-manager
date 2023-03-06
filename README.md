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

## Install using GitHub
```
git clone https://github.com/ansicat/task-manager.git
cd task-manager
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Getting access
- create admin user
    ```
    python manage.py createsuperuser
    ```
- open start page of site: /login/

## Fast review (with test data)
- load test data
    ```
    python manage.py loaddata task_manager_db_data.json
    ```
- use credentials for login:
  - user: admin
  - password: asdf7890
