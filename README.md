# 🎓 Student Performance Prediction & Management System

> **A command-line AI/ML project for managing student records, analyzing academic data, and predicting student performance.**

---

## 📌 Overview

The **Student Performance Prediction & Management System** is a command-line based application developed using **Python, MySQL, Pandas, and Scikit-learn**.

The project combines **student record management, data preprocessing, machine learning, prediction, and model analysis** into a single system.

Instead of maintaining student information separately and manually analyzing academic performance, the system provides a centralized workflow where users can:

* Manage student records
* Search and update student information
* Clean and validate academic data
* Train a machine learning model
* Predict student performance
* Evaluate model accuracy
* Analyze important prediction features

The application is designed to run completely through the **command line**, making it simple to execute and test in a terminal environment.

---

## ✨ Key Features

### 👨‍🎓 Student Management

The system provides complete CRUD operations for student records.

* ➕ Add a student
* 👁️ View all students
* 🔎 Search for a student
* ✏️ Edit student information
* 🗑️ Delete student records

### 🧹 Data Processing

Before machine learning is performed, the system can process the academic data.

* Detect invalid values
* Handle missing data
* Validate student information
* Prepare data for model training

### 🤖 Machine Learning

The system uses machine learning to analyze student academic data.

* Train the prediction model
* Use selected academic features
* Generate performance predictions
* Reuse the trained model for predictions

### 📊 Model Evaluation

The system provides basic model analysis.

* Calculate prediction accuracy
* Display model performance
* Identify important input features
* Help understand which academic factors influence predictions

### 💾 MySQL Database

Student records are stored in a **MySQL database**, providing persistent storage for the application.

The database is used for:

* Storing student records
* Retrieving student information
* Updating records
* Deleting records
* Providing data for machine learning

---

# 🖥️ Application Menu

The application provides a simple interactive command-line menu:

```text
==================================================
       STUDENT PERFORMANCE PREDICTION SYSTEM
==================================================

1. View all students
2. Search student
3. Add student
4. Edit student
5. Delete student
6. Clean data
7. Train model
8. Predict result
9. View accuracy
10. View feature importance
11. Exit

==================================================
Enter your choice:
```

The menu allows the evaluator to test each major functionality independently.

---

# 🏗️ System Architecture

```text
                     ┌───────────────────┐
                     │       USER        │
                     └─────────┬─────────┘
                               │
                               ▼
                     ┌───────────────────┐
                     │     main.py       │
                     │   CLI Interface   │
                     └─────────┬─────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
      ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
      │   Student    │ │     Data     │ │  Machine     │
      │  Management  │ │  Processing  │ │   Learning   │
      └──────┬───────┘ └──────┬───────┘ └──────┬───────┘
             │                │                │
             ▼                ▼                ▼
      ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
      │    MySQL     │ │    Pandas    │ │ Scikit-learn │
      │   Database   │ │              │ │     Model    │
      └──────────────┘ └──────────────┘ └──────┬───────┘
                                               │
                                               ▼
                                      ┌─────────────────┐
                                      │ Prediction &    │
                                      │ Model Analysis  │
                                      └─────────────────┘
```

---

# 🔄 Project Workflow

```text
START
  │
  ▼
Connect to MySQL
  │
  ▼
Display Main Menu
  │
  ├──► Manage Student Records
  │
  ├──► Clean Academic Data
  │
  ├──► Train ML Model
  │
  ├──► Predict Student Result
  │
  ├──► View Model Accuracy
  │
  └──► View Feature Importance
  │
  ▼
Exit
```

---

# 🧰 Technologies Used

| Technology      | Purpose                             |
| --------------- | ----------------------------------- |
| 🐍 Python       | Core application development        |
| 🗄️ MySQL       | Student data storage                |
| 🐼 Pandas       | Data processing and manipulation    |
| 🔢 NumPy        | Numerical operations                |
| 🤖 Scikit-learn | Machine learning                    |
| 💻 Command Line | User interaction                    |
| 🔧 Git & GitHub | Version control and project hosting |

---

# 📂 Project Structure

```text
student-performance-prediction/
│
├── main.py
├── requirements.txt
├── README.md
├── statement.md
└── .gitignore
```

### Main Components

**`main.py`**

Contains the complete application logic, including:

* MySQL connection
* Student management
* Data processing
* Machine learning
* Prediction
* Model evaluation
* Feature analysis
* Command-line menu

**`requirements.txt`**

Contains the Python dependencies required to run the project.

**`statement.md`**

Contains the project's problem statement, scope, target users, and high-level features.

---

# ⚙️ Requiremen
