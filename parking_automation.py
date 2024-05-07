from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.service import Service
import os, sys
from win10toast import ToastNotifier
from selenium.webdriver.chrome.service import Service as ChromeService
#from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from plyer import notification  
import tkinter as tk
import datetime
from PIL import Image, ImageTk
from plyer import notification



import psutil

import psutil
import os
import sys


# Global flag to track if Selenium has run
selenium_has_run = False

"""def terminate_processes_by_name(process_name):
    current_pid = os.getpid()

    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'] == process_name and process.info['pid'] != current_pid:
            try:
                # Terminate the process
                psutil.Process(process.info['pid']).terminate()
            except Exception as e:
                print(f"Failed to terminate process {process_name}: {e}")

# Terminate background processes from a previous instance, if any
terminate_processes_by_name("parking_automation.exe")"""





# Part 1 - UI

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

image1 = Image.open(resource_path("aerocol_1.png"))

def save_license_plate(license_plate):
    appdata_dir = os.path.join(os.getenv('APPDATA'), 'ParkingReg')
    data_file_path = os.path.join(appdata_dir, 'license_plate.txt')

    os.makedirs(os.path.dirname(data_file_path), exist_ok=True)

    with open(data_file_path, "w") as file:
        file.write(license_plate)

def load_license_plate():
    appdata_dir = os.path.join(os.getenv('APPDATA'), 'ParkingReg')
    data_file_path = os.path.join(appdata_dir, 'license_plate.txt')

    try:
        with open(data_file_path, "r") as file:
            return file.read()
    except FileNotFoundError:
        return ""
def save_checkbox_state():
    appdata_dir = os.path.join(os.getenv('APPDATA'), 'ParkingReg')
    data_file_path = os.path.join(appdata_dir, 'checkbox_state.txt')

    os.makedirs(os.path.dirname(data_file_path), exist_ok=True)

    with open(data_file_path, "w") as file:
        for day, var in reminder_days.items():
            file.write(f"{day}:{var.get()}\n")

def load_checkbox_state():
    appdata_dir = os.path.join(os.getenv('APPDATA'), 'ParkingReg')
    data_file_path = os.path.join(appdata_dir, 'checkbox_state.txt')

    try:
        with open(data_file_path, "r") as file:
            for line in file:
                day, state = line.strip().split(':')
                reminder_days[day].set(int(state))
    except FileNotFoundError:
        pass  # If the file is not found, use default values

def on_license_plate_change(*args):
    entered_license_plate = license_plate_var.get().upper()
    license_plate_var.set(entered_license_plate)



# Function to submit the license plate and start Selenium (only if a license plate is entered)
def submit_license_plate_and_run_selenium():
    entered_license_plate = license_plate_var.get()
    if entered_license_plate:
        result_label.config(text=f"Entered License Plate: {entered_license_plate}")
        save_license_plate(entered_license_plate)
        save_checkbox_state()  # Save the state of reminder checkboxes
        global stored_license_plate
        stored_license_plate = entered_license_plate
        window.destroy()
        run_selenium()  # Call the function to run Selenium





# Create the main window
window = tk.Tk()
window.title("Parking Registration, Aerosoft")

# Global dictionary for reminder days
reminder_days = {
    "Monday": tk.IntVar(),
    "Tuesday": tk.IntVar(),
    "Wednesday": tk.IntVar(),
    "Thursday": tk.IntVar(),
    "Friday": tk.IntVar(),
    "Saturday": tk.IntVar(),
    "Sunday": tk.IntVar(),
}


# Set window size
window.geometry("400x350")  # Increased height for checkboxes and title

# Load the company logo image
logo = ImageTk.PhotoImage(image1)

# Create a label to display the logo
logo_label = tk.Label(window, image=logo)
logo_label.pack(anchor="w")  # Add padding and anchor to the left (west)

# Create a label for the title
title_label = tk.Label(window, text="Parking Registration, Aerosoft", font=("Helvetica", 16, "bold"), fg="red")
title_label.pack(pady=10)  # Add some padding

# Create a label for the "In office reminder days" title
reminder_title_label = tk.Label(window, text="In office reminder days", font=("Helvetica", 12, "bold"))
reminder_title_label.pack(pady=5)



checkbox_line = tk.Frame(window)
checkbox_line.pack()

for day, var in reminder_days.items():
    checkbox = tk.Checkbutton(checkbox_line, text=day[0], variable=var, font=("Helvetica", 12))
    checkbox.pack(side=tk.LEFT)

# Create a label to instruct the user
instructions_label = tk.Label(window, text="Enter your license plate:", font=("Helvetica", 12))
instructions_label.pack()

# Create a StringVar to store the license plate text and load the last entered plate
license_plate_var = tk.StringVar()
last_entered_license_plate = load_license_plate()
license_plate_var.set(last_entered_license_plate)

# Create an entry widget for the license plate
license_plate_entry = tk.Entry(window, textvariable=license_plate_var, font=("Helvetica", 12))
license_plate_entry.pack()

# Add a trace to monitor changes in the text field
license_plate_var.trace("w", on_license_plate_change)

# Create a button to submit the license plate and start Selenium (if a license plate is entered)
submit_button = tk.Button(window, text="Submit", command=submit_license_plate_and_run_selenium, font=("Helvetica", 12))
submit_button.pack(pady=10)  # Add some padding

# Create a label to display the entered license plate
result_label = tk.Label(window, text="", font=("Helvetica", 12))
result_label.pack()
# Load the state of reminder checkboxes
load_checkbox_state()



# Part 2 - Selenium Automation

