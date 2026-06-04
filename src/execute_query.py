import sqlite3

import pandas as pd


def _build_connection():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE employees(
            emp_id INTEGER PRIMARY KEY,
            name TEXT,
            department TEXT,
            salary INTEGER,
            hire_date TEXT
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE departments(
            department TEXT PRIMARY KEY,
            manager TEXT,
            location TEXT
        )
        """
    )
    cursor.executemany(
        "INSERT INTO employees VALUES (?,?,?,?,?)",
        [
            (1, "Rahul", "IT", 60000, "2023-01-15"),
            (2, "Priya", "HR", 50000, "2022-08-01"),
            (3, "Arjun", "Finance", 70000, "2021-05-10"),
            (4, "Sneha", "IT", 80000, "2024-02-20"),
            (5, "Kiran", "Marketing", 45000, "2023-11-05"),
        ],
    )
    cursor.executemany(
        "INSERT INTO departments VALUES (?,?,?)",
        [
            ("IT", "Meera", "Bangalore"),
            ("HR", "Anita", "Mumbai"),
            ("Finance", "Ravi", "Delhi"),
            ("Marketing", "Sana", "Pune"),
        ],
    )
    conn.commit()
    return conn


def run_query(sql):

    conn = _build_connection()

    result = pd.read_sql_query(sql, conn)

    conn.close()

    return result
