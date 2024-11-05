from flask import Flask, render_template, request, flash, redirect
from datetime import datetime
import re
from modules.databaseManager import DatabaseManager 
from modules.emailSender import EmailSender
import os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# Regular expression for basic email validation
EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

db_manager = DatabaseManager()
email_Sender = EmailSender()

@app.route('/unsubscribe')
def unsubscribe():
    email = request.args.get('email')

    if email:
        db_manager.remove_email(email)
        flash("You have been unsubscribed from Morning Pulse.")
    else:
        flash("Invalid unsubscribe link or missing email.")
        
    return redirect('/')

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        email = request.form.get('email')
        country = request.form.get('country')
        city = request.form.get('city')
        home_address = request.form.get('home_address')
        work_address = request.form.get('work_address')
        arrival_time_str = request.form.get('arrival_time')

        arrival_time = datetime.strptime(arrival_time_str, '%H:%M').time()

        if not email or not country or not city:
            flash("Please fill in all fields.")
            return redirect('/')
        

        # Server-side email validation
        if not re.match(EMAIL_REGEX, email):
            flash("Invalid email address. Please enter a valid email.")
            return redirect('/')
        
        if db_manager.email_exists(email):
            flash("This email is already subscribed.")
            return redirect('/')
        

        # If email is valid, proceed with database

        if db_manager.add_email(email, country, city, work_address, home_address, arrival_time):
            flash("Email added successfully!")
        else:
            flash("Failed to add the email.")
        
        return redirect('/')
            
    return render_template('index.html')
