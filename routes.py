"""
==============================================================================
AQUATIC PANDAS - API Routes
CS440 Project - Budget Management System
==============================================================================

This file defines all Flask routes/API endpoints for the application.
Routes are organized by resource type:
- Authentication (login, register, logout)
- Users (profile management)
- Accounts (account management)
- Categories (budget categories)
- Transactions (financial records)
"""

from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db
from models import User, Account, Institution, Category, Transaction
from datetime import datetime
import re

# Create Blueprints for organizing routes
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
api_bp = Blueprint('api', __name__, url_prefix='/api')

# ==============================================================================
# AUTHENTICATION ROUTES
# ==============================================================================

def validate_email(email):
    """Validate email format"""
    # Basic email-format guard for registration.
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user account
    
    REQUEST BODY: {
        first_name: str (required),
        last_name: str (required),
        email: str (required, unique),
        password: str (required, min 6 chars),
        phone: str (optional),
        address: str (optional)
    }
    
    RESPONSE: 
        201 Created: {status: 'success', user_id: int, message: 'User created'}
        400 Bad Request: {status: 'error', message: 'error details'}
        409 Conflict: {status: 'error', message: 'Email already exists'}
    """
    try:
        # Parse JSON payload from request body.
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['first_name', 'last_name', 'email', 'password']
        if not all(field in data for field in required_fields):
            return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400
        
        # Validate email format
        if not validate_email(data['email']):
            return jsonify({'status': 'error', 'message': 'Invalid email format'}), 400
        
        # Check if email already exists
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return jsonify({'status': 'error', 'message': 'Email already registered'}), 409
        
        # Build model object from request payload.
        new_user = User(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            phone=data.get('phone', ''),
            address=data.get('address', '')
        )
        
        # Set password (will be hashed)
        new_user.set_password(data['password'])
        
        # Persist the new user row.
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'User registered successfully',
            'user_id': new_user.user_id
        }), 201
        
    except ValueError as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': 'Server error: ' + str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login user with email and password
    
    REQUEST BODY: {
        email: str (required),
        password: str (required)
    }
    
    RESPONSE:
        200 OK: {
            status: 'success',
            message: 'Login successful',
            user: {user_data},
            user_id: int
        }
        401 Unauthorized: {status: 'error', message: 'Invalid credentials'}
        400 Bad Request: {status: 'error', message: 'Missing fields'}
    """
    try:
        # Parse login payload and validate required credentials.
        data = request.get_json()
        
        # Validate required fields
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'status': 'error', 'message': 'Missing email or password'}), 400
        
        # Find user by email
        user = User.query.filter_by(email=data['email']).first()
        
        # Check if user exists and password is correct
        if not user or not user.check_password(data['password']):
            return jsonify({'status': 'error', 'message': 'Invalid email or password'}), 401
        
        # Create authenticated session for this user.
        login_user(user, remember=True)
        
        return jsonify({
            'status': 'success',
            'message': 'Login successful',
            'user': user.to_dict(),
            'user_id': user.user_id
        }), 200
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': 'Server error: ' + str(e)}), 500


