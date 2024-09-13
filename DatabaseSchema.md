Database Schema

1. Tables Overview:

users: Stores user information.
reports: Stores report metadata.
data_sources: Stores information about data sources (e.g., Excel files, APIs).
report_data: Stores the raw data used in generating reports.
report_files: Stores paths to generated report files.
user_reports: A join table that links users to their generated reports.


2. Entity-Relationship Diagram (ERD):
Below is an ERD-style description of the relationships:

users (1) --- (N) user_reports
reports (1) --- (N) user_reports
reports (1) --- (N) report_data
data_sources (1) --- (N) report_data
reports (1) --- (1) report_files