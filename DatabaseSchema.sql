-- Create database
CREATE DATABASE IF NOT EXISTS report_generator_db;
USE report_generator_db;

-- Table: users
-- Purpose: Stores user details, including authentication information.
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,            -- Primary Key: Unique identifier for each user.
    username VARCHAR(50) NOT NULL UNIQUE,         -- Username: Unique username for each user.
    email VARCHAR(100) NOT NULL UNIQUE,           -- Email: User’s email address, must be unique.
    password_hash VARCHAR(255) NOT NULL,          -- Password Hash: Encrypted password for secure authentication.
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Created At: Timestamp when the user was created.
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP -- Updated At: Timestamp when the user was last updated.
);

-- Index on email for faster lookups
CREATE INDEX idx_users_email ON users (email);

-- Table: reports
-- Purpose: Stores metadata about generated reports.
CREATE TABLE reports (
    id INT AUTO_INCREMENT PRIMARY KEY,            -- Primary Key: Unique identifier for each report.
    title VARCHAR(100) NOT NULL,                  -- Title: Title of the report.
    description TEXT,                             -- Description: Short description of the report.
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Created At: Timestamp when the report was generated.
    user_id INT,                                  -- User ID: Foreign Key linking to the user who generated the report.
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL -- Foreign Key constraint with ON DELETE SET NULL to retain reports even if the user is deleted.
);

-- Index on user_id for faster lookups
CREATE INDEX idx_reports_user_id ON reports (user_id);

-- Table: data_sources
-- Purpose: Stores information about the data sources used to generate reports.
CREATE TABLE data_sources (
    id INT AUTO_INCREMENT PRIMARY KEY,            -- Primary Key: Unique identifier for each data source.
    source_name VARCHAR(100) NOT NULL,            -- Source Name: Name of the data source (e.g., "Sales Data").
    source_type VARCHAR(50) NOT NULL,             -- Source Type: Type of the data source (e.g., "Excel", "API").
    connection_details JSON,                      -- Connection Details: JSON storing connection info (e.g., file path, API endpoint).
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Created At: Timestamp when the data source was added.
);

-- Table: report_data
-- Purpose: Stores data used in generating the report.
CREATE TABLE report_data (
    id INT AUTO_INCREMENT PRIMARY KEY,            -- Primary Key: Unique identifier for each report data entry.
    report_id INT,                                -- Report ID: Foreign Key linking to the report this data is associated with.
    data_source_id INT,                           -- Data Source ID: Foreign Key linking to the data source from which the data was pulled.
    data JSON,                                    -- Data: JSON storing the processed data.
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Created At: Timestamp when the data was added.
    FOREIGN KEY (report_id) REFERENCES reports(id) ON DELETE CASCADE, -- Foreign Key constraint with ON DELETE CASCADE to remove data if the report is deleted.
    FOREIGN KEY (data_source_id) REFERENCES data_sources(id) ON DELETE CASCADE -- Foreign Key constraint with ON DELETE CASCADE to remove data if the data source is deleted.
);

-- Index on report_id for faster lookups
CREATE INDEX idx_report_data_report_id ON report_data (report_id);

-- Table: report_files
-- Purpose: Stores file paths to the generated reports.
CREATE TABLE report_files (
    id INT AUTO_INCREMENT PRIMARY KEY,            -- Primary Key: Unique identifier for each report file.
    report_id INT,                                -- Report ID: Foreign Key linking to the report this file belongs to.
    file_path VARCHAR(255) NOT NULL,              -- File Path: Path to the generated report file (e.g., PDF, Excel).
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Created At: Timestamp when the file was generated.
    FOREIGN KEY (report_id) REFERENCES reports(id) ON DELETE CASCADE -- Foreign Key constraint with ON DELETE CASCADE to remove files if the report is deleted.
);

-- Index on report_id for faster lookups
CREATE INDEX idx_report_files_report_id ON report_files (report_id);

-- Table: user_reports
-- Purpose: Manages the many-to-many relationship between users and reports.
CREATE TABLE user_reports (
    id INT AUTO_INCREMENT PRIMARY KEY,            -- Primary Key: Unique identifier for each record.
    user_id INT,                                  -- User ID: Foreign Key linking to the user.
    report_id INT,                                -- Report ID: Foreign Key linking to the report.
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE, -- Foreign Key constraint with ON DELETE CASCADE to remove records if the user is deleted.
    FOREIGN KEY (report_id) REFERENCES reports(id) ON DELETE CASCADE -- Foreign Key constraint with ON DELETE CASCADE to remove records if the report is deleted.
);

-- Index on user_id and report_id for faster lookups
CREATE INDEX idx_user_reports_user_id ON user_reports (user_id);
CREATE INDEX idx_user_reports_report_id ON user_reports (report_id);
