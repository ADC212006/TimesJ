import mysql.connector
from datetime import datetime

def connect_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='employee_time_tracking'
    )

def log_automatic_tracking(employee_id, start_time, end_time):
    conn = connect_db()
    cursor = conn.cursor()
    query = "INSERT INTO automatic_time_tracking (employee_id, start_time, end_time) VALUES (%s, %s, %s)"
    cursor.execute(query, (employee_id, start_time, end_time))
    conn.commit()
    cursor.close()
    conn.close()

# Example usage
# log_automatic_tracking(1, "2024-10-01 09:00:00", "2024-10-01 17:00:00")
