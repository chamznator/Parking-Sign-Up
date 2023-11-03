from selenium import webdriver
from selenium.webdriver.common.by import By
import time  # Import the time module
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
import os, sys
from win10toast import ToastNotifier

import tkinter as tk
import time
import datetime






#Part 1- UI


def save_license_plate(license_plate):
    appdata_dir = os.path.join(os.getenv('APPDATA'), 'ParkingReg')  # Replace 'YourAppName' with your application's folder name
    data_file_path = os.path.join(appdata_dir, 'license_plate.txt')

    os.makedirs(os.path.dirname(data_file_path), exist_ok=True)

    with open(data_file_path, "w") as file:
        file.write(license_plate)

def load_license_plate():
    appdata_dir = os.path.join(os.getenv('APPDATA'), 'ParkingReg')  # Replace 'YourAppName' with your application's folder name
    data_file_path = os.path.join(appdata_dir, 'license_plate.txt')

    try:
        with open(data_file_path, "r") as file:
            return file.read()
    except FileNotFoundError:
        return ""


def on_license_plate_change(*args):
    entered_license_plate = license_plate_var.get().upper()
    license_plate_var.set(entered_license_plate)

# Function to submit the license plate and start Selenium (only if a license plate is entered)
def submit_license_plate_and_run_selenium():
    entered_license_plate = license_plate_var.get()
    if entered_license_plate:
        result_label.config(text=f"Entered License Plate: {entered_license_plate}")
        save_license_plate(entered_license_plate)
        global stored_license_plate
        stored_license_plate = entered_license_plate
        window.destroy()
        run_selenium()  # Call the function to run Selenium

# Create the main window
window = tk.Tk()
window.title("Parking Registration, Aerosoft")  # Set the title

# Set window size
window.geometry("400x200")  # Set window size (width x height)

# Load the company logo image
logo = tk.PhotoImage(file="aerocol 1.png")  # Replace "company_logo.gif" with the path to your logo image

# Create a label to display the logo
logo_label = tk.Label(window, image=logo)
logo_label.pack(padx=10, pady=10, anchor="w")  # Add padding and anchor to the left (west)


# Create a label for the title
title_label = tk.Label(window, text="Parking Registration, Aerosoft", font=("Helvetica", 16, "bold"), fg="red")
title_label.pack(pady=10)  # Add some padding

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



# Function to run Selenium
def run_selenium():
    service = Service(executable_path='C:/Users/ChamathGuruge/Documents/Parking Sign Up/chromedriver.exe')
    options = webdriver.ChromeOptions()




    if getattr(sys, 'frozen', False):
        chromedriver_path=os.path.join(sys._MEIPASS, "chromedriver.exe")
        service=Service(executable_path=chromedriver_path)
        driver= webdriver.Chrome(service=service, options=options)
    else:
        driver = webdriver.Chrome(service=service, options=options)



    # Initialize the WebDriver (choose the appropriate browser)
    #Running Selenium Stuff

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

    try:
        driver.implicitly_wait(10)

        dropdown = driver.find_element(By.XPATH, '//*[@id="permitConfigSelect"]/div')
        dropdown.click()

        option = driver.find_element(By.XPATH, '//*[@id="Day Parking ($15 - expires at midnight)"]/span')
        option.click()

        licence = driver.find_element(By.ID, 'plateInput')
        licence.click()

        licence.send_keys(stored_license_plate)

        create = driver.find_element(By.ID, 'create')
        create.click()
        # Wait for 2 seconds
        time.sleep(2)

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











#Part 3- Notification

# Create a function to send a daily notification
def send_daily_notification():
    toaster = ToastNotifier()
    current_date = datetime.date.today()
    notification_title = "Parking Registration"
    notification_message = f"Today's date: {current_date} Please register for parking"
    # Set a large duration to make the notification persistent
    toaster.show_toast(notification_title, notification_message, icon_path='',duration=2147483647)

# Schedule the notification to run every day at a specific time
notification_time = datetime.time(9,30)  # 8:00 AM
while True:
    now = datetime.datetime.now().time()
    if now.hour == notification_time.hour and now.minute == notification_time.minute:
        send_daily_notification()
    time.sleep(60)  # Check every minute

# The script will keep running to check and send the daily notification