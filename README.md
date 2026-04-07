# Aquatic Pandas - Budget Management System
## CS440 Project

A comprehensive budget management system built with Python, Flask, and MySQL. The application allows users to track accounts, manage budgets across categories, and monitor transactions.

---

## Project Overview

**Aquatic Pandas** is a personal finance management application that helps users:
- Manage multiple accounts across different financial institutions
- Track income and expenses through transactions
- Create and monitor budget categories
- View spending patterns and budget summaries
- Analyze financial data with detailed reporting

**Tech Stack:**
- **Backend:** Python 3.11 + Flask 3.0
- **Database:** MySQL 8.0
- **ORM:** SQLAlchemy 2.0
- **Docker:** Docker & Docker Compose for containerization
- **Server Port:** 3000 (localhost)

---

## Project Structure

```
CS_440_Aquatic_Pandas/
├── app.py                        # Flask application entry point
├── models.py                     # SQLAlchemy ORM models
├── routes.py                     # API endpoints/routes
├── init.sql                      # Database schema initialization
├── docker-compose.yml            # Docker Compose configuration
├── Dockerfile                    # Flask app container definition
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment variables template
├── .gitignore                    # Git ignore rules
├── APPLICATION_PSEUDOCODE.md     # Detailed pseudocode documentation
└── README.md                     # This file
```

### File Descriptions

| File | Purpose |
|------|---------|
| **app.py** | Flask application factory, initialization, and main entry point |
| **models.py** | SQLAlchemy ORM model definitions (User, Account, Institution, Category, Transaction) |
| **routes.py** | RESTful API endpoints organized by resource type |
| **init.sql** | SQL script to initialize database schema and tables |
| **docker-compose.yml** | Orchestrates Flask app and MySQL database containers |
| **Dockerfile** | Builds Docker image for Flask application |
| **requirements.txt** | Python package dependencies |
| **APPLICATION_PSEUDOCODE.md** | Comprehensive pseudocode for database models and API routes |

---

## Database Schema

### Entities

**User**
- Stores user account information
- Primary Key: `user_id`
- Relationships: Has many Accounts and Categories

**Institution**
- Financial institutions/banks
- Primary Key: `institution_id`
- Relationships: Has many Accounts

**Account**
- User's financial accounts (checking, savings, credit card, etc.)
- Primary Key: `account_id`
- Foreign Keys: `user_id`, `institution_id`
- Relationships: Has many Transactions

**Category**
- Budget categories for transaction classification
- Primary Key: `category_id`
- Foreign Key: `user_id`
- Relationships: Has many Transactions
- Unique Constraint: (category_name, user_id)

**Transaction**
- Financial transactions (income/expenses)
- Primary Key: `transaction_id`
- Foreign Keys: `account_id`, `category_id`
- Types: Inflow (income) or Outflow (expense)

---

## Getting Started

### Prerequisites
- Docker & Docker Compose installed
- Git for version control
- (Optional) Python 3.11+ for local development

### Quick Start with Docker

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd CS_440_Aquatic_Pandas
   ```

2. **Copy environment file**
   ```bash
   cp .env.example .env
   ```

3. **Start the application**
   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   - Flask Server: http://localhost:3000
   - MySQL Database: localhost:3306
   - Default credentials:
     - User: `pandas_user`
     - Password: `pandas_password`
     - Database: `aquatic_pandas`

5. **Stop the application**
   ```bash
   docker-compose down
   ```

### Local Development (Without Docker)

1. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up database**
   - Install MySQL server locally
   - Create database: `aquatic_pandas`
   - Run: `mysql -u root < init.sql`

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with local database credentials
   ```

5. **Run the application**
   ```bash
   flask run --host=0.0.0.0 --port=3000
   ```

---

## API Endpoints

### User Management
- `POST /api/users` - Create user
- `GET /api/users/<user_id>` - Get user profile
- `PUT /api/users/<user_id>` - Update user
- `DELETE /api/users/<user_id>` - Delete user

### Accounts
- `POST /api/users/<user_id>/accounts` - Create account
- `GET /api/users/<user_id>/accounts` - List user accounts
- `GET /api/accounts/<account_id>` - Get account details
- `PUT /api/accounts/<account_id>` - Update account
- `DELETE /api/accounts/<account_id>` - Delete account

### Categories
- `POST /api/users/<user_id>/categories` - Create category
- `GET /api/users/<user_id>/categories` - List user categories
- `PUT /api/categories/<category_id>` - Update category
- `DELETE /api/categories/<category_id>` - Delete category
- `GET /api/categories/<category_id>/transactions` - Get category transactions

### Transactions
- `POST /api/accounts/<account_id>/transactions` - Create transaction
- `GET /api/accounts/<account_id>/transactions` - List account transactions
- `GET /api/transactions/<transaction_id>` - Get transaction details
- `PUT /api/transactions/<transaction_id>` - Update transaction
- `DELETE /api/transactions/<transaction_id>` - Delete transaction

### Institutions
- `POST /api/institutions` - Create institution
- `GET /api/institutions` - List all institutions
- `GET /api/institutions/<institution_id>` - Get institution details

### Analytics
- `GET /api/users/<user_id>/budget-summary` - Get budget overview
- `GET /api/accounts/<account_id>/balance-history` - Get balance trend

---

## Development Workflow

### Database Management
```bash
# View database (from container)
docker exec -it aquatic_pandas_db mysql -u pandas_user -p aquatic_pandas

# Apply schema changes
docker exec -i aquatic_pandas_db mysql -u pandas_user -p aquatic_pandas < init.sql
```

### Application Logs
```bash
# View Flask app logs
docker-compose logs -f app

# View MySQL logs
docker-compose logs -f db
```

### Port Conflicts
If port 3000 or 3306 are in use:
1. Edit `docker-compose.yml`
2. Change the port mappings
3. Restart containers

---

## Documentation Files

- **APPLICATION_PSEUDOCODE.md** - Contains detailed pseudocode for:
  - Complete API endpoint logic flow
  - Database model structures and methods
  - Business logic implementation guides
  - Error handling strategies

---

## Learning Resources

### Project Structure
The codebase is organized using:
- **Factory Pattern** - Flask app initialization
- **ORM Patterns** - SQLAlchemy models
- **RESTful Architecture** - Stateless API design
- **Blueprint Organization** - Route grouping

### Model Architecture
Each model follows standard patterns:
- Defines table schema with constraints
- Implements relationships with other models
- Provides helper/business logic methods
- Includes serialization (to_dict) methods

---

## Troubleshooting

### Container Issues
```bash
# Rebuild containers
docker-compose build --no-cache

# Reset everything
docker-compose down -v
docker-compose up --build
```

### Database Connection Errors
- Verify MySQL is healthy: `docker-compose ps`
- Check container logs: `docker-compose logs db`
- Ensure database exists and user credentials are correct

### Port Already in Use
```bash
# Find process using port 3000
lsof -i :3000
# Kill process
kill -9 <PID>
```

---

## License

This is a CS440 academic project.

---

## Team

**Aquatic Pandas Team**
- CS440 Course Project
- Date: 2026-03-28