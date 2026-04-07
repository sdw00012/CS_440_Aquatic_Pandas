"""
==============================================================================
AQUATIC PANDAS - Database Models (SQLAlchemy ORM)
CS440 Project - Budget Management System
==============================================================================

This file defines all database models using SQLAlchemy ORM.
Models are mapped to the database tables defined in init.sql.
"""

from app import db
from datetime import datetime

# ==============================================================================
# USER MODEL
# ==============================================================================

class User(db.Model):
    """
    PSEUDOCODE:
        TABLE: User
        PRIMARY KEY: user_id
        
        ATTRIBUTES:
            user_id: Integer (auto-increment)
            first_name: String (max 100)
            last_name: String (max 100)
            email: String (unique, max 255)
            phone: String (nullable, max 20)
            address: String (nullable, max 255)
            created_at: DateTime (auto-generated)
            updated_at: DateTime (auto-updated)
        
        RELATIONSHIPS:
            accounts: One-to-Many with Account
            categories: One-to-Many with Category
        
        METHODS:
            to_dict() -> dict
                RETURN serialized user data as dictionary
            
            get_total_budget() -> float
                QUERY all categories for this user
                CALCULATE sum of all budget values
                RETURN total
            
            get_accounts() -> list
                RETURN all accounts associated with user
            
            add_category(name, budget) -> Category
                VALIDATE name doesn't exist
                CREATE Category object
                ADD to database
                RETURN new category
    """
    __tablename__ = 'User'
    
    # Attributes
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    accounts = db.relationship('Account', back_populates='user', cascade='all, delete-orphan')
    categories = db.relationship('Category', back_populates='user', cascade='all, delete-orphan')
    
    def to_dict(self):
        """STUB: Return serialized user data"""
        pass
    
    def get_total_budget(self):
        """STUB: Calculate total budget across all categories"""
        pass
    
    def get_accounts(self):
        """STUB: Return all user accounts"""
        pass


# ==============================================================================
# INSTITUTION MODEL
# ==============================================================================

class Institution(db.Model):
    """
    PSEUDOCODE:
        TABLE: Institution
        PRIMARY KEY: institution_id
        
        ATTRIBUTES:
            institution_id: Integer (auto-increment)
            institution_name: String (unique, max 255)
            website: String (nullable, max 255)
            created_at: DateTime
            updated_at: DateTime
        
        RELATIONSHIPS:
            accounts: One-to-Many with Account
        
        METHODS:
            to_dict() -> dict
                RETURN serialized institution data
            
            get_accounts() -> list
                RETURN all accounts at this institution
    """
    __tablename__ = 'Institution'
    
    # Attributes
    institution_id = db.Column(db.Integer, primary_key=True)
    institution_name = db.Column(db.String(255), unique=True, nullable=False)
    website = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    accounts = db.relationship('Account', back_populates='institution')
    
    def to_dict(self):
        """STUB: Return serialized institution data"""
        pass


# ==============================================================================
# ACCOUNT MODEL
# ==============================================================================

