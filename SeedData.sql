-- Insert dummy users
INSERT INTO users (username, email, password_hash, created_at, updated_at)
VALUES
    ('john_doe', 'john.doe@example.com', 'hashed_password1', NOW(), NOW()),
    ('jane_smith', 'jane.smith@example.com', 'hashed_password2', NOW(), NOW()),
    ('alice_johnson', 'alice.johnson@example.com', 'hashed_password3', NOW(), NOW());

-- Insert dummy data sources
INSERT INTO data_sources (source_name, source_type, connection_details, created_at)
VALUES
    ('Sales Data', 'API', '{"endpoint": "https://api.example.com/sales"}', NOW()),
    ('Customer Data', 'Excel', '{"file_path": "/path/to/customers.xlsx"}', NOW()),
    ('Product Data', 'Database', '{"connection_string": "dbname=products user=admin password=secret"}', NOW());

-- Insert dummy reports
INSERT INTO reports (title, description, created_at, user_id)
VALUES
    ('Sales Report Q1', 'Quarterly sales report for Q1', NOW(), 1),
    ('Customer Insights', 'Insights into customer demographics', NOW(), 2),
    ('Product Performance', 'Performance metrics for products', NOW(), 3);

-- Insert dummy report data
INSERT INTO report_data (report_id, data_source_id, data, created_at)
VALUES
    (1, 1, '{"total_sales": 10000, "new_customers": 150}', NOW()),
    (2, 2, '{"customer_count": 200, "average_age": 35}', NOW()),
    (3, 3, '{"top_selling_product": "Widget A", "sales_volume": 500}', NOW());

-- Insert dummy report files
INSERT INTO report_files (report_id, file_path, created_at)
VALUES
    (1, '/reports/sales_q1.pdf', NOW()),
    (2, '/reports/customer_insights.xlsx', NOW()),
    (3, '/reports/product_performance.csv', NOW());

-- Insert dummy user-reports mappings
INSERT INTO user_reports (user_id, report_id)
VALUES
    (1, 1),
    (2, 2),
    (3, 3);

-- Verify inserted data
SELECT * FROM users;
SELECT * FROM data_sources;
SELECT * FROM reports;
SELECT * FROM report_data;
SELECT * FROM report_files;
SELECT * FROM user_reports;