def run_selenium():
    """service = Service(executable_path='C:/Users/ChamathGuruge/Documents/Parking Sign Up/chromedriver.exe')
    options = webdriver.ChromeOptions()

    if getattr(sys, 'frozen', False):
        chromedriver_path = os.path.join(sys._MEIPASS, "chromedriver.exe")
        service = Service(executable_path=chromedriver_path)    
        driver = webdriver.Chrome(service=service, options=options)
    else:
        driver = webdriver.Chrome(service=service, options=options)

    # Initialize the WebDriver (choose the appropriate browser)"""
    global selenium_has_run
    try:
        # Initialize Chrome WebDriver with manual setup
        chrome_service = ChromeService(executable_path='C:/Users/ChamathGuruge/Documents/Parking Sign Up/chromedriver.exe')
        chrome_options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
        print("Using Chrome WebDriver")
    except Exception as chrome_exception:
        print(f"Chrome initialization failed: {chrome_exception}, switching to Edge")
        try:
            # Correct initialization of Edge WebDriver with WebDriver Manager
            edge_service = EdgeService(EdgeChromiumDriverManager().install())
            driver = webdriver.Edge(service=edge_service)
            print("Using Edge WebDriver")
        except Exception as edge_exception:
            print(f"Edge initialization also failed: {edge_exception}")
            return  # Exit the function if both drivers fail
    # Running Selenium Stuff

    # Open the parking website
    driver.get("https://dashboard-login.offstreet.io/login?state=hKFo2SA3TmFsZGdPUFlBa29WekRJbkRwenlURklOUjZVTVlNd6FupWxvZ2luo3RpZNkgWHRxNmoyRmMzU0NFbVVsM014bEFWdmtvNEtMeDJYYWujY2lk2SBiRFB6T1hMMVFZQ1cyRHRiSGV4dHpPa1ZQbkM1QWlvTA&client=bDPzOXL1QYCW2DtbHextzOkVPnC5AioL&protocol=oauth2&audience=https%3A%2F%2Fovm.offstreet.ca%2F&redirect_uri=https%3A%2F%2Fdashboard.offstreet.io&wl=null&scope=openid%20profile%20email&response_type=code&response_mode=query&nonce=OUVkZnRrNGVPMDBHNXMyOWlmSTBabVU2czMwdWY4bmRFTVM5T2h5dWlJMg%3D%3D&code_challenge=CsS_krl5KY7KMRTdYFtLobFUL7-w0nb4sL1Zl3U2Ay4&code_challenge_method=S256&auth0Client=eyJuYW1lIjoiYXV0aDAtcmVhY3QiLCJ2ZXJzaW9uIjoiMS4xMi4xIn0%3D")

    try:
        # Find the username and password fields and enter your credentials
        username_field = driver.find_element(By.ID, "email")
        password_field = driver.find_element(By.ID, "password")

        username_field.send_keys("ctyndorf@aerosoftsys.com")
        password_field.send_keys("K8p0n3r1d!sAB")

        # Locate and click the login button
        login_button = driver.find_element(By.ID, "login")
        login_button.click()
    except Exception as e:
        print(f"Failed to log in: {str(e)}")
   
    wait = WebDriverWait(driver, 15)  # Wait for up to 15 seconds
    try:
        # Wait until the dropdown is clickable and then click it
        dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="permitConfigSelect"]/div')))
        dropdown.click()

        # Wait until the option is clickable and then click it
        option = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="Day Parking ($15 - expires at midnight)"]/span')))
        option.click()

        # Wait until the licence input is clickable
        licence = wait.until(EC.element_to_be_clickable((By.ID, 'plateInput')))
        licence.click()
        licence.send_keys(stored_license_plate)

        # Wait until the create button is clickable and then click it
        create = wait.until(EC.element_to_be_clickable((By.ID, 'create')))
        create.click()
        # Wait for 2 seconds
        time.sleep(2)
        selenium_has_run = True
        # Direct to the specified website
        driver.get("https://dashboard.offstreet.io/vehicles/active")
        # Add a delay to keep the browser open
        time.sleep(30)
       
    except Exception as e:
        print(f"Failed to complete the process: {str(e)}")

    # You may need to add additional steps for CAPTCHA, two-factor authentication, etc.

    # Close the browser when done
    driver.quit()

# Start the GUI main loop
window.mainloop()

# Part 3 - Notification

# Create a function to send a daily notification
def send_daily_notification():
    while True:
        current_datetime = datetime.datetime.now()
        current_day = current_datetime.strftime("%A")
        current_hour = current_datetime.hour
        current_minute = current_datetime.minute

        # Check if today is a reminder day and it's after 9:00 AM
        if reminder_days.get(current_day, False) and current_hour >= 9:
            # Keep reminding every 15 minutes until selenium_has_run is True
            while not selenium_has_run:
                # Check time again to ensure reminders are sent in new iteration only if it's still the same day
                current_datetime = datetime.datetime.now()
                new_current_day = current_datetime.strftime("%A")
                if new_current_day != current_day or selenium_has_run:
                    # Break if the day has changed or selenium_has_run has been set to True
                    break
                
                notification_title = "Parking Registration Reminder"
                notification_message = "Don't forget to register your parking today!"
                try:
                    notification.notify(
                        title=notification_title,
                        message=notification_message,
                        app_name='Parking Registration App',
                        timeout=10,  # Duration in seconds
                        # Optional: app_icon='path/to/your/icon.ico'  # Path to your .ico file (Windows)
                    )
                except Exception as e:
                    print(f"Failed to show notification. Error: {e}")
                    # Optionally, log the error to a file or handle it in another way

                # Wait for 15 minutes before sending the next reminder
                time.sleep(900)  # 900 seconds = 15 minutes

            # Once selenium_has_run is True, wait till the next day to check conditions again
            while current_datetime.strftime("%A") == current_day:
                time.sleep(3600)  # Check again in an hour if it's still the same day



send_daily_notification()

   
    
        
    
