import mysql.connector
from datetime import datetime

def connect_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='employee_time_tracking'
    )

def log_compliance(employee_id, compliance_issue):
    conn = connect_db()
    cursor = conn.cursor()
    query = "INSERT INTO compliance_logs (employee_id, compliance_issue, logged_time) VALUES (%s, %s, %s)"
    logged_time = datetime.now().timestamp()
    cursor.execute(query, (employee_id, compliance_issue, logged_time))
    conn.commit()
    cursor.close()
    conn.close()

# Example usage
# log_compliance(1, "Completed safety training.")
