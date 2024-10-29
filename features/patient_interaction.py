import tkinter as tk
from tkinter import messagebox
import mysql.connector
import os
from datetime import datetime
import threading
from PIL import ImageGrab
import time

# Database connection
def connect_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='employee_time_tracking'
    )

def log_interaction(employee_id, interaction_details):
    conn = connect_db()
    cursor = conn.cursor()
    query = "INSERT INTO patient_interactions (employee_id, interaction_details, timestamp) VALUES (%s, %s, %s)"
    timestamp = datetime.now().timestamp()
    cursor.execute(query, (employee_id, interaction_details, timestamp))
    conn.commit()
    cursor.close()
    conn.close()

def take_screenshot(employee_id):
    # Create directory if it doesn't exist
    directory = "user_data/screenshots"
    if not os.path.exists(directory):
        os.makedirs(directory)
    timestamp = int(datetime.now().timestamp())
    screenshot_path = os.path.join(directory, f"screenshot_{employee_id}_{timestamp}.png")
    screenshot = ImageGrab.grab()
    screenshot.save(screenshot_path)

# Define the GUI
class TimeTrackingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee Time Tracking")
        self.root.geometry("900x600")

        self.login_frame = tk.Frame(self.root)
        self.create_login_frame()
        self.login_frame.pack()

        self.dashboard_frame = tk.Frame(self.root)
        self.create_dashboard_frame()

        self.current_user = None
        self.running = False

    def create_login_frame(self):
        tk.Label(self.login_frame, text="Username").pack(pady=5)
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.pack(pady=5)

        tk.Label(self.login_frame, text="Password").pack(pady=5)
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.pack(pady=5)

        login_button = tk.Button(self.login_frame, text="Login", command=self.login_user)
        login_button.pack(pady=10)

    def create_dashboard_frame(self):
        tk.Label(self.dashboard_frame, text="Welcome to the Employee Dashboard").pack(pady=10)

        # Buttons for time tracking
        start_button = tk.Button(self.dashboard_frame, text="Start Tracking", command=self.track_time)
        start_button.pack(pady=5)

        end_button = tk.Button(self.dashboard_frame, text="End Tracking", command=self.end_time_tracking)
        end_button.pack(pady=5)

        break_button = tk.Button(self.dashboard_frame, text="Take Break", command=self.take_break)
        break_button.pack(pady=5)

        resume_button = tk.Button(self.dashboard_frame, text="Resume Work", command=self.resume_work)
        resume_button.pack(pady=5)

    def login_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Connect to the database and validate user
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employees WHERE name = %s AND password = %s", (username, password))
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if result:
            self.current_user = result[0]  # Assuming the first column is the user ID
            self.show_dashboard()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def show_dashboard(self):
        self.login_frame.pack_forget()
        self.dashboard_frame.pack(fill='both', expand=True)

    def track_time(self):
        if not self.running:
            self.running = True
            self.start_time = datetime.now()

            # Log start time in the database
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO time_tracking (employee_id, start_time) VALUES (%s, %s)",
                (self.current_user, self.start_time)
            )
            conn.commit()
            cursor.close()
            conn.close()

            messagebox.showinfo("Track Time", "Time tracking started...")
            self.track_idle_time()  # Start tracking idle time

    def end_time_tracking(self):
        if self.running:
            self.running = False
            end_time = datetime.now()

            # Log end time in the database
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE time_tracking SET end_time = %s WHERE employee_id = %s AND end_time IS NULL",
                (end_time, self.current_user)
            )
            conn.commit()
            cursor.close()
            conn.close()

            # Log interaction and take screenshot
            log_interaction(self.current_user, "Tracking ended.")
            take_screenshot(self.current_user)

            messagebox.showinfo("Track Time", "Time tracking ended.")

    def take_break(self):
        if self.running:
            break_time = datetime.now()
            # Log break start in the database
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO breaks (employee_id, break_start) VALUES (%s, %s)",
                (self.current_user, break_time)
            )
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Break", "Break started.")

            # Log interaction and take screenshot
            log_interaction(self.current_user, "Break started.")
            take_screenshot(self.current_user)

    def resume_work(self):
        if self.running:
            resume_time = datetime.now()
            # Log break end in the database
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE breaks SET break_end = %s WHERE employee_id = %s AND break_end IS NULL",
                (resume_time, self.current_user)
            )
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Break", "Break ended.")

            # Log interaction and take screenshot
            log_interaction(self.current_user, "Break ended.")
            take_screenshot(self.current_user)

    def track_idle_time(self):
        # Start a new thread to check for idle time
        def idle_time_check():
            while self.running:
                # Logic to check if the user is idle
                idle_time = 0  # Replace with actual idle time checking logic
                if idle_time >= 300:  # 300 seconds = 5 minutes
                    self.log_idle_time()
                time.sleep(60)  # Check every minute

        threading.Thread(target=idle_time_check, daemon=True).start()

    def log_idle_time(self):
        idle_time = datetime.now()
        # Log idle time in the database
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO idle_times (employee_id, idle_time) VALUES (%s, %s)",
            (self.current_user, idle_time)
        )
        conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo("Idle Time", "Idle time recorded.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TimeTrackingApp(root)
    root.mainloop()
