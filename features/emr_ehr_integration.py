import mysql.connector
from datetime import datetime

def connect_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='employee_time_tracking'
    )

def log_emr_integration(employee_id, emr_data):
    conn = connect_db()
    cursor = conn.cursor()
    query = "INSERT INTO emr_integration_logs (employee_id, emr_data, logged_time) VALUES (%s, %s, %s)"
    logged_time = datetime.now().timestamp()
    cursor.execute(query, (employee_id, emr_data, logged_time))
    conn.commit()
    cursor.close()
    conn.close()

# Example usage
# log_emr_integration(1, "Patient data integrated with EMR system.")
