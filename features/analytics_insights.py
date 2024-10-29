import mysql.connector
from datetime import datetime

def connect_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='employee_time_tracking'
    )

def get_analytics(employee_id):
    conn = connect_db()
    cursor = conn.cursor()
    query = "SELECT COUNT(*) FROM patient_interactions WHERE employee_id = %s"
    cursor.execute(query, (employee_id,))
    interaction_count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return interaction_count

# Example usage
# analytics = get_analytics(1)
# print(f"Interactions for employee 1: {analytics}")
