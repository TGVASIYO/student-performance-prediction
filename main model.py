import mysql.connector
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report


# ================= DATABASE =================

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "student_performance_db"
}

logistic_model = None
tree_model = None
scaler = None
logistic_accuracy = None
tree_accuracy = None
cleaned_data = None


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


# ================= VIEW STUDENTS =================

def view_all_students():
    conn = get_connection()
    query = "SELECT * FROM raw_students"

    df = pd.read_sql(query, conn)
    conn.close()

    if df.empty:
        print("\nNo students found.")
    else:
        print("\n========== ALL STUDENTS ==========")
        print(df.to_string(index=False))
        
# ================= SEARCH =================

def search_student():
    choice = input(
        "\nSearch by:\n"
        "1. Student ID\n"
        "2. Result\n"
        "Enter choice: "
    )

    conn = get_connection()

    if choice == "1":
        sid = input("Enter student ID: ")
        query = "SELECT * FROM raw_students WHERE id = %s"
        df = pd.read_sql(query, conn, params=(sid,))

    elif choice == "2":
        result = input("Enter Pass or Fail: ").capitalize()
        query = "SELECT * FROM raw_students WHERE result = %s"
        df = pd.read_sql(query, conn, params=(result,))

    else:
        print("Invalid choice.")
        conn.close()
        return

    conn.close()

    if df.empty:
        print("\nNo matching student found.")
    else:
        print("\n========== SEARCH RESULT ==========")
        print(df.to_string(index=False))


# ================= ADD STUDENT =================

def add_student():
    try:
        study = float(input("Study hours per day: "))
        attendance = float(input("Attendance percentage: "))
        score = float(input("Previous score: "))
        sleep = float(input("Sleep hours: "))
        extra = int(input("Extracurricular (0 = No, 1 = Yes): "))
        result = input("Actual result (Pass/Fail): ").capitalize()

        if result not in ["Pass", "Fail"]:
            print("Result must be Pass or Fail.")
            return

        conn = get_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO raw_students
        (study_hours_per_day, attendance_percent, previous_score,
         sleep_hours, extracurricular, result)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        values = (study, attendance, score, sleep, extra, result)

        cursor.execute(query, values)
        conn.commit()

        cursor.close()
        conn.close()

        print("\nStudent added successfully.")

    except ValueError:
        print("Please enter valid numerical values.")


# ================= EDIT STUDENT =================

def edit_student():
    try:
        sid = int(input("Enter student ID to edit: "))

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM raw_students WHERE id = %s",
            (sid,)
        )

        student = cursor.fetchone()

        if not student:
            print("Student not found.")
            cursor.close()
            conn.close()
            return

        study = float(input("New study hours: "))
        attendance = float(input("New attendance: "))
        score = float(input("New previous score: "))
        sleep = float(input("New sleep hours: "))
        extra = int(input("New extracurricular (0/1): "))
        result = input("New result (Pass/Fail): ").capitalize()

        if result not in ["Pass", "Fail"]:
            print("Invalid result.")
            cursor.close()
            conn.close()
            return

        query = """
        UPDATE raw_students
        SET study_hours_per_day = %s,
            attendance_percent = %s,
            previous_score = %s,
            sleep_hours = %s,
            extracurricular = %s,
            result = %s
        WHERE id = %s
        """

        cursor.execute(
            query,
            (study, attendance, score, sleep, extra, result, sid)
        )

        conn.commit()

        cursor.close()
        conn.close()

        print("\nStudent updated successfully.")

    except ValueError:
        print("Invalid input.")


# ================= DELETE STUDENT =================

def delete_student():
    try:
        sid = int(input("Enter student ID to delete: "))

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id FROM raw_students WHERE id = %s",
            (sid,)
        )

        if not cursor.fetchone():
            print("Student not found.")
            cursor.close()
            conn.close()
            return

        confirm = input("Are you sure? (y/n): ").lower()

        if confirm == "y":
            cursor.execute(
                "DELETE FROM raw_students WHERE id = %s",
                (sid,)
            )
            conn.commit()
            print("Student deleted successfully.")
        else:
            print("Delete cancelled.")

        cursor.close()
        conn.close()

    except ValueError:
        print("Invalid ID.")


# ================= CLEAN DATA =================

