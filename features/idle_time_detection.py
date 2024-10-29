import mysql.connector
from datetime import datetime

def connect_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='employee_time_tracking'
    )

def log_idle_time(employee_id, idle_duration):
    conn = connect_db()
    cursor = conn.cursor()
    query = "INSERT INTO idle_time_logs (employee_id, idle_duration, logged_time) VALUES (%s, %s, %s)"
    logged_time = datetime.now().timestamp()
    cursor.execute(query, (employee_id, idle_duration, logged_time))
    conn.commit()
    cursor.close()
    conn.close()

# Example usage
# log_idle_time(1, "10 minutes")
