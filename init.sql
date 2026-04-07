-- ==============================================================================
-- AQUATIC PANDAS - Database Schema Initialization
-- CS440 Project - Database Design
-- ==============================================================================

-- Drop existing tables if they exist (for clean development)
DROP TABLE IF EXISTS Transaction;
DROP TABLE IF EXISTS Category;
DROP TABLE IF EXISTS Account;
DROP TABLE IF EXISTS Institution;
DROP TABLE IF EXISTS User;

-- ==============================================================================
-- USER TABLE
-- ==============================================================================
-- Purpose: Stores user account information
-- Primary Key: user_id (auto-incremented)
-- Constraints: email must be unique
CREATE TABLE User (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    address VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ==============================================================================
-- INSTITUTION TABLE
-- ==============================================================================
-- Purpose: Stores banking/financial institution information
-- Primary Key: institution_id (auto-incremented)
-- Constraints: institution_name must be unique
CREATE TABLE Institution (
    institution_id INT AUTO_INCREMENT PRIMARY KEY,
    institution_name VARCHAR(255) UNIQUE NOT NULL,
    website VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ==============================================================================
-- ACCOUNT TABLE
-- ==============================================================================
-- Purpose: Stores user's accounts at various institutions
-- Primary Key: account_id (auto-incremented)
-- Foreign Keys: user_id (references User), institution_id (references Institution)
CREATE TABLE Account (
    account_id INT AUTO_INCREMENT PRIMARY KEY,
    account_name VARCHAR(255) NOT NULL,
    account_type VARCHAR(50) NOT NULL,
    user_id INT NOT NULL,
    institution_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE,
    FOREIGN KEY (institution_id) REFERENCES Institution(institution_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ==============================================================================
-- CATEGORY TABLE
-- ==============================================================================
-- Purpose: Stores budget categories for a user
-- Primary Key: category_id (auto-incremented)
-- Foreign Key: user_id (references User)
-- Constraints: category_name and user_id must be unique together
CREATE TABLE Category (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(255) NOT NULL,
    budget DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    user_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE,
    UNIQUE KEY unique_category_per_user (category_name, user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ==============================================================================
-- TRANSACTION TABLE
-- ==============================================================================
-- Purpose: Records financial transactions (income/expenses)
-- Primary Key: transaction_id (auto-incremented)
-- Foreign Keys: category_id (references Category), account_id (references Account)
-- Note: outflow = money leaving the account (expense)
--       inflow = money entering the account (income)
CREATE TABLE Transaction (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    memo VARCHAR(255),
    date DATE NOT NULL,
    outflow DECIMAL(10, 2) DEFAULT 0.00,
    payee VARCHAR(255),
    category_id INT,
    account_id INT NOT NULL,
    inflow DECIMAL(10, 2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES Category(category_id) ON DELETE SET NULL,
    FOREIGN KEY (account_id) REFERENCES Account(account_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ==============================================================================
-- INDEXES
-- ==============================================================================
-- Performance optimization indexes
CREATE INDEX idx_account_user_id ON Account(user_id);
CREATE INDEX idx_account_institution_id ON Account(institution_id);
CREATE INDEX idx_category_user_id ON Category(user_id);
CREATE INDEX idx_transaction_account_id ON Transaction(account_id);
CREATE INDEX idx_transaction_category_id ON Transaction(category_id);
CREATE INDEX idx_transaction_date ON Transaction(date);
