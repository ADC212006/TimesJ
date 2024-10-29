import mysql.connector
from datetime import datetime

def connect_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='employee_time_tracking'
    )

def log_location(employee_id, location_data):
    conn = connect_db()
    cursor = conn.cursor()
    query = "INSERT INTO location_logs (employee_id, location_data, logged_time) VALUES (%s, %s, %s)"
    logged_time = datetime.now().timestamp()
    cursor.execute(query, (employee_id, location_data, logged_time))
    conn.commit()
    cursor.close()
    conn.close()

# Example usage
# log_location(1, "Location data captured.")