class Account(db.Model):
    """
    PSEUDOCODE:
        TABLE: Account
        PRIMARY KEY: account_id
        FOREIGN KEYS: user_id (User), institution_id (Institution)
        
        ATTRIBUTES:
            account_id: Integer (auto-increment)
            account_name: String (max 255)
            account_type: String (max 50)
            user_id: Integer (foreign key)
            institution_id: Integer (foreign key)
            created_at: DateTime
            updated_at: DateTime
        
        RELATIONSHIPS:
            user: Many-to-One with User
            institution: Many-to-One with Institution
            transactions: One-to-Many with Transaction
        
        METHODS:
            to_dict() -> dict
                RETURN serialized account data
            
            get_balance() -> float
                QUERY all transactions for account
                CALCULATE: sum(inflows) - sum(outflows)
                RETURN balance
            
            get_transactions(start_date, end_date) -> list
                FILTER transactions by date range
                RETURN filtered transactions
            
            add_transaction(date, amount, type, payee, category, memo)
                VALIDATE amount > 0
                CREATE Transaction object
                ADD to database
                RETURN new transaction
    """
    __tablename__ = 'Account'
    
    # Attributes
    account_id = db.Column(db.Integer, primary_key=True)
    account_name = db.Column(db.String(255), nullable=False)
    account_type = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable=False)
    institution_id = db.Column(db.Integer, db.ForeignKey('Institution.institution_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', back_populates='accounts')
    institution = db.relationship('Institution', back_populates='accounts')
    transactions = db.relationship('Transaction', back_populates='account', cascade='all, delete-orphan')
    
    def to_dict(self):
        """STUB: Return serialized account data"""
        pass
    
    def get_balance(self):
        """STUB: Calculate account balance"""
        pass
    
    def get_transactions(self, start_date=None, end_date=None):
        """STUB: Get transactions within date range"""
        pass


# ==============================================================================
# CATEGORY MODEL
# ==============================================================================

class Category(db.Model):
    """
    PSEUDOCODE:
        TABLE: Category
        PRIMARY KEY: category_id
        FOREIGN KEY: user_id (User)
        UNIQUE CONSTRAINT: (category_name, user_id)
        
        ATTRIBUTES:
            category_id: Integer (auto-increment)
            category_name: String (max 255)
            budget: Decimal (2 decimal places)
            user_id: Integer (foreign key)
            created_at: DateTime
            updated_at: DateTime
        
        RELATIONSHIPS:
            user: Many-to-One with User
            transactions: One-to-Many with Transaction
        
        METHODS:
            to_dict() -> dict
                RETURN serialized category data
            
            get_spent_amount() -> float
                QUERY all transactions in category
                CALCULATE: sum(all outflows)
                RETURN total spent
            
            get_remaining_budget() -> float
                CALCULATE: budget - get_spent_amount()
                RETURN remaining
            
            is_over_budget() -> bool
                CHECK: get_spent_amount() > budget
                RETURN boolean
            
            get_transactions() -> list
                RETURN all transactions in this category
    """
    __tablename__ = 'Category'
    
    # Attributes
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(255), nullable=False)
    budget = db.Column(db.Numeric(10, 2), default=0.00)
    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Unique constraint on category_name and user_id
    __table_args__ = (db.UniqueConstraint('category_name', 'user_id', name='unique_category_per_user'),)
    
    # Relationships
    user = db.relationship('User', back_populates='categories')
    transactions = db.relationship('Transaction', back_populates='category', cascade='all, delete-orphan')
    
    def to_dict(self):
        """STUB: Return serialized category data"""
        pass
    
    def get_spent_amount(self):
        """STUB: Calculate total spent in category"""
        pass
    
    def get_remaining_budget(self):
        """STUB: Calculate remaining budget"""
        pass
    
    def is_over_budget(self):
        """STUB: Check if category is over budget"""
        pass


# ==============================================================================
# TRANSACTION MODEL
# ==============================================================================

class Transaction(db.Model):
    """
    PSEUDOCODE:
        TABLE: Transaction
        PRIMARY KEY: transaction_id
        FOREIGN KEYS: category_id (Category), account_id (Account)
        
        ATTRIBUTES:
            transaction_id: Integer (auto-increment)
            memo: String (nullable, max 255)
            date: Date (not nullable)
            outflow: Decimal (expense amount)
            payee: String (nullable, max 255)
            inflow: Decimal (income amount)
            category_id: Integer (foreign key, nullable)
            account_id: Integer (foreign key)
            created_at: DateTime
            updated_at: DateTime
        
        RELATIONSHIPS:
            category: Many-to-One with Category
            account: Many-to-One with Account
        
        METHODS:
            to_dict() -> dict
                RETURN serialized transaction data
            
            get_amount() -> float
                IF outflow > 0 RETURN outflow
                ELSE RETURN inflow
            
            get_type() -> string
                IF outflow > 0 RETURN "Expense"
                ELSE RETURN "Income"
            
            update_transaction(date, payee, amount, category, memo)
                VALIDATE new data
                UPDATE attributes
                SAVE to database
    """
    __tablename__ = 'Transaction'
    
    # Attributes
    transaction_id = db.Column(db.Integer, primary_key=True)
    memo = db.Column(db.String(255))
    date = db.Column(db.Date, nullable=False)
    outflow = db.Column(db.Numeric(10, 2), default=0.00)
    payee = db.Column(db.String(255))
    inflow = db.Column(db.Numeric(10, 2), default=0.00)
    category_id = db.Column(db.Integer, db.ForeignKey('Category.category_id'))
    account_id = db.Column(db.Integer, db.ForeignKey('Account.account_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    category = db.relationship('Category', back_populates='transactions')
    account = db.relationship('Account', back_populates='transactions')
    
    def to_dict(self):
        """STUB: Return serialized transaction data"""
        pass
    
    def get_amount(self):
        """STUB: Get transaction amount"""
        pass
    
    def get_type(self):
        """STUB: Get transaction type (income/expense)"""
        pass
