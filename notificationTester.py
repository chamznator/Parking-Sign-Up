from plyer import notification

# Function to show the notification
def show_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        timeout=10  # Notification duration in seconds
    )

# Call the function with your desired title and message
show_notification('Test Notification', 'This is a test message.')
