# Aquatic Pandas API Testing Guide

This guide tests the backend in its current state using curl.

## 1. Start Services

```bash
./restart.sh
```

Use this variable in the same terminal:

```bash
export COOKIE_FILE="./cookies.txt"
rm -f "$COOKIE_FILE"
```

## 2. Create Prerequisite Institution (Required For Account Tests)

There is currently no Institution API route, so insert one directly in MySQL.

```bash
docker compose exec db mysql -u pandas_user -p pandas_password aquatic_pandas -e "INSERT INTO Institution (institution_name, website) VALUES ('Chase', 'https://www.chase.com');"
```

Optional: confirm it exists.

```bash
docker compose exec db mysql -u pandas_user -p pandas_password aquatic_pandas -e "SELECT institution_id, institution_name FROM Institution;"
```

Assume institution_id is 1 in commands below.

## 3. Authentication Endpoints

### Register (POST /auth/register)

```bash
curl -s -X POST "http://localhost:3000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "password": "secure123",
    "phone": "",
    "address": ""
  }'
```

### Login (POST /auth/login) and Save Session Cookie

```bash
curl -s -c "$COOKIE_FILE" -X POST "http://localhost:3000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"john@example.com","password":"secure123"}'
```

### Current User (GET /auth/current-user)

```bash
curl -s -b "$COOKIE_FILE" "http://localhost:3000/auth/current-user"
```

### Logout (POST /auth/logout)

```bash
curl -s -b "$COOKIE_FILE" -X POST "http://localhost:3000/auth/logout"
```

### Current User After Logout (Expected Unauthorized)

```bash
curl -s -b "$COOKIE_FILE" "http://localhost:3000/auth/current-user"
```

## 4. Login Again For Protected Route Tests

```bash
curl -s -c "$COOKIE_FILE" -X POST "http://localhost:3000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"john@example.com","password":"secure123"}'
```

Assume user_id is 1 for a fresh database.

## 5. User Endpoints

### Get User (GET /api/users/1)

```bash
curl -s -b "$COOKIE_FILE" "http://localhost:3000/api/users/1"
```

### Update User (PUT /api/users/1)

```bash
curl -s -b "$COOKIE_FILE" -X PUT "http://localhost:3000/api/users/1" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Johnny",
    "last_name": "Doe",
    "phone": "555-123-4567",
    "address": "123 Test St"
  }'
```

## 6. Account Endpoints

### Create Account (POST /api/users/1/accounts)

```bash
curl -s -b "$COOKIE_FILE" -X POST "http://localhost:3000/api/users/1/accounts" \
  -H "Content-Type: application/json" \
  -d '{
    "account_name": "Main Checking",
    "account_type": "Checking",
    "institution_id": 1
  }'
```

Assume account_id is 1 for a fresh database.

### Get User Accounts (GET /api/users/1/accounts)

```bash
curl -s -b "$COOKIE_FILE" "http://localhost:3000/api/users/1/accounts"
```

### Get Account (GET /api/accounts/1)

```bash
curl -s -b "$COOKIE_FILE" "http://localhost:3000/api/accounts/1"
```

### Update Account (PUT /api/accounts/1)

```bash
curl -s -b "$COOKIE_FILE" -X PUT "http://localhost:3000/api/accounts/1" \
  -H "Content-Type: application/json" \
  -d '{
    "account_name": "Primary Checking",
    "account_type": "Checking",
    "institution_id": 1
  }'
```

## 7. Category Endpoints

### Create Category (POST /api/users/1/categories)

```bash
curl -s -b "$COOKIE_FILE" -X POST "http://localhost:3000/api/users/1/categories" \
  -H "Content-Type: application/json" \
  -d '{
    "category_name": "Groceries",
    "budget": 500
  }'
```

Assume category_id is 1 for a fresh database.

### Get User Categories (GET /api/users/1/categories)

```bash
curl -s -b "$COOKIE_FILE" "http://localhost:3000/api/users/1/categories"
```

### Get Category (GET /api/categories/1)

```bash
curl -s -b "$COOKIE_FILE" "http://localhost:3000/api/categories/1"
```

### Update Category (PUT /api/categories/1)

```bash
curl -s -b "$COOKIE_FILE" -X PUT "http://localhost:3000/api/categories/1" \
  -H "Content-Type: application/json" \
  -d '{
    "category_name": "Food",
    "budget": 650
  }'
```

## 8. Transaction Endpoints

### Create Transaction (POST /api/accounts/1/transactions)

```bash
curl -s -b "$COOKIE_FILE" -X POST "http://localhost:3000/api/accounts/1/transactions" \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2026-04-16",
    "payee": "Trader Joes",
    "memo": "Weekly groceries",
    "outflow": 84.22,
    "inflow": 0,
    "category_id": 1
  }'
```

Assume transaction_id is 1 for a fresh database.

### Get Account Transactions (GET /api/accounts/1/transactions)

```bash
curl -s -b "$COOKIE_FILE" "http://localhost:3000/api/accounts/1/transactions"
```

### Get Account Transactions In Date Range

```bash
curl -s -b "$COOKIE_FILE" "http://localhost:3000/api/accounts/1/transactions?start_date=2026-04-01&end_date=2026-04-30"
```

### Get Transaction (GET /api/transactions/1)

```bash
curl -s -b "$COOKIE_FILE" "http://localhost:3000/api/transactions/1"
```

### Update Transaction (PUT /api/transactions/1)

```bash
curl -s -b "$COOKIE_FILE" -X PUT "http://localhost:3000/api/transactions/1" \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2026-04-17",
    "payee": "Trader Joes",
    "memo": "Updated memo",
    "outflow": 90.00,
    "inflow": 0,
    "category_id": 1
  }'
```

### Delete Transaction (DELETE /api/transactions/1)

```bash
curl -s -b "$COOKIE_FILE" -X DELETE "http://localhost:3000/api/transactions/1"
```

## 9. Delete Endpoints

### Delete Category (DELETE /api/categories/1)

```bash
curl -s -b "$COOKIE_FILE" -X DELETE "http://localhost:3000/api/categories/1"
```

### Delete Account (DELETE /api/accounts/1)

```bash
curl -s -b "$COOKIE_FILE" -X DELETE "http://localhost:3000/api/accounts/1"
```

### Delete User (DELETE /api/users/1)

```bash
curl -s -b "$COOKIE_FILE" -X DELETE "http://localhost:3000/api/users/1"
```

## 10. Helpful Docker Debug Commands

```bash
docker compose ps
docker compose logs -f app
docker compose logs -f db
```

## Notes

- Protected endpoints require a valid session cookie created by login.
- If IDs differ from 1 in your database, replace them in the commands.
- If you want a clean slate for repeat testing, run:

```bash
docker compose down -v
./restart.sh
```
