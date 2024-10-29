import mysql.connector
from datetime import datetime

def connect_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='employee_time_tracking'
    )

def log_patient_appointment(employee_id, patient_id, appointment_details):
    conn = connect_db()
    cursor = conn.cursor()
    query = "INSERT INTO patient_appointments (employee_id, patient_id, appointment_details, appointment_time) VALUES (%s, %s, %s, %s)"
    appointment_time = datetime.now().timestamp()
    cursor.execute(query, (employee_id, patient_id, appointment_details, appointment_time))
    conn.commit()
    cursor.close()
    conn.close()

# Example usage
# log_patient_appointment(1, 123, "Consultation at 10 AM.")
