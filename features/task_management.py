import mysql.connector
from datetime import datetime

def connect_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='employee_time_tracking'
    )

def log_task(employee_id, task_description):
    conn = connect_db()
    cursor = conn.cursor()
    query = "INSERT INTO task_logs (employee_id, task_description, logged_time) VALUES (%s, %s, %s)"
    logged_time = datetime.now().timestamp()
    cursor.execute(query, (employee_id, task_description, logged_time))
    conn.commit()
    cursor.close()
    conn.close()

# Example usage
# log_task(1, "Completed report analysis.")
