import mysql.connector
from datetime import datetime

def connect_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='employee_time_tracking'
    )

def log_alert(employee_id, alert_message):
    conn = connect_db()
    cursor = conn.cursor()
    query = "INSERT INTO alerts (employee_id, alert_message, logged_time) VALUES (%s, %s, %s)"
    logged_time = datetime.now().timestamp()
    cursor.execute(query, (employee_id, alert_message, logged_time))
    conn.commit()
    cursor.close()
    conn.close()

# Example usage
# log_alert(1, "Reminder: Staff meeting at 3 PM.")
