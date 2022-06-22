import os
import requests
import urllib.parse
from cs50 import SQL
from flask import redirect, render_template, request, session
from functools import wraps
from datetime import datetime
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



