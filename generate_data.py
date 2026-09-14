

import numpy as np
import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "student_performance_db",
}

np.random.seed(42)
N = 300  # number of students

# --- Core features -----------------------------------------------------
study_hours = np.round(np.random.normal(5, 2, N), 1)          # hrs/day
study_hours = np.clip(study_hours, 0, 12)

attendance = np.round(np.random.normal(80, 12, N), 1)         # %
attendance = np.clip(attendance, 30, 100)

previous_score = np.round(np.random.normal(65, 15, N), 1)     # marks out of 100
previous_score = np.clip(previous_score, 0, 100)

sleep_hours = np.round(np.random.normal(6.5, 1.2, N), 1)      # hrs/day
sleep_hours = np.clip(sleep_hours, 3, 10)

extracurricular = np.random.choice([0, 1], size=N, p=[0.55, 0.45])  # 0=No, 1=Yes

# --- Target: final result, driven by a weighted mix of the features ----
raw_score = (
    0.35 * study_hours
    + 0.05 * attendance
    + 0.04 * previous_score
    + 0.15 * sleep_hours
    - 0.5 * extracurricular
    + np.random.normal(0, 2, N)  # noise
)
threshold = np.percentile(raw_score, 40)  # bottom 40% -> Fail
result = np.where(raw_score >= threshold, "Pass", "Fail")

# --- Inject realistic messiness for the cleaning step -------------------
# Convert to Python lists (of possibly-NaN floats) so we can turn NaN -> None
attendance = attendance.astype(object)
previous_score = previous_score.astype(object)
study_hours = study_hours.astype(object)

missing_idx = np.random.choice(N, size=12, replace=False)
for i in missing_idx:
    attendance[i] = None  # missing value -> SQL NULL

missing_idx2 = np.random.choice(N, size=8, replace=False)
for i in missing_idx2:
    previous_score[i] = None

typo_idx = np.random.choice(N, size=5, replace=False)
for i in typo_idx:
    study_hours[i] = -1.0  # impossible negative value = data entry error

# --- Insert into MySQL ---------------------------------------------------
conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

# Clear old rows so re-running this script doesn't duplicate data
cursor.execute("TRUNCATE TABLE raw_students")

insert_query = """
INSERT INTO raw_students
    (study_hours_per_day, attendance_percent, previous_score,
     sleep_hours, extracurricular, result)
VALUES (%s, %s, %s, %s, %s, %s)
"""

rows = [
    (
        study_hours[i],
        attendance[i],
        previous_score[i],
        float(sleep_hours[i]),
        int(extracurricular[i]),
        str(result[i]),
    )
    for i in range(N)
]

cursor.executemany(insert_query, rows)
conn.commit()
print(f"Inserted {cursor.rowcount} rows into MySQL table 'raw_students'.")

cursor.close()
conn.close()
