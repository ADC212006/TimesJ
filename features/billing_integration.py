import mysql.connector
from datetime import datetime

def connect_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='employee_time_tracking'
    )

def log_billing(employee_id, billing_details):
    conn = connect_db()
    cursor = conn.cursor()
    query = "INSERT INTO billing_logs (employee_id, billing_details, logged_time) VALUES (%s, %s, %s)"
    logged_time = datetime.now().timestamp()
    cursor.execute(query, (employee_id, billing_details, logged_time))
    conn.commit()
    cursor.close()
    conn.close()

# Example usage
# log_billing(1, "Billing for patient consultation.")
