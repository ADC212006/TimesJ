import mysql.connector
from datetime import datetime

def connect_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='employee_time_tracking'
    )

def add_work_category(employee_id, category):
    conn = connect_db()
    cursor = conn.cursor()
    query = "INSERT INTO work_categories (employee_id, category_name, logged_time) VALUES (%s, %s, %s)"
    logged_time = datetime.now().timestamp()
    cursor.execute(query, (employee_id, category, logged_time))
    conn.commit()
    cursor.close()
    conn.close()

# Example usage
# add_work_category(1, "Patient Care")
