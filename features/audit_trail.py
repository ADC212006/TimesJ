import mysql.connector
from datetime import datetime

def connect_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='employee_time_tracking'
    )

def log_audit_trail(employee_id, action):
    conn = connect_db()
    cursor = conn.cursor()
    query = "INSERT INTO audit_trails (employee_id, action, logged_time) VALUES (%s, %s, %s)"
    logged_time = datetime.now().timestamp()
    cursor.execute(query, (employee_id, action, logged_time))
    conn.commit()
    cursor.close()
    conn.close()

# Example usage
# log_audit_trail(1, "Accessed patient record.")
