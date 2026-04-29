# Aquatic Pandas Budget Management System

Aquatic Pandas is a Flask + MySQL budget tracking backend with user authentication, account management, category budgeting, and transaction tracking, all running in a Docker container. This project provides a robust foundation for personal financial data management, featuring a clean RESTful API, structured database models, and a pre-configured environment designed to streamline the development-to-deployment workflow.

## Tech Stack

- Python 3.11
- Flask 3.0
- Flask-SQLAlchemy
- SQLAlchemy 2.0
- Flask-Login
- MySQL 8.0
- Docker / Docker Compose

## Current Status

- Backend API is implemented and runs from `app.py`.
- Authentication uses Flask-Login session cookies (not token-based auth).
- CRUD endpoints exist for users, accounts, categories, and transactions.
- MySQL schema is defined in `init.sql` and mirrored by SQLAlchemy models in `models.py`.
- Docker setup is available for local development.
- HTML templates exist in `templates/`, but they are not wired into Flask routes in the current code.

## Documentation

- API Reference - Detailed endpoint documentation and roadmap.
- Database Schema - ORM models and relationship logic.
- Docker Setup - Detailed container management.
- Development Guide - Local setup and contribution notes.
- Testing Guide - How to verify endpoints using curl.
- App Mockup - Visual flow and dashboard layout.

## Project Structure

```sh
aquatic-pandas-bms/
├── app.py
├── close.sh
├── docker-compose.yml
├── Dockerfile
├── docs
│   ├── APPLICATION_PSEUDOCODE.md
│   ├── App_Mockup.md
│   ├── DOCKER_SETUP.md
│   └── Doc_TESTING.md
├── extensions.py
├── init.sql
├── models.py
├── __pycache__
│   ├── extensions.cpython-311.pyc
│   ├── models.cpython-311.pyc
│   └── routes.cpython-311.pyc
├── README.md
├── requirements.txt
├── restart.sh
├── routes.py
├── run.sh
├── start.sh
├── static
│   ├── bootstrap.css
│   └── style.css
├── templates
│   ├── accounts.html
│   ├── base.html
│   ├── buget.html
│   ├── index.html
│   ├── login.html
│   ├── profile.html
│   ├── register.html
│   └── transactions.html
└── testing.sh
```


## Run the App

### Run With Docker (Recommended)

1. Copy and Setup Environment

```bash
cp .env-example .env
```

2. Start Services

```bash
docker compose down --remove-orphans
```

3. Access Services

- App: `http://localhost:3000`
- MySQL: `localhost:3306`

4. Stop services:

```bash
docker compose down --remove-orphans
```

### Run Locally (Without Docker, and NOT RECOMMENDED)

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create MySQL database and run schema:

```bash
mysql -u <user> -p <database_name> < init.sql
```

4. Copy environment template and set local values:

```bash
cp .env.example .env
```

5. Start app:

```bash
python app.py
```

The app reads:

- `FLASK_HOST` (default: `0.0.0.0`)
- `FLASK_PORT` (default: `3000`)
- `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`
- `SECRET_KEY`

## Notes and Gaps

- Existing templates and static assets are not connected to Flask view routes yet.
- Planned routes in this README are explicitly marked and may not exist yet in `routes.py`.
- There is no automated test suite in the repository at this time.

## Useful Commands

```bash
# View app logs
docker-compose logs -f app

# View db logs
docker-compose logs -f db

# Open MySQL shell in container
docker-compose exec db mysql -u pandas_user -p aquatic_pandas
```