def clean_data():
    global cleaned_data

    conn = get_connection()

    df = pd.read_sql(
        "SELECT * FROM raw_students",
        conn
    )

    conn.close()

    if df.empty:
        print("No data available.")
        return

    print("\n========== DATA BEFORE CLEANING ==========")
    print("Rows:", len(df))
    print("Missing values:")
    print(df.isnull().sum())

    numeric_cols = [
        "study_hours_per_day",
        "attendance_percent",
        "previous_score",
        "sleep_hours",
        "extracurricular"
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Remove impossible values
    df.loc[
        df["study_hours_per_day"] < 0,
        "study_hours_per_day"
    ] = np.nan

    df.loc[
        (df["attendance_percent"] < 0) |
        (df["attendance_percent"] > 100),
        "attendance_percent"
    ] = np.nan

    df.loc[
        (df["previous_score"] < 0) |
        (df["previous_score"] > 100),
        "previous_score"
    ] = np.nan

    # Fill missing values with median
    for col in numeric_cols:
        df[col] = df[col].fillna(df[col].median())

    df["result"] = df["result"].str.capitalize()

    cleaned_data = df

    print("\n========== DATA AFTER CLEANING ==========")
    print("Missing values:")
    print(df.isnull().sum())

    print("\nData cleaning completed.")


# ================= TRAIN MODEL =================

def train_model():
    global logistic_model
    global tree_model
    global scaler
    global logistic_accuracy
    global tree_accuracy
    global cleaned_data

    if cleaned_data is None:
        clean_data()

    if cleaned_data is None or cleaned_data.empty:
        print("No data available for training.")
        return

    features = [
        "study_hours_per_day",
        "attendance_percent",
        "previous_score",
        "sleep_hours",
        "extracurricular"
    ]

    X = cleaned_data[features]
    y = cleaned_data["result"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )

    # ---------- Logistic Regression ----------

    scaler = StandardScaler()

    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    logistic_model = LogisticRegression()
    logistic_model.fit(X_train_scaled, y_train)

    logistic_pred = logistic_model.predict(X_test_scaled)

    logistic_accuracy = accuracy_score(
        y_test,
        logistic_pred
    )

    # ---------- Decision Tree ----------

    tree_model = DecisionTreeClassifier(
        random_state=42,
        max_depth=5
    )

    tree_model.fit(X_train, y_train)

    tree_pred = tree_model.predict(X_test)

    tree_accuracy = accuracy_score(
        y_test,
        tree_pred
    )

    print("\n========== MODEL TRAINING ==========")

    print(
        f"Logistic Regression Accuracy: "
        f"{logistic_accuracy * 100:.2f}%"
    )

    print(
        f"Decision Tree Accuracy: "
        f"{tree_accuracy * 100:.2f}%"
    )

    if logistic_accuracy >= tree_accuracy:
        print("\nBest Model: Logistic Regression")
    else:
        print("\nBest Model: Decision Tree")


# ================= PREDICT =================

def predict_result():
    if logistic_model is None:
        print("\nPlease train the model first.")
        return

    try:
        study = float(input("\nStudy hours per day: "))
        attendance = float(input("Attendance percentage: "))
        score = float(input("Previous score: "))
        sleep = float(input("Sleep hours: "))
        extra = int(input("Extracurricular (0/1): "))

        data = np.array([
            [study, attendance, score, sleep, extra]
        ])

        scaled_data = scaler.transform(data)

        prediction = logistic_model.predict(
            scaled_data
        )[0]

        probability = logistic_model.predict_proba(
            scaled_data
        )[0]

        classes = logistic_model.classes_

        print("\n========== PREDICTION ==========")
        print("Predicted Result:", prediction)

        for cls, prob in zip(classes, probability):
            print(
                f"{cls} probability: "
                f"{prob * 100:.2f}%"
            )

    except ValueError:
        print("Please enter valid values.")


# ================= ACCURACY =================

def view_accuracy():
    if logistic_accuracy is None:
        print("\nPlease train the models first.")
        return

    print("\n========== MODEL ACCURACY ==========")

    print(
        f"Logistic Regression: "
        f"{logistic_accuracy * 100:.2f}%"
    )

    print(
        f"Decision Tree: "
        f"{tree_accuracy * 100:.2f}%"
    )

    if logistic_accuracy >= tree_accuracy:
        print("\nBest Model: Logistic Regression")
    else:
        print("\nBest Model: Decision Tree")


# ================= FEATURE IMPORTANCE =================

def view_feature_importance():
    if tree_model is None:
        print("\nPlease train the model first.")
        return

    features = [
        "study_hours_per_day",
        "attendance_percent",
        "previous_score",
        "sleep_hours",
        "extracurricular"
    ]

    importance = tree_model.feature_importances_

    result = pd.DataFrame({
        "Feature": features,
        "Importance": importance
    })

    result = result.sort_values(
        by="Importance",
        ascending=False
    )

    print("\n========== FEATURE IMPORTANCE ==========")
    print(result.to_string(index=False))

    plt.figure(figsize=(8, 5))
    plt.bar(
        result["Feature"],
        result["Importance"]
    )

    plt.xticks(rotation=30)
    plt.ylabel("Importance")
    plt.title("Decision Tree Feature Importance")
    plt.tight_layout()
    plt.show()


# ================= MAIN MENU =================

def main():

    while True:

        print("\n")
        print("==========================================")
        print("   STUDENT PERFORMANCE PREDICTION SYSTEM")
        print("==========================================")
        print("1. View all students")
        print("2. Search student")
        print("3. Add student")
        print("4. Edit student")
        print("5. Delete student")
        print("6. Clean data")
        print("7. Train model")
        print("8. Predict result")
        print("9. View accuracy")
        print("10. View feature importance")
        print("11. Exit")
        print("==========================================")

        choice = input("Enter your choice: ")

        if choice == "1":
            view_all_students()

        elif choice == "2":
            search_student()

        elif choice == "3":
            add_student()

        elif choice == "4":
            edit_student()

        elif choice == "5":
            delete_student()

        elif choice == "6":
            clean_data()

        elif choice == "7":
            train_model()

        elif choice == "8":
            predict_result()

        elif choice == "9":
            view_accuracy()

        elif choice == "10":
            view_feature_importance()

        elif choice == "11":
            print("\nThank you for using the system.")
            break

        else:
            print("\nInvalid choice. Please try again.")


if __name__ == "__main__":
    main()