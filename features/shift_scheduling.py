import mysql.connector
from datetime import datetime

def connect_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='employee_time_tracking'
    )

def log_shift_schedule(employee_id, shift_details):
    conn = connect_db()
    cursor = conn.cursor()
    query = "INSERT INTO shift_schedules (employee_id, shift_details, scheduled_time) VALUES (%s, %s, %s)"
    scheduled_time = datetime.now().timestamp()
    cursor.execute(query, (employee_id, shift_details, scheduled_time))
    conn.commit()
    cursor.close()
    conn.close()

# Example usage
# log_shift_schedule(1, "Scheduled for 9 AM to 5 PM.")
