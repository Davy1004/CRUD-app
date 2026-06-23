# Task & Project Tracker

A full-stack web app for managing projects and the tasks inside them, with
session-based login. Built by extending an existing Flask + Angular CRUD app.

## Live Demo

- Frontend (Vercel): https://crud-app-blush-beta.vercel.app
- Backend (Render): https://crud-app-narb.onrender.com

> Note: the backend runs on Render's free tier, which sleeps after inactivity.
> The first request after a quiet period takes 30–60 seconds to wake up.

## Tech Stack

- Frontend: Angular (standalone components, Bootstrap 5)
- Backend: Flask + SQLAlchemy
- Database: PostgreSQL (on Render)
- Auth: Flask server-side sessions (cookie-based, no JWT)
- Hosting: Vercel (frontend), Render (backend + Postgres)

## Features

- Sign up, log in, and log out with session-based authentication
- Create, view, and delete projects
- Create, view, complete, and delete tasks within a project
- Filter tasks by status: All / Completed / Pending
- Form validation on both frontend and backend (empty project names and task
  titles are rejected with clear error messages)
- Confirmation dialog before deleting
- Success and error messages in the UI

## API Endpoints

Auth:

- `POST /api/auth/signup` — create an account and start a session
- `POST /api/auth/login` — log in and start a session
- `POST /api/auth/logout` — end the session
- `GET /api/auth/me` — check current login status

Projects:

- `GET /api/projects` — list all projects
- `POST /api/projects` — create a project
- `PUT /api/projects/<id>` — update a project
- `DELETE /api/projects/<id>` — delete a project (and its tasks)

Tasks:

- `GET /api/tasks` — list all tasks
- `GET /api/tasks?status=completed` — list completed tasks
- `GET /api/tasks?status=pending` — list pending tasks
- `POST /api/tasks` — create a task
- `PUT /api/tasks/<id>` — update a task (e.g. mark complete)
- `DELETE /api/tasks/<id>` — delete a task

Users (from the original CRUD app, still functional):

- `GET /api/users`, `POST /api/users`, `PUT /api/users/<id>`, `DELETE /api/users/<id>`

## Running Locally

### Backend

```
cd backend
pip install -r requirements.txt
python app.py
```

The backend defaults to a local SQLite database and runs on
`http://localhost:5000`.

To run against Postgres or in production mode, set these environment variables:

- `FLASK_CONFIG` = `production`
- `DATABASE_URL` = your Postgres connection string
- `SECRET_KEY` = any long random string (signs session cookies)
- `FRONTEND_ORIGIN` = the URL the frontend runs on (e.g. `http://localhost:4200`),
  with no trailing slash

### Frontend

```
cd backend/crud-app
npm install
npm start
```

The frontend runs on `http://localhost:4200`.

> For local login to work, `FRONTEND_ORIGIN` on the backend must exactly match
> the frontend URL (`http://localhost:4200`), with no trailing slash. A mismatch
> blocks the session cookie and login will silently fail.

## Project Structure

```
backend/
  app.py                  # app factory, CORS, session config, blueprint registration
  config.py               # dev / production config (Postgres URL handling)
  models/                 # User, Project, Task SQLAlchemy models
  services/               # business logic (auth, project, task, user)
  routes/                 # API route blueprints
  crud-app/               # Angular frontend
    src/app/
      login/              # login + signup form
      dashboard/          # projects + tasks UI with filter
      services/           # auth, project, task HTTP services
```

## 5-Minute Demo Script

1. Open the live frontend URL. (Hit it a minute beforehand so Render is awake.)
2. Sign up with a username and password — you land on the dashboard.
3. Add a project (e.g. "Website Redesign").
4. Add a couple of tasks to it.
5. Mark one task complete by ticking its checkbox.
6. Use the filter dropdown to switch between All / Completed / Pending and show
   the list changing.
7. Try adding a task with an empty title to show the validation error.
8. Delete a task — show the confirmation dialog, then confirm.
9. Log out, then log back in to show the session persists the data.

README.md
Displaying README.md.