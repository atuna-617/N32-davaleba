import sqlite3

conn = sqlite3.connect('company_database.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS departments (
        department_id INTEGER PRIMARY KEY AUTOINCREMENT,
        department_name TEXT
    )
''')

data_departments = [
    ('HR'),
    ('IT managment'),
    ('Finance')
]

cursor.executemany('INSERT INTO departments (department_name) VALUES (?)', data_departments)

cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_name TEXT,
        department_id INTEGER,
        FOREIGN KEY (department_id) REFERENCES departments(department_id)
    )
''')

data_employees = [
    ('Avtandil Javrishvili', 1),
    ('Nini Jabanashvili', 2),
    ('Giorgi Pataridze', 3),
    ('Elza ositashvili', 1),
    ('Nika Cicqishvili', 2)
]

cursor.executemany('INSERT INTO employees (employee_name, department_id) VALUES (?, ?)', data_employees)

cursor.execute('''
    CREATE TABLE IF NOT EXISTS salaries (
        salary_id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL,
        employee_id INTEGER,
        FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
    )
''')

data_salaries = [
    (50000.0, 1),
    (60000.0, 2),
    (55000.0, 3),
    (70000.0, 4),
    (65000.0, 5)
]

cursor.executemany('INSERT INTO salaries (amount, employee_id) VALUES (?, ?)', data_salaries)

cursor.execute('''
    SELECT department_name, AVG(amount) as avg_salary
    FROM departments
    LEFT JOIN employees ON departments.department_id = employees.department_id
    LEFT JOIN salaries ON employees.employee_id = salaries.employee_id
    GROUP BY department_name
''')
avg_salaries = cursor.fetchall()
print("Average Salaries by Department:")
for row in avg_salaries:
    print(f"{row[0]}: {row[1]}")

cursor.execute('''
    SELECT employee_name, amount
    FROM employees
    LEFT JOIN salaries ON employees.employee_id = salaries.employee_id
''')
left_join_result = cursor.fetchall()

cursor.execute('''
    SELECT employee_name, amount
    FROM employees
    RIGHT JOIN salaries ON employees.employee_id = salaries.employee_id
''')
right_join_result = cursor.fetchall()

conn.commit()
conn.close()
