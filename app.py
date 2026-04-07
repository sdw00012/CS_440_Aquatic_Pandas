"""
==============================================================================
AQUATIC PANDAS - Main Application Entry Point
CS440 Project - Budget Management System
==============================================================================

This file initializes the Flask application, configures the database,
and registers all routes.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize SQLAlchemy ORM
db = SQLAlchemy()

def create_app():
    """
    Application Factory Pattern - Creates and configures Flask app
    
    PSEUDOCODE:
        FUNCTION create_app():
            app = Flask(__name__)
            
            // Configure database connection
            app.config['SQLALCHEMY_DATABASE_URI'] = (
                f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
            )
            app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
            
            // Initialize database with app
            db.init_app(app)
            
            // Register database models
            IMPORT User, Account, Institution, Category, Transaction models
            
            // Register API blueprints/routes
            IMPORT create_user_routes, create_account_routes, etc.
            REGISTER all routes with app
            
            // Setup error handlers
            REGISTER error handler for 404
            REGISTER error handler for 500
            REGISTER error handler for 400
            
            // Create database tables if they don't exist
            WITH app.app_context():
                db.create_all()
            
            RETURN app
    """
    pass


if __name__ == '__main__':
    """
    PSEUDOCODE - Main Entry Point:
        app = create_app()
        
        HOST = 'localhost' or os.getenv('FLASK_HOST', '0.0.0.0')
        PORT = 3000 or os.getenv('FLASK_PORT', 3000)
        DEBUG = os.getenv('FLASK_ENV') == 'development'
        
        PRINT "Starting Aquatic Pandas application..."
        PRINT f"Server running at http://{HOST}:{PORT}"
        
        app.run(host=HOST, port=PORT, debug=DEBUG)
    """
    pass
