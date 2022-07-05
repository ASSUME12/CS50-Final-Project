import os
import requests
import urllib.parse
from cs50 import SQL
from flask import redirect, render_template, request, session, url_for
from functools import wraps
from datetime import datetime, timedelta
from flask_mail import Mail, Message
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import schedule
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
now = datetime.now()

db = SQL("sqlite:///finalProject.db")

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def get_navbar_data(userId):
    row = db.execute("SELECT * FROM users WHERE id = ?", userId)
    role = row[0]["role"]
    username = row[0]["username"]
    groupNumber = row[0]["groupNumber"]
    profile_pic_path = row[0]["profile_pic"]

    notifications = db.execute("SELECT * FROM notifications WHERE userId = ? ORDER BY dateTime DESC;", session["user_id"])

    for notification in notifications:

        date_time_obj = datetime.strptime(notification["dateTime"], '%Y-%m-%d %H:%M:%S')
        notification["dateTime"] = str(int(abs(datetime.now() - date_time_obj).total_seconds() / 3600)) + "#Hours ago"

        time = notification["dateTime"].split("#")
        time = time[0]

        if int(time) < 1:
            notification["dateTime"] = str(int(abs(datetime.now() - date_time_obj).total_seconds() / 60)) + " Minutes ago"
        else:
            notification["dateTime"] = notification["dateTime"].replace("#", " ")
    
    navbar_data = [
        {"username": username,
        "groupNumber": groupNumber,
        "role": role,
        "profile_pic_path": profile_pic_path},
        {"notifications": notifications},
        {"notificationslenght": len(notifications)}
    ]
    return navbar_data

def send_mail(email, tokenType):
    from app import mail
    if tokenType == "resetPassword":
        token = get_token(email, tokenType)
        msg = Message('Reset Password', sender='Vocabulary Trainer', recipients=[email])
        msg.body = f'''
        Hello,

        Follow this link to reset your Vocabulary Trainer password. You have 30 Minutes or the token will expire! 

        {url_for('reset_request', _external=True)  + '/'+ token}

        If you didn't ask to reset your password, you can ignore this email.

        Thanks,

        Your Vocabulary Trainer team
        '''
        mail.send(msg)
    elif tokenType == "accouhntConfirmation":
        token = get_token(email, tokenType)
        msg = Message('Account confirmation', sender='Vocabulary Trainer', recipients=[email])
        msg.body = f'''
        Hello,

        Follow this link to confirm your Vocabulary Trainer Account. You have 30 Minutes or the token will expire! 

        {url_for('accouhntConfirmationTemp', _external=True)  + '/'+ token}

        If you didn't register on vocabularytrainer.com, you can ignore this email.

        Thanks,

        Your Vocabulary Trainer team
        '''
        mail.send(msg)

    schedule.every(1).minutes.do(DeleteExpiredToken)
    
def get_token(email, type):
    serial = Serializer("UltimateVocabularyTrainere", expires_in=300)
    token = serial.dumps({'email': email}).decode('utf-8')
    tokenType = type
    currentTime = now.strftime('%Y-%m-%d %H:%M:%S')
    ExpireTime = (now + timedelta(minutes=1)).strftime('%Y-%m-%d %H:%M:%S')

    row = db.execute("SELECT * FROM tokens WHERE email = ?;", email)

    if len(row) == 1:
        db.execute("DELETE FROM tokens WHERE email = ?;",email)

    db.execute("INSERT INTO tokens (email, token, tokenType, TimeCreated, ExpireTime) VALUES (?, ?, ?, ?, ?);", email, token, tokenType, currentTime, ExpireTime)
    return token

def DeleteExpiredToken():
    db.execute("DELETE FROM tokens WHERE ? > ExpireTime", now)

scheduler = BackgroundScheduler()
scheduler.add_job(func=DeleteExpiredToken, trigger="interval", minutes=5)
scheduler.start()