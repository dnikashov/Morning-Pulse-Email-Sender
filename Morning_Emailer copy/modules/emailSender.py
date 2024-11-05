import smtplib
from email.message import EmailMessage
from modules.weather import Weather
from modules.driveTime import driveTime
import os
import urllib.parse
from modules.databaseManager import DatabaseManager 

def generate_unsubscribe_link(email):
    # URL-encode the email and include it in the unsubscribe link
    encoded_email = urllib.parse.quote(email)
    return f"https://dnikashov.pythonanywhere.com/unsubscribe?email={encoded_email}"

db_manager = DatabaseManager()

class EmailSender:
    def __init__(self):
        self.sender_email = os.getenv("EMAIL_SENDER")
        self.password = os.getenv("EMAIL_PASSWORD")
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587

    def send_email(self, recipient_email, country, city, address, destination, arrival_time):
        weather = Weather(city,country)
        weather_message = weather.get_message(country,city)
        unsubscribe_link = generate_unsubscribe_link(recipient_email)
        template_path = os.path.join('/home/dnikashov/flask/templates/email_template.html')

        drive_time = driveTime(address,destination, arrival_time)
        drive_message = drive_time.get_message()

        with open(template_path) as f:
            html_content = f.read()
            html_content = html_content.replace("{{ city }}", city)
            html_content = html_content.replace("{{ weather_message }}", weather_message)
            html_content = html_content.replace("{{ drive_message }}", drive_message)
            html_content = html_content.replace("{{ unsubscribe_link }}", unsubscribe_link)

        msg = EmailMessage()
        msg['Subject'] = "Morning Pulse Daily Email"
        msg['To'] = recipient_email
        msg['From'] = self.sender_email
        msg.set_content("This is a plain text version of the email", subtype='plain')  # Fallback plain text
        msg.add_alternative(html_content, subtype='html')  # HTML version of the email

        try:
            # Set up the server connection and login
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()  # Upgrade connection to secure
            server.login(self.sender_email, self.password)

            # Send the email
            server.send_message(msg)
            return True
        
        except Exception as e:
            return False

        finally:
            server.quit()