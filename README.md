# Project Management - Flask

A responsive project management application built with **Python, Flask, Jinja, Bootstrap, and Object-Oriented Programming (OOP)**.

The project simulates a simple workflow for managing web development projects, including proposals, active projects, tasks, deadlines, progress, and completed projects.

> This project was created for academic purposes and currently uses in-memory mock data instead of a database.

## Live Demo

https://project-management-flask-m51l.onrender.com/

## Demo Login

```text
Email: william@test.com
Password: admin123
```

The login uses a simple Flask validation for demonstration purposes.

## Main Features

- Project creation and status tracking
- Workflow from **Proposal Sent** to **In Progress** and **Completed**
- Predefined task lists for each project category
- Task owners automatically assigned as **Designer** or **Developer**
- Task completion and project progress tracking
- Deadline calculation for active projects
- Monthly and annual earnings calculation
- Completed projects grouped by month
- Responsive interface with Bootstrap
- Deployment on Render with Gunicorn

## Project Workflow

```text
Proposal Sent
     ↓
In Progress
     ↓
Completed
```

When a project is started, the application creates its task list according to the selected category:

| Category | Tasks |
| --- | ---: |
| E-commerce Websites | 23 |
| Landing Pages | 18 |
| Institutional Websites | 16 |

Tasks containing `Design` are assigned to the **Designer**. All other tasks are assigned to the **Developer**.

As tasks are completed, the project progress is updated automatically. A project can only be completed when it reaches **100%** progress.

## Dashboard

The dashboard calculates its information dynamically from the project data, including:

- Monthly earnings
- Annual earnings
- Pending approvals
- Completed tasks from active projects
- Progress of projects currently in development

## Main Pages

**Project Tracker** displays all projects grouped by category and shows their status, client, prices, dates, and deadlines.

**In Progress** displays active projects ordered by the closest deadline. Clicking a project name opens its task page.

**Project Details** displays each task, its owner, status, and the overall project progress.

**Completed Projects** groups completed projects by month and displays completion date, net value, invoice status, and project URL.

## OOP Structure

The main classes are:

- `Project` — project data, progress, earnings, dates, and task management
- `ProjectGroup` — project categories and predefined task lists
- `Task` — task name, owner, and completion status
- `RecentActivity` — mock activity entries displayed on the dashboard

## Project Structure

```text
project-management-flask/
├── app.py
├── data/
│   ├── models.py
│   ├── dashboard_data.py
│   └── tracker_data.py
├── static/
│   ├── css/style.css
│   └── images/
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── dashboard.html
│   ├── project_tracker.html
│   ├── in_progress.html
│   ├── project_details.html
│   └── completed_projects.html
├── pyproject.toml
├── uv.lock
└── README.md
```

## Technologies

- Python
- Flask
- Jinja
- HTML5 / CSS3
- Bootstrap 5
- Bootstrap Icons
- uv
- Gunicorn
- Render

## Running Locally

Clone the repository and enter the project folder:

```bash
git clone https://github.com/williamcarvalhodev/project-management-flask.git
cd project-management-flask
```

Install dependencies:

```bash
uv sync
```

Set the Flask secret key:

```bash
export SECRET_KEY="development-secret-key"
```

Run the application:

```bash
uv run app.py
```

Then open:

```text
http://127.0.0.1:5000
```

## Deployment

The application is deployed on **Render** using **Gunicorn**.

Production start command:

```bash
gunicorn app:app
```

The Flask secret key is stored in Render as an environment variable:

```text
SECRET_KEY
```

The application reads it with:

```python
import os

app.secret_key = os.environ["SECRET_KEY"]
```

## Data Storage

The project currently uses Python lists and objects instead of a database. Runtime changes are stored only in memory, so they are lost when the server restarts.

## Author

**William Carvalho**

GitHub: [williamcarvalhodev](https://github.com/williamcarvalhodev)