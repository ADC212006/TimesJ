import mysql.connector
from datetime import datetime

def connect_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='employee_time_tracking'
    )

def log_break_time(employee_id, break_duration):
    conn = connect_db()
    cursor = conn.cursor()
    query = "INSERT INTO break_logs (employee_id, break_duration, break_time) VALUES (%s, %s, %s)"
    break_time = datetime.now().timestamp()
    cursor.execute(query, (employee_id, break_duration, break_time))
    conn.commit()
    cursor.close()
    conn.close()

# Example usage
# log_break_time(1, "30 minutes")
