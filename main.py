import tkinter as tk
from tkinter import messagebox
import mysql.connector
import os
from datetime import datetime
import threading
import time  # Add this import for time.sleep
from PIL import ImageGrab

# Database connection setup
def connect_to_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='employee_time_tracking'
    )

def log_interaction(employee_id, patient_id, interaction_details):
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "INSERT INTO patient_interactions (employee_id, patient_id, interaction_details, logged_time) VALUES (%s, %s, %s, NOW())"
    cursor.execute(query, (employee_id, patient_id, interaction_details))
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
class NavBar(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.create_navbar()

    def create_navbar(self):
        home_button = tk.Button(self, text="Home", command=self.app.show_dashboard)
        home_button.pack(side="left", padx=10, pady=10)

        track_time_button = tk.Button(self, text="Track Time", command=self.app.track_time)
        track_time_button.pack(side="left", padx=10, pady=10)

        view_logs_button = tk.Button(self, text="View Logs", command=self.app.view_logs)
        view_logs_button.pack(side="left", padx=10, pady=10)

        logout_button = tk.Button(self, text="Logout", command=self.app.logout_user)
        logout_button.pack(side="left", padx=10, pady=10)

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
        self.patient_id = 1  # Set a default patient ID or implement a way to get it

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
        tk.Label(self.dashboard_frame, text="Welcome to the Employee Dashboard", font=("Arial", 16)).pack(pady=10)

        # Add a button to show tracking
        track_time_button = tk.Button(self.dashboard_frame, text="Track Time", command=self.track_time)
        track_time_button.pack(pady=5)

        # Add a button to show logs
        view_logs_button = tk.Button(self.dashboard_frame, text="View Logs", command=self.view_logs)
        view_logs_button.pack(pady=5)

        # Logout button
        logout_button = tk.Button(self.dashboard_frame, text="Logout", command=self.logout_user)
        logout_button.pack(pady=5)

    def login_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Connect to the database and validate user
        conn = connect_to_db()
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
        self.running = True
        employee_id = self.current_user  # Assuming current_user is the employee ID
        threading.Thread(target=self.track_time_with_screenshots, args=(employee_id, self.patient_id)).start()
        messagebox.showinfo("Track Time", "Time tracking started...")

    def track_time_with_screenshots(self, employee_id, patient_id):
        while self.running:
            interaction_details = "Tracking interaction..."  # Customize this message as needed
            log_interaction(employee_id, patient_id, interaction_details)  # Include patient_id here
            take_screenshot(employee_id)
            time.sleep(5)  # Wait for 5 seconds before next action

    def view_logs(self):
        # Dummy implementation for viewing logs
        messagebox.showinfo("View Logs", "Displaying logs...")  # Add your log viewing logic here

    def logout_user(self):
        self.running = False  # Stop the tracking
        self.dashboard_frame.pack_forget()
        self.login_frame.pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = TimeTrackingApp(root)
    root.mainloop()  # Corrected placement of mainloop
