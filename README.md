# Aquatic Pandas Budget Management System

Aquatic Pandas is a Flask + MySQL budget tracking backend with user authentication, account management, category budgeting, and transaction tracking.

## Current Status

- Backend API is implemented and runs from `app.py`.
- Authentication uses Flask-Login session cookies (not token-based auth).
- CRUD endpoints exist for users, accounts, categories, and transactions.
- MySQL schema is defined in `init.sql` and mirrored by SQLAlchemy models in `models.py`.
- Docker setup is available for local development.
- HTML templates exist in `templates/`, but they are not wired into Flask routes in the current code.

## Tech Stack

- Python 3.11
- Flask 3.0
- Flask-SQLAlchemy
- SQLAlchemy 2.0
- Flask-Login
- MySQL 8.0
- Docker / Docker Compose

## Project Structure

```text
CS_440_Aquatic_Pandas/
├── app.py
├── models.py
├── routes.py
├── init.sql
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── DOCKER_SETUP.md
├── APPLICATION_PSEUDOCODE.md
├── App_Mockup.md
├── static/
│   └── style.css
└── templates/
    ├── accounts.html
    ├── buget.html
    ├── login.html
    ├── profile.html
    ├── registrar.html
    └── transactions.html
```

## Database Models

The ORM models in `models.py` map to the tables in `init.sql`:

- `User`
- `Institution`
- `Account`
- `Category`
- `Transaction`

Key relationship behavior:

- Deleting a user cascades to accounts and categories.
- Deleting an account cascades to transactions.
- Deleting a category sets `Transaction.category_id` to `NULL`.
- `Category` enforces uniqueness for `(category_name, user_id)`.

## API Routes

This section is split into two groups:

- Implemented now (matches the current Flask code in `routes.py`)
- Planned for future implementation (kept here as project roadmap)

All implemented routes currently return JSON.

### Auth Routes (`/auth`)

- `POST /auth/register`
- `POST /auth/login`
- `POST /auth/logout` (login required)
- `GET /auth/current-user` (login required)

### User Routes (`/api`)

- `GET /api/users/<user_id>` (login required)
- `PUT /api/users/<user_id>` (login required)
- `DELETE /api/users/<user_id>` (login required)

### Account Routes (`/api`)

- `POST /api/users/<user_id>/accounts` (login required)
- `GET /api/users/<user_id>/accounts` (login required)
- `GET /api/accounts/<account_id>` (login required)
- `PUT /api/accounts/<account_id>` (login required)
- `DELETE /api/accounts/<account_id>` (login required)

### Category Routes (`/api`)

- `POST /api/users/<user_id>/categories` (login required)
- `GET /api/users/<user_id>/categories` (login required)
- `GET /api/categories/<category_id>` (login required)
- `PUT /api/categories/<category_id>` (login required)
- `DELETE /api/categories/<category_id>` (login required)

### Transaction Routes (`/api`)

- `POST /api/accounts/<account_id>/transactions` (login required)
- `GET /api/accounts/<account_id>/transactions` (login required)
- `GET /api/transactions/<transaction_id>` (login required)
- `PUT /api/transactions/<transaction_id>` (login required)
- `DELETE /api/transactions/<transaction_id>` (login required)

## Planned Routes (Future)

The following routes are intentionally documented for future work and are **not implemented yet**.

### Institution Routes (`/api`)

- `POST /api/institutions`
- `GET /api/institutions`
- `GET /api/institutions/<institution_id>`

### Analytics Routes (`/api`)

- `GET /api/users/<user_id>/budget-summary`
- `GET /api/accounts/<account_id>/balance-history`

### Planned Frontend/View Routes

Template files exist and are expected to be wired later to view routes (for example, pages related to login, profile, accounts, budgets, and transactions).


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
