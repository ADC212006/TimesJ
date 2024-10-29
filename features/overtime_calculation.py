import mysql.connector
from datetime import datetime

def connect_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='employee_time_tracking'
    )

def log_overtime(employee_id, hours):
    conn = connect_db()
    cursor = conn.cursor()
    query = "INSERT INTO overtime_logs (employee_id, hours, logged_time) VALUES (%s, %s, %s)"
    logged_time = datetime.now().timestamp()
    cursor.execute(query, (employee_id, hours, logged_time))
    conn.commit()
    cursor.close()
    conn.close()

# Example usage
# log_overtime(1, 2)