@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """
    Logout current user
    
    RESPONSE:
        200 OK: {status: 'success', message: 'Logout successful'}
        401 Unauthorized: {status: 'error', message: 'Not logged in'}
    """
    try:
        # Clear current login session.
        logout_user()
        return jsonify({'status': 'success', 'message': 'Logout successful'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': 'Server error: ' + str(e)}), 500


@auth_bp.route('/current-user', methods=['GET'])
@login_required
def get_current_user():
    """
    Get current logged-in user information
    
    RESPONSE:
        200 OK: {status: 'success', user: {user_data}}
        401 Unauthorized: {status: 'error', message: 'Not logged in'}
    """
    # current_user is injected by Flask-Login after authentication.
    return jsonify({
        'status': 'success',
        'user': current_user.to_dict()
    }), 200


# ==============================================================================
# USER ROUTES
# ==============================================================================

@api_bp.route('/users/<int:user_id>', methods=['GET'])
@login_required
def get_user(user_id):
    """
    Get user profile
    Users can only view their own profile unless they're admin
    
    RESPONSE:
        200 OK: {status: 'success', user: {user_data}}
        404 Not Found: {status: 'error', message: 'User not found'}
        403 Forbidden: {status: 'error', message: 'Cannot view this user'}
    """
    try:
        # Check authorization
        if current_user.user_id != user_id:
            return jsonify({'status': 'error', 'message': 'Cannot view this user'}), 403
        
        # Load target user record.
        user = User.query.get(user_id)
        if not user:
            return jsonify({'status': 'error', 'message': 'User not found'}), 404
        
        return jsonify({
            'status': 'success',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': 'Server error: ' + str(e)}), 500


@api_bp.route('/users/<int:user_id>', methods=['PUT'])
@login_required
def update_user(user_id):
    """
    Update user profile information
    Users can only update their own profile
    
    REQUEST BODY: {
        first_name: str (optional),
        last_name: str (optional),
        phone: str (optional),
        address: str (optional)
    }
    
    RESPONSE:
        200 OK: {status: 'success', user: {updated_user_data}}
        404 Not Found: {status: 'error', message: 'User not found'}
        403 Forbidden: {status: 'error', message: 'Cannot update this user'}
    """
    try:
        # Check authorization
        if current_user.user_id != user_id:
            return jsonify({'status': 'error', 'message': 'Cannot update this user'}), 403
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'status': 'error', 'message': 'User not found'}), 404
        
        # Apply partial updates from request body.
        data = request.get_json()
        
        # Update allowed fields
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'phone' in data:
            user.phone = data['phone']
        if 'address' in data:
            user.address = data['address']
        
        # Persist profile changes.
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': 'Server error: ' + str(e)}), 500


@api_bp.route('/users/<int:user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
    """
    Delete user account (cascades to all related data)
    Users can only delete their own account
    
    RESPONSE:
        200 OK: {status: 'success', message: 'User deleted'}
        404 Not Found: {status: 'error', message: 'User not found'}
        403 Forbidden: {status: 'error', message: 'Cannot delete this user'}
    """
    try:
        # Check authorization
        if current_user.user_id != user_id:
            return jsonify({'status': 'error', 'message': 'Cannot delete this user'}), 403
        
        # Load then delete user; cascades remove linked data by schema rules.
        user = User.query.get(user_id)
        if not user:
            return jsonify({'status': 'error', 'message': 'User not found'}), 404
        
        db.session.delete(user)
        db.session.commit()
        
        # Logout the user
        logout_user()
        
        return jsonify({
            'status': 'success',
            'message': 'User deleted successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': 'Server error: ' + str(e)}), 500


# ==============================================================================
# ACCOUNT ROUTES
# ==============================================================================

@api_bp.route('/users/<int:user_id>/accounts', methods=['POST'])
@login_required
def create_account(user_id):
    """
    Create new account for user
    Users can only create accounts for themselves
    
    REQUEST BODY: {
        account_name: str (required),
        account_type: str (required, e.g., 'Checking', 'Savings'),
        institution_id: int (required)
    }
    
    RESPONSE:
        201 Created: {status: 'success', account: {account_data}}
        400 Bad Request: {status: 'error', message: 'Missing fields'}
        403 Forbidden: {status: 'error', message: 'Cannot create account'}
        404 Not Found: {status: 'error', message: 'Institution not found'}
    """
    try:
        # Check authorization
        if current_user.user_id != user_id:
            return jsonify({'status': 'error', 'message': 'Cannot create account for this user'}), 403
        
        # Parse and validate account creation payload.
        data = request.get_json()
        
        # Validate required fields
        if not data or not data.get('account_name') or not data.get('account_type') or not data.get('institution_id'):
            return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400
        
        # Check if institution exists
        institution = Institution.query.get(data['institution_id'])
        if not institution:
            return jsonify({'status': 'error', 'message': 'Institution not found'}), 404
        
        # Create new account
        new_account = Account(
            account_name=data['account_name'],
            account_type=data['account_type'],
            user_id=user_id,
            institution_id=data['institution_id']
        )
        
        # Persist the new account record.
        db.session.add(new_account)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'account': new_account.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': 'Server error: ' + str(e)}), 500


@api_bp.route('/users/<int:user_id>/accounts', methods=['GET'])
@login_required
def get_user_accounts(user_id):
    """
    Get all accounts for user with balances
    Users can only view their own accounts
    
    RESPONSE:
        200 OK: {status: 'success', accounts: [{account_data}]}
        403 Forbidden: {status: 'error', message: 'Cannot view accounts'}
    """
    try:
        # Check authorization
        if current_user.user_id != user_id:
            return jsonify({'status': 'error', 'message': 'Cannot view these accounts'}), 403
        
        accounts = Account.query.filter_by(user_id=user_id).all()
        
        return jsonify({
            'status': 'success',
            'accounts': [account.to_dict() for account in accounts]
        }), 200
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': 'Server error: ' + str(e)}), 500


@api_bp.route('/accounts/<int:account_id>', methods=['GET'])
@login_required
def get_account(account_id):
    """
    Get account details with balance
    
    RESPONSE:
        200 OK: {status: 'success', account: {account_data}}
        404 Not Found: {status: 'error', message: 'Account not found'}
        403 Forbidden: {status: 'error', message: 'Cannot view this account'}
    """
    try:
        account = Account.query.get(account_id)
        if not account:
            return jsonify({'status': 'error', 'message': 'Account not found'}), 404
        
        # Check authorization
        if current_user.user_id != account.user_id:
            return jsonify({'status': 'error', 'message': 'Cannot view this account'}), 403
        
        return jsonify({
            'status': 'success',
            'account': account.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': 'Server error: ' + str(e)}), 500


@api_bp.route('/accounts/<int:account_id>', methods=['PUT'])
@login_required
def update_account(account_id):
    """
    Update account details
    
    REQUEST BODY: {
        account_name: str (optional),
        account_type: str (optional),
        institution_id: int (optional)
    }
    
    RESPONSE:
        200 OK: {status: 'success', account: {updated_account_data}}
        404 Not Found: {status: 'error', message: 'Account not found'}
        403 Forbidden: {status: 'error', message: 'Cannot update this account'}
    """
    try:
        account = Account.query.get(account_id)
        if not account:
            return jsonify({'status': 'error', 'message': 'Account not found'}), 404
        
        # Check authorization
        if current_user.user_id != account.user_id:
            return jsonify({'status': 'error', 'message': 'Cannot update this account'}), 403
        
        # Apply optional field updates.
        data = request.get_json()
        
        # Update allowed fields
        if 'account_name' in data:
            account.account_name = data['account_name']
        if 'account_type' in data:
            account.account_type = data['account_type']
        if 'institution_id' in data:
            # Verify institution exists
            institution = Institution.query.get(data['institution_id'])
            if not institution:
                return jsonify({'status': 'error', 'message': 'Institution not found'}), 404
            account.institution_id = data['institution_id']
        
        # Persist account updates.
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'account': account.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': 'Server error: ' + str(e)}), 500


@api_bp.route('/accounts/<int:account_id>', methods=['DELETE'])
@login_required
def delete_account(account_id):
    """
    Delete account and all associated transactions
    
    RESPONSE:
        200 OK: {status: 'success', message: 'Account deleted'}
        404 Not Found: {status: 'error', message: 'Account not found'}
        403 Forbidden: {status: 'error', message: 'Cannot delete this account'}
    """
    try:
        account = Account.query.get(account_id)
        if not account:
            return jsonify({'status': 'error', 'message': 'Account not found'}), 404
        
        # Check authorization
        if current_user.user_id != account.user_id:
            return jsonify({'status': 'error', 'message': 'Cannot delete this account'}), 403
        
        db.session.delete(account)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Account deleted successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': 'Server error: ' + str(e)}), 500


# ==============================================================================
# CATEGORY ROUTES
# ==============================================================================

@api_bp.route('/users/<int:user_id>/categories', methods=['POST'])
@login_required
def create_category(user_id):
    """
    Create budget category for user
    Users can only create categories for themselves
    
    REQUEST BODY: {
        category_name: str (required),
        budget: float (required, >= 0)
    }
    
    RESPONSE:
        201 Created: {status: 'success', category: {category_data}}
        400 Bad Request: {status: 'error', message: 'Missing fields or invalid data'}
        403 Forbidden: {status: 'error', message: 'Cannot create category'}
        409 Conflict: {status: 'error', message: 'Category already exists'}
    """
    try:
        # Check authorization
        if current_user.user_id != user_id:
            return jsonify({'status': 'error', 'message': 'Cannot create category for this user'}), 403
        
        # Parse and validate category payload.
        data = request.get_json()
        
        # Validate required fields
        if not data or not data.get('category_name') or 'budget' not in data:
            return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400
        
        # Check if category already exists for this user
        existing_category = Category.query.filter_by(
            category_name=data['category_name'],
            user_id=user_id
        ).first()
        
        if existing_category:
            return jsonify({'status': 'error', 'message': 'Category already exists for this user'}), 409
        
        # Create new category
        new_category = Category(
            category_name=data['category_name'],
            budget=float(data['budget']),
            user_id=user_id
        )
        
        # Persist the new budget category.
        db.session.add(new_category)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'category': new_category.to_dict()
        }), 201
        
    except ValueError:
        return jsonify({'status': 'error', 'message': 'Invalid budget value'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': 'Server error: ' + str(e)}), 500


@api_bp.route('/users/<int:user_id>/categories', methods=['GET'])
@login_required
def get_user_categories(user_id):
    """
    Get all budget categories for user
    Users can only view their own categories
    
    RESPONSE:
        200 OK: {status: 'success', categories: [{category_data}]}
        403 Forbidden: {status: 'error', message: 'Cannot view categories'}
    """
    try:
        # Check authorization
        if current_user.user_id != user_id:
            return jsonify({'status': 'error', 'message': 'Cannot view these categories'}), 403
        
        categories = Category.query.filter_by(user_id=user_id).all()
        
        return jsonify({
            'status': 'success',
            'categories': [category.to_dict() for category in categories]
        }), 200
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': 'Server error: ' + str(e)}), 500


@api_bp.route('/categories/<int:category_id>', methods=['GET'])
@login_required
def get_category(category_id):
    """
    Get category details with spending information
    
    RESPONSE:
        200 OK: {status: 'success', category: {category_data}}
        404 Not Found: {status: 'error', message: 'Category not found'}
        403 Forbidden: {status: 'error', message: 'Cannot view this category'}
    """
    try:
        category = Category.query.get(category_id)
        if not category:
            return jsonify({'status': 'error', 'message': 'Category not found'}), 404
        
        # Check authorization
        if current_user.user_id != category.user_id:
            return jsonify({'status': 'error', 'message': 'Cannot view this category'}), 403
        
        return jsonify({
            'status': 'success',
            'category': category.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': 'Server error: ' + str(e)}), 500


@api_bp.route('/categories/<int:category_id>', methods=['PUT'])
@login_required
def update_category(category_id):
    """
    Update category budget
    
    REQUEST BODY: {
        category_name: str (optional),
        budget: float (optional, >= 0)
    }
    
    RESPONSE:
        200 OK: {status: 'success', category: {updated_category_data}}
        404 Not Found: {status: 'error', message: 'Category not found'}
        403 Forbidden: {status: 'error', message: 'Cannot update this category'}
    """
    try:
        category = Category.query.get(category_id)
        if not category:
            return jsonify({'status': 'error', 'message': 'Category not found'}), 404
        
        # Check authorization
        if current_user.user_id != category.user_id:
            return jsonify({'status': 'error', 'message': 'Cannot update this category'}), 403
        
        # Apply category name/budget updates.
        data = request.get_json()
        
        # Update allowed fields
        if 'category_name' in data:
            category.category_name = data['category_name']
        if 'budget' in data:
            category.budget = float(data['budget'])
        
        # Persist category updates.
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'category': category.to_dict()
        }), 200
        
    except ValueError:
        return jsonify({'status': 'error', 'message': 'Invalid budget value'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': 'Server error: ' + str(e)}), 500


@api_bp.route('/categories/<int:category_id>', methods=['DELETE'])
@login_required
def delete_category(category_id):
    """
    Delete category (cascades to associated transactions)
    
    RESPONSE:
        200 OK: {status: 'success', message: 'Category deleted'}
        404 Not Found: {status: 'error', message: 'Category not found'}
        403 Forbidden: {status: 'error', message: 'Cannot delete this category'}
    """
    try:
        category = Category.query.get(category_id)
        if not category:
            return jsonify({'status': 'error', 'message': 'Category not found'}), 404
        
        # Check authorization
        if current_user.user_id != category.user_id:
            return jsonify({'status': 'error', 'message': 'Cannot delete this category'}), 403
        
        db.session.delete(category)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Category deleted successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': 'Server error: ' + str(e)}), 500


# ==============================================================================
# TRANSACTION ROUTES
# ==============================================================================

@api_bp.route('/accounts/<int:account_id>/transactions', methods=['POST'])
@login_required
def create_transaction(account_id):
    """
    Create new transaction for account
    Users can only create transactions for their own accounts
    
    REQUEST BODY: {
        date: str (required, YYYY-MM-DD format),
        payee: str (required),
        memo: str (optional),
        outflow: float (optional, >= 0),
        inflow: float (optional, >= 0),
        category_id: int (optional)
    }
    
    RESPONSE:
        201 Created: {status: 'success', transaction: {transaction_data}}
        400 Bad Request: {status: 'error', message: 'Invalid data'}
        404 Not Found: {status: 'error', message: 'Account not found'}
        403 Forbidden: {status: 'error', message: 'Cannot create transaction'}
    """
    try:
        account = Account.query.get(account_id)
        if not account:
            return jsonify({'status': 'error', 'message': 'Account not found'}), 404
        
        # Check authorization
        if current_user.user_id != account.user_id:
            return jsonify({'status': 'error', 'message': 'Cannot create transaction for this account'}), 403
        
        # Parse transaction payload.
        data = request.get_json()
        
        # Validate required fields
        if not data or not data.get('date') or not data.get('payee'):
            return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400
        
        # Parse date
        try:
            transaction_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'status': 'error', 'message': 'Invalid date format (use YYYY-MM-DD)'}), 400
        
        # Create a transaction row linked to the account.
        new_transaction = Transaction(
            date=transaction_date,
            payee=data['payee'],
            memo=data.get('memo', ''),
            outflow=float(data.get('outflow', 0)),
            inflow=float(data.get('inflow', 0)),
            account_id=account_id,
            category_id=data.get('category_id')
        )
        
        # Persist transaction.
        db.session.add(new_transaction)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'transaction': new_transaction.to_dict()
        }), 201
        
    except ValueError as e:
        return jsonify({'status': 'error', 'message': 'Invalid value: ' + str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': 'Server error: ' + str(e)}), 500


@api_bp.route('/accounts/<int:account_id>/transactions', methods=['GET'])
@login_required
def get_account_transactions(account_id):
    """
    Get all transactions for account
    Users can only view transactions for their own accounts
    
    Query parameters:
        start_date: str (optional, YYYY-MM-DD)
        end_date: str (optional, YYYY-MM-DD)
    
    RESPONSE:
        200 OK: {status: 'success', transactions: [{transaction_data}]}
        404 Not Found: {status: 'error', message: 'Account not found'}
        403 Forbidden: {status: 'error', message: 'Cannot view transactions'}
    """
    try:
        account = Account.query.get(account_id)
        if not account:
            return jsonify({'status': 'error', 'message': 'Account not found'}), 404
        
        # Check authorization
        if current_user.user_id != account.user_id:
            return jsonify({'status': 'error', 'message': 'Cannot view these transactions'}), 403
        
        # Optional filtering window for transaction listing.
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        transactions = account.get_transactions(start_date, end_date)
        
        return jsonify({
            'status': 'success',
            'transactions': [transaction.to_dict() for transaction in transactions]
        }), 200
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': 'Server error: ' + str(e)}), 500


@api_bp.route('/transactions/<int:transaction_id>', methods=['GET'])
@login_required
def get_transaction(transaction_id):
    """
    Get transaction details
    
    RESPONSE:
        200 OK: {status: 'success', transaction: {transaction_data}}
        404 Not Found: {status: 'error', message: 'Transaction not found'}
        403 Forbidden: {status: 'error', message: 'Cannot view this transaction'}
    """
    try:
        transaction = Transaction.query.get(transaction_id)
        if not transaction:
            return jsonify({'status': 'error', 'message': 'Transaction not found'}), 404
        
        # Check authorization
        if current_user.user_id != transaction.account.user_id:
            return jsonify({'status': 'error', 'message': 'Cannot view this transaction'}), 403
        
        return jsonify({
            'status': 'success',
            'transaction': transaction.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': 'Server error: ' + str(e)}), 500


@api_bp.route('/transactions/<int:transaction_id>', methods=['PUT'])
@login_required
def update_transaction(transaction_id):
    """
    Update transaction details
    
    REQUEST BODY: {
        date: str (optional, YYYY-MM-DD),
        payee: str (optional),
        memo: str (optional),
        outflow: float (optional),
        inflow: float (optional),
        category_id: int (optional)
    }
    
    RESPONSE:
        200 OK: {status: 'success', transaction: {updated_transaction_data}}
        404 Not Found: {status: 'error', message: 'Transaction not found'}
        403 Forbidden: {status: 'error', message: 'Cannot update this transaction'}
    """
    try:
        transaction = Transaction.query.get(transaction_id)
        if not transaction:
            return jsonify({'status': 'error', 'message': 'Transaction not found'}), 404
        
        # Check authorization
        if current_user.user_id != transaction.account.user_id:
            return jsonify({'status': 'error', 'message': 'Cannot update this transaction'}), 403
        
        # Apply partial transaction updates.
        data = request.get_json()
        
        # Update allowed fields
        if 'date' in data:
            try:
                transaction.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'status': 'error', 'message': 'Invalid date format (use YYYY-MM-DD)'}), 400
        
        if 'payee' in data:
            transaction.payee = data['payee']
        if 'memo' in data:
            transaction.memo = data['memo']
        if 'outflow' in data:
            transaction.outflow = float(data['outflow'])
        if 'inflow' in data:
            transaction.inflow = float(data['inflow'])
        if 'category_id' in data:
            transaction.category_id = data['category_id']
        
        # Persist updated transaction values.
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'transaction': transaction.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': 'Server error: ' + str(e)}), 500


@api_bp.route('/transactions/<int:transaction_id>', methods=['DELETE'])
@login_required
def delete_transaction(transaction_id):
    """
    Delete transaction
    
    RESPONSE:
        200 OK: {status: 'success', message: 'Transaction deleted'}
        404 Not Found: {status: 'error', message: 'Transaction not found'}
        403 Forbidden: {status: 'error', message: 'Cannot delete this transaction'}
    """
    try:
        transaction = Transaction.query.get(transaction_id)
        if not transaction:
            return jsonify({'status': 'error', 'message': 'Transaction not found'}), 404
        
        # Check authorization
        if current_user.user_id != transaction.account.user_id:
            return jsonify({'status': 'error', 'message': 'Cannot delete this transaction'}), 403
        
        db.session.delete(transaction)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Transaction deleted successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': 'Server error: ' + str(e)}), 500
