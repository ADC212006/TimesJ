import mysql.connector
from datetime import datetime

def connect_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='employee_time_tracking'
    )

def generate_report(employee_id):
    conn = connect_db()
    cursor = conn.cursor()
    query = "SELECT * FROM patient_interactions WHERE employee_id = %s"
    cursor.execute(query, (employee_id,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

# Example usage
# report = generate_report(1)
# print(report)
