import mysql.connector
from datetime import datetime

def connect_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='employee_time_tracking'
    )

def log_shift_swap(employee_id, swapped_with, swap_details):
    conn = connect_db()
    cursor = conn.cursor()
    query = "INSERT INTO shift_swaps (employee_id, swapped_with, swap_details, logged_time) VALUES (%s, %s, %s, %s)"
    logged_time = datetime.now().timestamp()
    cursor.execute(query, (employee_id, swapped_with, swap_details, logged_time))
    conn.commit()
    cursor.close()
    conn.close()

# Example usage
# log_shift_swap(1, 2, "Swapped shifts with employee 2.")
