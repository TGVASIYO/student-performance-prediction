"""
mysql_setup.py
----------------
Creates the MySQL database and both tables used by this project.
Run this ONCE before generate_data.py.

    raw_students     -> the messy, freshly generated data (before cleaning)
    students          -> cleaned data + model predictions (final output)

Edit DB_CONFIG below with your own MySQL username/password before running.
"""

import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",
}

DB_NAME = "student_performance_db"

conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
print(f"Database '{DB_NAME}' ready.")
cursor.execute(f"USE {DB_NAME}")

# Raw table: allows NULLs, since we deliberately generate missing/bad values
# here for the cleaning step to fix later.
cursor.execute("""
CREATE TABLE IF NOT EXISTS raw_students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    study_hours_per_day FLOAT,
    attendance_percent FLOAT,
    previous_score FLOAT,
    sleep_hours FLOAT,
    extracurricular TINYINT,
    result VARCHAR(10)
)
""")
print("Table 'raw_students' ready.")

# Results table: cleaned data + what the model predicted for each row.
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    study_hours_per_day FLOAT,
    attendance_percent FLOAT,
    previous_score FLOAT,
    sleep_hours FLOAT,
    extracurricular TINYINT,
    actual_result VARCHAR(10),
    predicted_result VARCHAR(10),
    model_used VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
print("Table 'students' ready.")

conn.commit()
cursor.close()
conn.close()
print("MySQL setup complete.")
