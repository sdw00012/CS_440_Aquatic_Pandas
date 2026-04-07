# ==============================================================================
# AQUATIC PANDAS - Flask Application Structure (PSEUDOCODE)
# CS440 Project - Budget Management System
# ==============================================================================

"""
Flask Application Architecture Overview:
- Database Models (ORM): SQLAlchemy-based model definitions
- Routes/Views: REST API endpoints for CRUD operations
- Services: Business logic layer for domain operations
- Utilities: Helper functions for common tasks
"""

# ==============================================================================
# DATABASE MODELS (models.py)
# ==============================================================================

"""
PSEUDOCODE for Database Models using SQLAlchemy ORM

class User(db.Model):
    # Table Configuration
    __tablename__ = 'User'
    
    # Attributes
    user_id: int (Primary Key, Auto-Increment)
    first_name: string (NOT NULL)
    last_name: string (NOT NULL)
    email: string (UNIQUE, NOT NULL)
    phone: string (NULLABLE)
    address: string (NULLABLE)
    created_at: datetime (Auto-generated)
    updated_at: datetime (Auto-updated)
    
    # Relationships
    accounts: List[Account]  # One-to-Many: User has many Accounts
    categories: List[Category]  # One-to-Many: User has many Categories
    
    # Methods
    def __init__(first_name, last_name, email, phone, address)
        INITIALIZE all attributes
        
    def to_dict() -> dict
        RETURN serialized user data
        
    def get_total_budget() -> float
        GET sum of all category budgets
        RETURN total budget amount
        
    def get_accounts() -> List[Account]
        RETURN all accounts associated with this user
        
    def add_category(category_name, budget) -> Category
        CREATE new category for this user
        VALIDATE category_name doesn't already exist
        RETURN newly created category


class Institution(db.Model):
    # Table Configuration
    __tablename__ = 'Institution'
    
    # Attributes
    institution_id: int (Primary Key, Auto-Increment)
    institution_name: string (UNIQUE, NOT NULL)
    website: string (NULLABLE)
    created_at: datetime
    updated_at: datetime
    
    # Relationships
    accounts: List[Account]  # One-to-Many: Institution has many Accounts
    
    # Methods
    def __init__(institution_name, website)
        INITIALIZE all attributes
        
    def to_dict() -> dict
        RETURN serialized institution data
        
    def get_accounts() -> List[Account]
        RETURN all accounts at this institution


class Account(db.Model):
    # Table Configuration
    __tablename__ = 'Account'
    
    # Attributes
    account_id: int (Primary Key, Auto-Increment)
    account_name: string (NOT NULL)
    account_type: string (NOT NULL)  # e.g., "Checking", "Savings", "Credit Card"
    user_id: int (Foreign Key -> User)
    institution_id: int (Foreign Key -> Institution)
    created_at: datetime
    updated_at: datetime
    
    # Relationships
    user: User  # Many-to-One: Account belongs to User
    institution: Institution  # Many-to-One: Account belongs to Institution
    transactions: List[Transaction]  # One-to-Many: Account has many Transactions
    
    # Methods
    def __init__(account_name, account_type, user_id, institution_id)
        INITIALIZE all attributes
        
    def to_dict() -> dict
        RETURN serialized account data
        
    def get_balance() -> float
        CALCULATE: sum(all inflows) - sum(all outflows)
        RETURN account balance
        
    def get_transactions(date_from, date_to) -> List[Transaction]
        FILTER transactions by date range
        RETURN filtered transactions
        
    def add_transaction(date, amount, type, payee, category_id, memo)
        CREATE new transaction for this account
        VALIDATE amount > 0
        RETURN newly created transaction


class Category(db.Model):
    # Table Configuration
    __tablename__ = 'Category'
    
    # Attributes
    category_id: int (Primary Key, Auto-Increment)
    category_name: string (NOT NULL)
    budget: decimal (NOT NULL, DEFAULT 0.00)
    user_id: int (Foreign Key -> User)
    created_at: datetime
    updated_at: datetime
    
    # Composite Unique Constraint: (category_name, user_id)
    
    # Relationships
    user: User  # Many-to-One: Category belongs to User
    transactions: List[Transaction]  # One-to-Many: Category has many Transactions
    
    # Methods
    def __init__(category_name, budget, user_id)
        INITIALIZE all attributes
        
    def to_dict() -> dict
        RETURN serialized category data
        
    def get_spent_amount() -> float
        CALCULATE: sum(all transaction outflows in this category)
        RETURN total spent
        
    def get_remaining_budget() -> float
        CALCULATE: budget - get_spent_amount()
        RETURN remaining budget
        
    def is_over_budget() -> bool
        CHECK: get_spent_amount() > budget
        RETURN boolean result
        
    def get_transactions() -> List[Transaction]
        RETURN all transactions in this category


class Transaction(db.Model):
    # Table Configuration
    __tablename__ = 'Transaction'
    
    # Attributes
    transaction_id: int (Primary Key, Auto-Increment)
    memo: string (NULLABLE)
    date: date (NOT NULL)
    outflow: decimal (DEFAULT 0.00)  # Money leaving account (expense)
    payee: string (NULLABLE)
    inflow: decimal (DEFAULT 0.00)   # Money entering account (income)
    category_id: int (Foreign Key -> Category, NULLABLE)
    account_id: int (Foreign Key -> Account)
    created_at: datetime
    updated_at: datetime
    
    # Relationships
    category: Category  # Many-to-One: Transaction belongs to Category
    account: Account  # Many-to-One: Transaction belongs to Account
    
    # Methods
    def __init__(date, payee, amount, type, account_id, category_id, memo)
        INITIALIZE all attributes
        IF type == "outflow"
            SET outflow = amount, inflow = 0
        ELSE IF type == "inflow"
            SET inflow = amount, outflow = 0
            
    def to_dict() -> dict
        RETURN serialized transaction data
        
    def get_amount() -> float
        IF outflow > 0 RETURN outflow
        ELSE RETURN inflow
        
    def get_type() -> string
        IF outflow > 0 RETURN "Expense"
        ELSE RETURN "Income"
        
    def update_transaction(date, payee, amount, category_id, memo)
        VALIDATE new data
        UPDATE all attributes
        SAVE changes

"""


