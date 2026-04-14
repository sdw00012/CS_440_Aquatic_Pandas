# Docker Setup Guide - Aquatic Pandas

## Prerequisites
- Docker Desktop installed ([Download here](https://www.docker.com/products/docker-desktop))
- Docker Compose (included with Docker Desktop)

## Quick Start

### 1. **Build and Run the Containers**

```bash
# Navigate to project directory
cd /...../CS_440_Aquatic_Pandas

# Start everything (builds image + starts containers + initializes DB)
docker-compose up

# Or start in background mode
docker-compose up -d
```

### 2. **Access the Application**

Once the containers are running, your app is available at:
- **Web Server**: http://localhost:5000
- **MySQL Database**: localhost:3306

### 3. **Test the Backend**

```bash
# Test Login Endpoint
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'

# Test Register Endpoint
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "password": "secure123"
  }'
```

## Useful Docker Commands

```bash
# View running containers
docker-compose ps

# View application logs
docker-compose logs -f app

# View database logs
docker-compose logs -f db

# Stop all containers
docker-compose stop

# Stop and remove all containers
docker-compose down

# Remove all containers and volumes (clean slate)
docker-compose down -v

# Access MySQL database inside container
docker-compose exec db mysql -u pandas_user -p aquatic_pandas
# Password: pandas_password

# Run bash inside app container
docker-compose exec app bash
```

## File Structure

```
.
├── Dockerfile              # Defines Flask app container
├── docker-compose.yml      # Orchestrates app + database containers
├── .env.example           # Example environment variables
├── app.py                 # Flask app entry point
├── models.py              # Database models
├── routes.py              # API endpoints
├── init.sql               # Database initialization script
└── requirements.txt       # Python dependencies
```

## Services

### App Service (Flask)
- **Container Name**: aquatic_pandas_app
- **Port**: 5000 (localhost:5000)
- **Environment**: Development mode with hot reload
- **Volume**: Current directory mounted for live code changes

### Database Service (MySQL 8.0)
- **Container Name**: aquatic_pandas_db
- **Port**: 3306 (localhost:3306)
- **User**: pandas_user
- **Password**: pandas_password
- **Database**: aquatic_pandas
- **Volume**: Data persists in named volume `mysql_data`

## Environment Variables

The Docker setup uses these variables (from `docker-compose.yml`):
- `FLASK_ENV`: development
- `FLASK_HOST`: 0.0.0.0
- `FLASK_PORT`: 5000
- `DB_HOST`: db (container name)
- `DB_PORT`: 3306
- `DB_USER`: pandas_user
- `DB_PASSWORD`: pandas_password
- `DB_NAME`: aquatic_pandas

To override these, create a `.env` file in the project root:
```
FLASK_ENV=development
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
SECRET_KEY=your-secret-key
DB_HOST=db
DB_PORT=3306
DB_USER=pandas_user
DB_PASSWORD=pandas_password
DB_NAME=aquatic_pandas
```

## Database Initialization

When the `db` service starts:
1. Creates MySQL container
2. Runs `init.sql` (auto-imported via `/docker-entrypoint-initdb.d/`)
3. Creates database and all tables
4. Waits for health check to pass before starting Flask app

## Troubleshooting

### "Address already in use"
Another service is using port 5000 or 3306:
```bash
# Find and kill process on port 5000
lsof -i :5000
kill -9 <PID>

# Or use different ports in docker-compose.yml
# Change "5000:5000" to "5001:5000" etc
```

### "Cannot connect to database"
- Make sure `db` service is healthy: `docker-compose ps`
- Check database logs: `docker-compose logs db`
- Wait a bit longer (first startup can take 30+ seconds)

### "Database file is corrupted"
Clean up everything and restart:
```bash
docker-compose down -v
docker-compose up
```

### View application logs
```bash
docker-compose logs app -f
```

## Production Deployment Notes

When deploying to production, update:
1. `SECRET_KEY` in environment to a production-grade secret
2. `FLASK_ENV` to `production` (disables debug mode)
3. Database credentials to secure values
4. Consider using a proper WSGI server (Gunicorn) instead of Flask's dev server
5. Use a reverse proxy (Nginx) in front

## Next Steps

- Frontend development in separate branch
- Add more features to backend
- Configure CI/CD pipeline
- Set up proper logging
- Add database backups strategy
