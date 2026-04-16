"""
==============================================================================
AQUATIC PANDAS - Main Application Entry Point
CS440 Project - Budget Management System
==============================================================================

This file initializes the Flask application, configures the database,
and registers all routes.
"""

from flask import Flask
from dotenv import load_dotenv
import os
from extensions import db, login_manager

# Load environment variables
# Reads values from a local .env file when present.
load_dotenv()

def create_app():
    """Create and configure the Flask application instance."""
    # Create the Flask app object.
    app = Flask(__name__)
    
    # Pull database settings from environment, with safe local defaults.
    db_user = os.getenv('DB_USER', 'root')
    db_password = os.getenv('DB_PASSWORD', '')
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '3306')
    db_name = os.getenv('DB_NAME', 'aquatic_pandas')
    
    # Configure SQLAlchemy and session security settings.
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['SESSION_COOKIE_SECURE'] = os.getenv('FLASK_ENV', 'development') == 'production'
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    
    # Bind extension instances to this app.
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    # Use app context for model registration and database/table operations.
    with app.app_context():
        # Import models here to avoid circular import issues.
        from models import User, Account, Institution, Category, Transaction
        
        # Create any missing tables from the ORM models.
        db.create_all()
        
        # Tell Flask-Login how to convert stored user_id -> User object.
        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))
        
        # Register auth and API route groups.
        from routes import auth_bp, api_bp
        app.register_blueprint(auth_bp)
        app.register_blueprint(api_bp)
        
        # Return JSON error payloads for common HTTP failures.
        @app.errorhandler(404)
        def not_found(error):
            return {'error': 'Resource not found'}, 404
        
        @app.errorhandler(500)
        def internal_error(error):
            db.session.rollback()
            return {'error': 'Internal server error'}, 500
        
        @app.errorhandler(400)
        def bad_request(error):
            return {'error': 'Bad request'}, 400
    
    return app


if __name__ == '__main__':
    # Build a configured app instance.
    app = create_app()
    
    # Host/port are configurable so local and Docker runs share the same entrypoint.
    HOST = os.getenv('FLASK_HOST', '0.0.0.0')
    PORT = int(os.getenv('FLASK_PORT', 3000))
    DEBUG = os.getenv('FLASK_ENV', 'development') == 'development'
    
    print("Starting Aquatic Pandas application...")
    print(f"Server running at http://{HOST}:{PORT}")
    
    # Start the development server.
    app.run(host=HOST, port=PORT, debug=DEBUG)