# ==============================================================================
# FLASK ROUTES / API ENDPOINTS (routes.py or app.py)
# ==============================================================================

"""
PSEUDOCODE for Flask Application Routes

class AquaticPandasApp(Flask):
    # Flask Application Initialization
    
    def __init__()
        INITIALIZE Flask app with configurations
        CONFIGURE database connection
        REGISTER all routes
        SETUP error handlers
        
    # ==================================================================
    # USER ROUTES
    # ==================================================================
    
    @app.route('/api/users', methods=['POST'])
    def create_user()
        // CREATE new user
        GET first_name, last_name, email, phone, address FROM request.json
        VALIDATE all required fields present
        VALIDATE email format
        CHECK email doesn't already exist
        CREATE new User object
        ADD user to database
        COMMIT to database
        RETURN {status: "success", user_id: new_user.user_id}, 201
    
    
    @app.route('/api/users/<user_id>', methods=['GET'])
    def get_user(user_id: int)
        // RETRIEVE user profile
        FIND user by user_id
        IF user not found
            RETURN {error: "User not found"}, 404
        RETURN user.to_dict(), 200
        
        
    @app.route('/api/users/<user_id>', methods=['PUT'])
    def update_user(user_id: int)
        // UPDATE user profile
        FIND user by user_id
        IF user not found
            RETURN {error: "User not found"}, 404
        GET updated fields FROM request.json
        UPDATE user attributes
        COMMIT changes
        RETURN {status: "success", user: user.to_dict()}, 200
        
        
    @app.route('/api/users/<user_id>', methods=['DELETE'])
    def delete_user(user_id: int)
        // DELETE user account
        FIND user by user_id
        IF user not found
            RETURN {error: "User not found"}, 404
        DELETE user from database (cascades to accounts, categories, transactions)
        COMMIT changes
        RETURN {status: "success", message: "User deleted"}, 200
    
    
    # ==================================================================
    # ACCOUNT ROUTES
    # ==================================================================
    
    @app.route('/api/users/<user_id>/accounts', methods=['POST'])
    def create_account(user_id: int)
        // CREATE new account for user
        FIND user by user_id
        IF user not found
            RETURN {error: "User not found"}, 404
        GET account_name, account_type, institution_id FROM request.json
        VALIDATE all required fields
        FIND institution by institution_id
        IF institution not found
            RETURN {error: "Institution not found"}, 404
        CREATE new Account object
        ADD account to database
        COMMIT to database
        RETURN {status: "success", account: account.to_dict()}, 201
        
        
    @app.route('/api/users/<user_id>/accounts', methods=['GET'])
    def get_user_accounts(user_id: int)
        // RETRIEVE all accounts for user
        FIND user by user_id
        IF user not found
            RETURN {error: "User not found"}, 404
        GET all accounts where account.user_id == user_id
        FOR each account
            CALCULATE account balance
        RETURN {accounts: [account.to_dict() for account in accounts]}, 200
        
        
    @app.route('/api/accounts/<account_id>', methods=['GET'])
    def get_account(account_id: int)
        // RETRIEVE account details
        FIND account by account_id
        IF account not found
            RETURN {error: "Account not found"}, 404
        RETURN {account: account.to_dict(), balance: account.get_balance()}, 200
        
        
    @app.route('/api/accounts/<account_id>', methods=['PUT'])
    def update_account(account_id: int)
        // UPDATE account details
        FIND account by account_id
        IF account not found
            RETURN {error: "Account not found"}, 404
        GET updated fields FROM request.json
        UPDATE account attributes
        COMMIT changes
        RETURN {status: "success", account: account.to_dict()}, 200
        
        
    @app.route('/api/accounts/<account_id>', methods=['DELETE'])
    def delete_account(account_id: int)
        // DELETE account
        FIND account by account_id
        IF account not found
            RETURN {error: "Account not found"}, 404
        DELETE account from database (cascades to transactions)
        COMMIT changes
        RETURN {status: "success", message: "Account deleted"}, 200
    
    
    # ==================================================================
    # CATEGORY ROUTES
    # ==================================================================
    
    @app.route('/api/users/<user_id>/categories', methods=['POST'])
    def create_category(user_id: int)
        // CREATE new budget category
        FIND user by user_id
        IF user not found
            RETURN {error: "User not found"}, 404
        GET category_name, budget FROM request.json
        VALIDATE category_name doesn't already exist for this user
        VALIDATE budget >= 0
        CREATE new Category object
        ADD category to database
        COMMIT to database
        RETURN {status: "success", category: category.to_dict()}, 201
        
        
    @app.route('/api/users/<user_id>/categories', methods=['GET'])
    def get_user_categories(user_id: int)
        // RETRIEVE all categories for user
        FIND user by user_id
        IF user not found
            RETURN {error: "User not found"}, 404
        GET all categories where category.user_id == user_id
        FOR each category
            CALCULATE spent = category.get_spent_amount()
            CALCULATE remaining = category.get_remaining_budget()
            ADD calculations to response
        RETURN {categories: [category data with spent/remaining]}, 200
        
        
    @app.route('/api/categories/<category_id>', methods=['PUT'])
    def update_category(category_id: int)
        // UPDATE category budget
        FIND category by category_id
        IF category not found
            RETURN {error: "Category not found"}, 404
        GET updated fields FROM request.json
        VALIDATE budget >= 0
        UPDATE category
        COMMIT changes
        RETURN {status: "success", category: category.to_dict()}, 200
        
        
    @app.route('/api/categories/<category_id>', methods=['DELETE'])
    def delete_category(category_id: int)
        // DELETE category
        FIND category by category_id
        IF category not found
            RETURN {error: "Category not found"}, 404
        // Option 1: Delete category and set all transactions to NULL category
        DELETE category from database
        COMMIT changes
        RETURN {status: "success", message: "Category deleted"}, 200
    
    
    # ==================================================================
    # TRANSACTION ROUTES
    # ==================================================================
    
    @app.route('/api/accounts/<account_id>/transactions', methods=['POST'])
    def create_transaction(account_id: int)
        // CREATE new transaction
        FIND account by account_id
        IF account not found
            RETURN {error: "Account not found"}, 404
        GET date, amount, type, payee, category_id, memo FROM request.json
        VALIDATE date is valid and not in future
        VALIDATE amount > 0
        VALIDATE type is "income" or "expense"
        IF category_id is provided
            FIND category by category_id
            IF category not found
                RETURN {error: "Category not found"}, 404
        CREATE new Transaction object
        ADD transaction to database
        COMMIT to database
        RETURN {status: "success", transaction: transaction.to_dict()}, 201
        
        
    @app.route('/api/accounts/<account_id>/transactions', methods=['GET'])
    def get_account_transactions(account_id: int)
        // RETRIEVE transactions for account
        FIND account by account_id
        IF account not found
            RETURN {error: "Account not found"}, 404
        GET query params: start_date, end_date, category_id
        QUERY all transactions for account
        IF start_date provided
            FILTER transactions >= start_date
        IF end_date provided
            FILTER transactions <= end_date
        IF category_id provided
            FILTER transactions where category_id matches
        SORT transactions by date (descending)
        RETURN {transactions: [transaction.to_dict()]}, 200
        
        
    @app.route('/api/transactions/<transaction_id>', methods=['GET'])
    def get_transaction(transaction_id: int)
        // RETRIEVE transaction details
        FIND transaction by transaction_id
        IF transaction not found
            RETURN {error: "Transaction not found"}, 404
        RETURN {transaction: transaction.to_dict()}, 200
        
        
    @app.route('/api/transactions/<transaction_id>', methods=['PUT'])
    def update_transaction(transaction_id: int)
        // UPDATE transaction
        FIND transaction by transaction_id
        IF transaction not found
            RETURN {error: "Transaction not found"}, 404
        GET updated fields FROM request.json
        VALIDATE all data
        UPDATE transaction attributes
        COMMIT changes
        RETURN {status: "success", transaction: transaction.to_dict()}, 200
        
        
    @app.route('/api/transactions/<transaction_id>', methods=['DELETE'])
    def delete_transaction(transaction_id: int)
        // DELETE transaction
        FIND transaction by transaction_id
        IF transaction not found
            RETURN {error: "Transaction not found"}, 404
        DELETE transaction from database
        COMMIT changes
        RETURN {status: "success", message: "Transaction deleted"}, 200
        
        
    @app.route('/api/categories/<category_id>/transactions', methods=['GET'])
    def get_category_transactions(category_id: int)
        // RETRIEVE all transactions in category
        FIND category by category_id
        IF category not found
            RETURN {error: "Category not found"}, 404
        GET all transactions where transaction.category_id == category_id
        RETURN {transactions: [transaction.to_dict()]}, 200
    
    
    # ==================================================================
    # INSTITUTION ROUTES
    # ==================================================================
    
    @app.route('/api/institutions', methods=['POST'])
    def create_institution()
        // CREATE new institution
        GET institution_name, website FROM request.json
        VALIDATE institution_name is provided
        CHECK institution_name doesn't already exist
        CREATE new Institution object
        ADD to database
        COMMIT changes
        RETURN {status: "success", institution: institution.to_dict()}, 201
        
        
    @app.route('/api/institutions', methods=['GET'])
    def get_all_institutions()
        // RETRIEVE all institutions
        GET all institutions from database
        RETURN {institutions: [institution.to_dict()]}, 200
        
        
    @app.route('/api/institutions/<institution_id>', methods=['GET'])
    def get_institution(institution_id: int)
        // RETRIEVE institution details
        FIND institution by institution_id
        IF institution not found
            RETURN {error: "Institution not found"}, 404
        RETURN {institution: institution.to_dict()}, 200
    
    
    # ==================================================================
    # ANALYTICS / REPORTING ROUTES
    # ==================================================================
    
    @app.route('/api/users/<user_id>/budget-summary', methods=['GET'])
    def get_budget_summary(user_id: int)
        // GET budget overview for user
        FIND user by user_id
        IF user not found
            RETURN {error: "User not found"}, 404
        GET all categories for user
        FOR each category
            spent = category.get_spent_amount()
            remaining = category.get_remaining_budget()
            is_over = category.is_over_budget()
            ADD to summary
        RETURN {
            summary: [category summaries],
            total_budget: user.get_total_budget(),
            total_spent: sum(all spent amounts),
            total_remaining: remaining
        }, 200
        
        
    @app.route('/api/accounts/<account_id>/balance-history', methods=['GET'])
    def get_balance_history(account_id: int)
        // GET balance history for account over time
        FIND account by account_id
        IF account not found
            RETURN {error: "Account not found"}, 404
        GET query param: time_period (week, month, year)
        CALCULATE balance at each time point
        RETURN {balance_history: [date, balance pairs]}, 200
        
        
    # ==================================================================
    # ERROR HANDLERS
    # ==================================================================
    
    @app.errorhandler(400)
    def handle_bad_request(error)
        RETURN {error: "Bad request"}, 400
        
    @app.errorhandler(404)
    def handle_not_found(error)
        RETURN {error: "Resource not found"}, 404
        
    @app.errorhandler(500)
    def handle_internal_error(error)
        LOG error
        RETURN {error: "Internal server error"}, 500

"""
