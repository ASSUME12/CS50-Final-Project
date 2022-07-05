import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for, jsonify, json
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required, get_navbar_data, send_mail, get_token
from random import seed
from random import randint
from werkzeug.utils import secure_filename
import uuid as uuid
from PIL import Image
from datetime import datetime, timedelta
import git
from flask_mail import Mail
now = datetime.now()
# seed random number generator
seed(1)

from datetime import datetime
now = datetime.now()

# Configure application
app = Flask(__name__)


# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = '587'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

mail=Mail(app)

# Configure Uploads
UPLOAD_FODER = 'static/profile_pics'
app.config["UPLOAD_FODER"] = UPLOAD_FODER

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finalProject.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    row = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    groupNumber = row[0]["groupNumber"]

    row = db.execute("SELECT * FROM vokabulariesPlace WHERE vokabularysGroup = ? ORDER BY dateTime DESC;", groupNumber)
    
    Assignments = []

    for Assignment in row:
        row1 = db.execute("SELECT * FROM ?;", Assignment["tableName"])
        x = {}
        AlreadyDid = db.execute("SELECT * FROM usersScores WHERE tableName = ? AND userId = ?",Assignment["tableName"], session["user_id"])
        x["name"] = row1[0]["nameOfAssignment"]
        x["tableName"] = Assignment["tableName"]
        if len(AlreadyDid) != 0:
            x["AlreadyDid"] = AlreadyDid[0]["AlreadyDid"]
        Assignments.append(x)
    
    navbar_data = get_navbar_data(session["user_id"])
    
    
    return render_template("index.html", loggedIn="True", Assignments=Assignments, navbar_data=navbar_data)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    try:
        if session["user_id"]:    
            session.clear()
    except:
        pass
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        rows = db.execute("SELECT * FROM users WHERE email = ?", request.form.get("email"))
        # Ensure username was submitted
        if not request.form.get("email"):
            flash("must provide email", category="error")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("must provide password", category="error")
        elif len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            flash("invalid username and/or password", category="error")
        else:
            if len(rows) == 1:
                session["user_id"] = rows[0]["id"]
            flash("Logged in successfully!", category="succes")
            # Redirect user to home page
            return redirect("/")
            
    # User reached route via GET (as by clicking a link or via redirect)
    return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    try:
        if session["user_id"]:    
            session.clear()
    except:
        pass
    # Redirect user to login form
    return redirect("/")

@app.route("/sign-up", methods=["GET", "POST"])
def signUp():
    try:
        if session["user_id"]:    
            session.clear()
    except:
        pass
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        rows1 = db.execute("SELECT * FROM users WHERE email = ?;", request.form.get("email"))
        rows2 = db.execute("SELECT * FROM users WHERE username = ?;", request.form.get("username"))
        if not request.form.get("email"):
            flash("must provide email", category="error")
            return 

        if not request.form.get("username"):
            flash("must provide username", category="error")
        elif " " in request.form.get("username"):
            flash("username can't contain spaces", category="error")
        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("must provide password", category="error")
        elif not request.form.get("confirmation"):
            flash("must confirm password", category="error")
        elif request.form.get("password") != request.form.get("confirmation"):
            flash("passwords dont match", category="error")
        elif not request.form.get("school"):
            flash("must provide a school", category="error")
        elif not request.form.get("class"):
            flash("must provide a Class", category="error")
        elif len(rows1) == 1:
                flash("Email already exists", category="error")
            # Ensure email does not exists and
        elif len(rows2) == 1:
                flash("Username already exists", category="error")
        else:
            group = 0
            if request.form.get("select") == "Teacher":
                group = randint(1,1000)
                rows = db.execute("SELECT * FROM users WHERE groupNumber = ?", group)
                while len((db.execute("SELECT * FROM users WHERE groupNumber = ?", group))) != 0:
                    group = randint(1,1000)
                ExpireTime = (now + timedelta(minutes=1)).strftime('%Y-%m-%d %H:%M:%S')
                db.execute("INSERT INTO usersTemporaryData (username, email, password, role, school, grade, profile_pic, groupNumber, token, TimeCreated, ExpireTime) VALUES (? , ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",request.form.get("username"), request.form.get("email"), generate_password_hash(request.form.get("password")),request.form.get("select"),request.form.get("school"),request.form.get("class"), "default.jpg", group, get_token(request.form.get("email"), "accouhntConfirmation"), now, ExpireTime)
                send_mail(request.form.get("email"), "accouhntConfirmation")
                #db.execute("INSERT INTO users (username, email, password, role, school, grade, profile_pic, groupNumber) VALUES (? , ?, ?, ?, ?, ?, ?, ?);",request.form.get("username"), request.form.get("email"), generate_password_hash(request.form.get("password")),request.form.get("select"),request.form.get("school"),request.form.get("class"), "default.jpg", group)
            else:
                group = request.form.get("groupNumber")
                row = db.execute("SELECT * FROM users WHERE groupNumber = ?;", int(group))

                if len(row) != 0:
                    ExpireTime = (now + timedelta(minutes=1)).strftime('%Y-%m-%d %H:%M:%S')
                    db.execute("INSERT INTO usersTemporaryData (username, email, password, role, school, grade, profile_pic, groupNumber, token, TimeCreated, ExpireTime) VALUES (? , ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",request.form.get("username"), request.form.get("email"), generate_password_hash(request.form.get("password")),request.form.get("select"),request.form.get("school"),request.form.get("class"), "default.jpg", 0, get_token(request.form.get("email"), "accouhntConfirmation"), now, ExpireTime)
                    send_mail(request.form.get("email"), "accouhntConfirmation")
                    #db.execute("INSERT INTO users (username, email, password, role, school, grade, profile_pic, groupNumber) VALUES (? , ?, ?, ?, ?, ?, ?, ?);",request.form.get("username"), request.form.get("email"), generate_password_hash(request.form.get("password")),request.form.get("select"),request.form.get("school"),request.form.get("class"), "default.jpg", 0)
                else:
                    flash('Group Number not found!', 'error')
                    return render_template("signUp.html")
            
            # Remember which user has logged in
            rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

            #session["user_id"] = rows[0]["id"]
            flash("We sent you a confirmation message with a link to your email. Please confirm that this is your email!", category="info")
            return redirect("/")

    return render_template("signUp.html")
            
        # Redirect user to home page
    # User reached route via GET (as by clicking a link or via redirect)

@app.route("/account-confirmation", methods=["GET", "POST"])
def accouhntConfirmationTemp():
    pass

@app.route("/account-confirmation/<token>", methods=["GET", "POST"])
def accouhntConfirmation(token):
    usertemporaryData = db.execute("SELECT * FROM usersTemporaryData WHERE token = ?;", token)

    if len(usertemporaryData) != 0:
        db.execute("INSERT INTO users (username, email, password, role, school, grade, profile_pic, groupNumber) VALUES (? , ?, ?, ?, ?, ?, ?, ?);",usertemporaryData[0]["username"], usertemporaryData[0]["email"], usertemporaryData[0]["password"],usertemporaryData[0]["role"],usertemporaryData[0]["school"],usertemporaryData[0]["grade"], "default.jpg", usertemporaryData[0]["groupNumber"])
        flash("Account confirmed successfully!", category="succes")
        # session["user_id"] = rows[0]["id"]
        if usertemporaryData[0]["role"] == "Student":
             db.execute("INSERT INTO joinGroupQueue (userUsername, groupToJoin) VALUES (?, ?);", usertemporaryData[0]["username"], usertemporaryData[0]["groupNumber"])
        return redirect("/") 
    else:
        flash('That is invalid token or expired. Please try again.', category='error')
        return redirect("/login")

@app.route("/reset-password", methods=['GET', 'POST'])
def reset_request():
    if request.method == 'POST':
        user = db.execute("SELECT * FROM users WHERE email = ?;",request.form.get("email"))
        if not request.form.get("email"):
            flash("must provide email", category="error")
        elif len(user) == 0:
            flash('Email not found.', category='error')
        else:
            send_mail(user[0]["email"], "resetPassword")
            flash('Reset request sent successfully!', category='succes')
            return redirect("/login")
            
    return render_template("reset_request.html")

@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    tokenRow = db.execute("SELECT * FROM tokens WHERE token = ?;", token)

    if request.method == 'GET':
        if len(tokenRow) == 0:
            flash('That is invalid token. Please try again.', category='error')
            return redirect("/login")
        else:
            tokenExpireDate = datetime.strptime(tokenRow[0]["ExpireTime"], '%Y-%m-%d %H:%M:%S')

            if now > tokenExpireDate:
                flash('That token has been expired. Please try again.', category='error')
                return redirect("/login")
            else:
                return render_template('change_password.html')
    else:
        if len(tokenRow) == 0:
            flash('That is invalid token. Please try again.', category='error')
            return redirect("/login")
        else:
            tokenExpireDate = datetime.strptime(tokenRow[0]["ExpireTime"], '%Y-%m-%d %H:%M:%S')

            result = now < tokenExpireDate
            if now > tokenExpireDate:
                flash('That token has been expired. Please try again.', category='error')
                return redirect("/login")
            else:
                password1 = request.form.get("password1")
                password2 = request.form.get("password2")

                if password1 != password2:
                    flash('Passwords dont match!', category='error')
                    return render_template("change_password.html")
                else:
                    user = db.execute("SELECT * FROM users WHERE id = ?;", tokenRow[0]["userId"])
                    db.execute("UPDATE users SET password = ? WHERE id = ?;", generate_password_hash(password1), user[0]["id"])
                    db.execute("DELETE FROM tokens WHERE userId = ?",user[0]["id"])
                    flash('Password changed Successfully!', 'succes')
                    return redirect("/login")

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    row = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    username = row[0]["username"]
    email = row[0]["email"]
    password = row[0]["password"]
    role = row[0]["role"]
    grade = row[0]["grade"]
    profile_pic_path = row[0]["profile_pic"]
    image_file = profile_pic_path
    groupNumber = row[0]["groupNumber"]
    if request.method == 'POST':
        row = db.execute("SELECT * FROM users WHERE id = ?;", session["user_id"])
        rows1 = db.execute("SELECT * FROM users WHERE email = ?;", request.form.get("email"))
        rows2 = db.execute("SELECT * FROM users WHERE username = ?;", request.form.get("username"))
        if not request.form.get("email"):
            flash("must provide email", category="error")
        if not request.form.get("username"):
            flash("must provide username", category="error")
        elif len(rows1) == 1 and row[0]["email"] != request.form.get("email"):
                flash("Email already exists", category="error")
        elif len(rows2) == 1 and row[0]["username"] != request.form.get("username"):
                flash("Username already exists", category="error")
        else:
            pic = request.files["Image"]
            if pic:
                pic_filename = secure_filename(pic.filename)

                im = Image.open(pic)
                new_size = im.resize((250, 250))
                pic = new_size

                pic_name = str(uuid.uuid1()) + "_" + pic_filename
                    
                pic.save(os.path.join(app.config["UPLOAD_FODER"], pic_name))
            else:
                pic_name = profile_pic_path
            db.execute("UPDATE users SET username = ?, email = ?, profile_pic = ? WHERE id = ?;",request.form.get("username"), request.form.get("email"),pic_name,session["user_id"])
            # Remember which user has logged in
            flash('Your profile has been updated!', 'success')
            return redirect("/profile")

    navbar_data = get_navbar_data(session["user_id"])
    return render_template('profile.html', title='Account', image_file=os.path.join(app.config["UPLOAD_FODER"], image_file), username=username, email=email, password=password, role=role, grade=grade,groupNumber=groupNumber, loggedIn="True", navbar_data=navbar_data)

@app.route('/AddAssignment', methods=['GET', 'POST'])
@login_required
def AddAssignment():
    row = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])

    if row[0]["role"] != "Teacher":
        flash("You are not allowed to visit this site!", "error")
        return redirect("/", loggedIn="True", role="Student")

    if request.method == "POST":

        if not request.form.get("nameOfAssignment"):
            flash("Must provide the name of the Assignment!", "error")
        elif not request.form.get("firstLanguage"):
            flash("Must provide the name of the first Language!", "error")
        elif not request.form.get("secondLanguage"):
            flash("Must provide the name of the second Language!", "error")
        else:
            vokabularies = []

            z = 0
            

            while request.form.get("lang1" + str(z)):
                vokabulary = {}

                firstVokabulary = request.form.get("lang1" + str(z))

                secondVokabulary = request.form.get("lang2" + str(z))

                vokabulary["firstVokabulary"] = firstVokabulary
                vokabulary["secondVokabulary"] = secondVokabulary

                vokabularies.append(vokabulary)

                z += 1

            x = randint(0,1000)
            while len(db.execute("SELECT * FROM vokabulariesPlace WHERE tableName = ?;", "vokabularyTable" + str(x))) == 1:
                x = randint(0,1000)

            tableName = "vokabularyTable" + str(x)
 
            db.execute("CREATE TABLE ? (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, nameOfAssignment TEXT NOT NULL, firstLanguage TEXT NOT NULL, secondLanguage TEXT NOT NULL, firstVokabulary TEXT NOT NULL, secondVokabulary TEXT NOT NULL);", tableName)
            formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
            db.execute("INSERT INTO vokabulariesPlace (tableName, vokabularysGroup, dateTime) VALUES (?, ?, ?);", tableName, row[0]["groupNumber"], formatted_date)


            for vokabulary in vokabularies:
                db.execute("INSERT INTO ? (nameOfAssignment, firstLanguage, secondLanguage, firstVokabulary, secondVokabulary) VALUES (?, ?, ?, ?, ?);", tableName, request.form.get("nameOfAssignment"),request.form.get("firstLanguage"), request.form.get("secondLanguage"), vokabulary["firstVokabulary"], vokabulary["secondVokabulary"])
   
            Teacher = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
            groupNumber = Teacher[0]["groupNumber"]

            users = db.execute("SELECT * FROM users WHERE groupnumber = ?;", groupNumber)

            Students = db.execute("SELECT * FROM users WHERE role = ? AND groupNumber = ?","Student", groupNumber)
            if len(Students) != 0:
                for Student in Students:
                    db.execute("INSERT INTO usersScores (userId, tableName, usersGroup, NumberOfvokabularies, usersCorrectVokabularies, usersTries, AlreadyDid) VALUES(?, ?, ?, ?, ?, ?, ?);", Student["id"], tableName, groupNumber, 0, 0, 0, "False")

    navbar_data = get_navbar_data(session["user_id"])
    return render_template("Add_Vokabulary_Teacher.html", loggedIn="True", navbar_data=navbar_data)

@app.route('/TestMe', methods=['GET', 'POST'])
@login_required
def TestMe():
    navbar_data = get_navbar_data(session["user_id"])
    return render_template("TestMe.html", loggedIn="True", navbar_data=navbar_data)

@app.route('/Progress', methods=['GET'])
@login_required
def Progress():

    tableName = request.args.get("tableName")

    usersScore1 = db.execute("SELECT * FROM usersScores WHERE tableName = ?;", tableName) 

    usersScore2 = []
    usersUsername = []
    
    for user in usersScore1:
        username = db.execute("SELECT * FROM users WHERE id = ?", user["userId"])
        user["username"] = username[0]["username"]
        user["vokabulariesTries"] = user["NumberOfvokabularies"] * user["usersTries"]
        if not user["username"] in usersUsername:
            usersUsername.append(user["username"])
        usersScore2.append(user)

    AssignmentName = db.execute("SELECT * FROM ?;",tableName)
    navbar_data = get_navbar_data(session["user_id"])
    return render_template("Progress.html", loggedIn="True", usersScore=usersScore2, usersUsername=usersUsername, navbar_data=navbar_data, tableName=tableName, Assignment=AssignmentName[0]["nameOfAssignment"])

@app.route('/getTestMeData', methods=['POST'])
def getTestMeData():
    if request.method == "POST":
        tableName = request.args.get("tableName")
        rows = db.execute("SELECT * FROM ?;", tableName)

        vokabularies = []

        for row in rows:
            vokabulary = {}

            firstVokabulary = row["firstVokabulary"]

            secondVokabulary = row["secondVokabulary"]

            vokabulary["firstVokabulary"] = firstVokabulary
            vokabulary["secondVokabulary"] = secondVokabulary

            vokabularies.append(vokabulary)

        return jsonify({'data': vokabularies, 'firstLanguage': rows[0]["firstLanguage"], 'secondLanguage': rows[0]["secondLanguage"]})

@app.route('/CheckAnswers', methods=['POST'])
def CheckAnswers():
    Answers = []
    tableName = request.form.get("tableIdentidfier")
    index = 0
    while request.form.get("lang1" + str(index)):   
        answer = {}

        answer["lang1" + str(index)] = request.form.get("lang1" + str(index))
        answer["lang2" + str(index)] = request.form.get("lang2" + str(index))

        Answers.append(answer)
        index += 1

    row = db.execute("SELECT firstVokabulary, secondVokabulary FROM ?;", tableName)

    index = 0

    correctAsnwersCount = 0
    worngAsnwersCount = 0

    AllAnswersWithResult = []
    for answer in Answers:
        if answer["lang1" + str(index)] == row[index]["firstVokabulary"] and answer["lang2" + str(index)] == row[index]["secondVokabulary"]:
            wrongAnswer = {}
            wrongAnswer["firstVokabulary"] = answer["lang1" + str(index)]
            wrongAnswer["secondVokabulary"] = answer["lang2" + str(index)]
            wrongAnswer["result"] = "correct"
            AllAnswersWithResult.append(wrongAnswer)
            correctAsnwersCount += 1
        else:
            wrongAnswer = {}
            wrongAnswer["firstVokabulary"] = answer["lang1" + str(index)]
            wrongAnswer["secondVokabulary"] = answer["lang2" + str(index)]
            wrongAnswer["result"] = "wrong"
            AllAnswersWithResult.append(wrongAnswer)
            worngAsnwersCount += 1
        
        index += 1

    user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    usersScore = db.execute("SELECT * FROM usersScores WHERE userId = ? AND tableName = ?;", session["user_id"],tableName)
    tries = 0

    if len(usersScore) != 0:
        tries = usersScore[len(usersScore) - 1]["usersTries"] + 1
    else:
        tries = 1
    
  #  correctAsnwersCount = usersScore[0]["usersCorrectVokabularies"] + correctAsnwersCount

    if tries == 1:
        db.execute("UPDATE usersScores SET NumberOfvokabularies = ?, usersCorrectVokabularies = ?, usersTries = ?, AlreadyDid = ? WHERE userId = ? AND tableName = ?;",len(Answers), correctAsnwersCount, tries, "True", session["user_id"], tableName)
    else:
        db.execute("INSERT INTO usersScores (userId, NumberOfvokabularies, usersCorrectVokabularies, usersTries, AlreadyDid, tableName, usersGroup) VALUES (?, ?, ?, ?, ?, ?, ?);",session["user_id"], len(Answers), correctAsnwersCount, tries, "True", tableName, user[0]["groupNumber"])
    #userScores = db.execute("SELECT * FROM usersScores WHERE userId = ?")


    navbar_data = get_navbar_data(session["user_id"])
    return render_template("result.html", loggedIn="True", correctAsnwersCount=correctAsnwersCount, worngAsnwersCount=worngAsnwersCount, AllAnswersWithResult=AllAnswersWithResult, navbar_data=navbar_data)

@app.route('/ClassMembers', methods=['GET', 'POST'])
@login_required
def ClassMembers():

    currentUser = db.execute("SELECT * FROM users WHERE id = ?;", session["user_id"])
    Members = db.execute("SELECT * FROM users WHERE groupNumber = ?;", currentUser[0]["groupNumber"])

    MembersQueue = db.execute("SELECT * FROM users JOIN joinGroupQueue ON users.username = joinGroupQueue.userUsername;")
    for Member in Members:
        Member["profile_pic"] = os.path.join(app.config["UPLOAD_FODER"], Member["profile_pic"])
    
    for Member in MembersQueue:
        Member["profile_pic"] = os.path.join(app.config["UPLOAD_FODER"], Member["profile_pic"])


    navbar_data = get_navbar_data(session["user_id"])
    return render_template("ClassMembers.html", loggedIn="True", Members=Members, MembersQueue=MembersQueue, navbar_data=navbar_data)

@app.route('/AcceptUser', methods=['POST'])
def AcceptUser():
    userID = request.form.get("accept")
    username = db.execute("SELECT * FROM users WHERE id = ?;", int(userID))
    groupNumber = db.execute("SELECT * FROM joinGroupQueue WHERE userUsername = ?;", username[0]["username"])
    db.execute("UPDATE users SET groupNumber = ? WHERE id = ?;", int(groupNumber[0]["groupToJoin"]), int(userID))
    db.execute("DELETE FROM joinGroupQueue WHERE userUsername = ?", username[0]["username"])


    notificationTitle = "Join request accepted"
    notification = "You were accepted to join group " + str(groupNumber[0]["groupToJoin"])
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
    db.execute("INSERT INTO notifications (userId, notificationTitle, notification, dateTime) VALUES (?, ?, ?, ?);", userID, notificationTitle, notification, formatted_date)

    Assignments = db.execute("SELECT * FROM vokabulariesPlace WHERE vokabularysGroup = ?;", groupNumber[0]["groupToJoin"])
    if len(Assignments) != 0:
        for Assignment in Assignments:
            db.execute("INSERT INTO usersScores (userId, tableName, usersGroup, NumberOfvokabularies, usersCorrectVokabularies, usersTries, AlreadyDid) VALUES(?, ?, ?, ?, ?, ?, ?);", userID, Assignment["tableName"], groupNumber[0]["groupToJoin"], 0, 0, 0, "False")
    
    return redirect("/ClassMembers")

@app.route('/DeclineUser', methods=['POST'])
def DeclineUser():

    userId = request.form.get("decline")
    username = db.execute("SELECT * FROM users WHERE id = ?;", int(userId))
    groupNumber = db.execute("SELECT * FROM joinGroupQueue WHERE userUsername = ?;", username[0]["username"])
    #db.execute("UPDATE users SET groupNumber = ? WHERE id = ?;", int(groupNumber[0]["groupToJoin"]), int(userID))
    db.execute("DELETE FROM joinGroupQueue WHERE userUsername = ?", username[0]["username"])

    notificationTitle = "Join request declined"
    notification = "You were declined to join group " + str(groupNumber[0]["groupToJoin"])
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
    db.execute("INSERT INTO notifications (userId, notificationTitle, notification, dateTime) VALUES (?, ?, ?, ?);", userId, notificationTitle, notification, formatted_date)

    return redirect("/ClassMembers")

@app.route('/requestNewGroup', methods=['GET', 'POST'])
@login_required
def requestNewGroup():
    row = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    role = row[0]["role"]
    username = row[0]["username"]
    groupNumber = row[0]["groupNumber"]

    row = db.execute("SELECT * FROM vokabulariesPlace WHERE vokabularysGroup = ?;", groupNumber)
    notifications = db.execute("SELECT * FROM notifications WHERE userId = ? ORDER BY dateTime;", session["user_id"])

    joinGroupQueue = db.execute("SELECT * FROM joinGroupQueue WHERE userUsername = ?;", username)

    if len(joinGroupQueue) == 1:
        flash("You are already in a queue", "error")
        return redirect("/")

    if request.method == "POST":
        if not request.form.get("groupNumber"):
            flash("must provide group Number", "error")
        else:
            group = request.form.get("groupNumber")
            row = db.execute("SELECT * FROM users WHERE groupNumber = ?;", int(group))

            if len(row) != 0:
                db.execute("INSERT INTO joinGroupQueue (userUsername, groupToJoin) VALUES (?, ?);", username, group)
                flash("Requested Successfully!", "succes")
                return redirect("/")
            else:
                flash('Group Number not found!', 'error')
                return render_template("requestNewGroup.html")
        
    navbar_data = get_navbar_data(session["user_id"])
    return render_template("requestNewGroup.html", loggedIn="True", navbar_data=navbar_data)

@app.route('/<username>', methods=['GET', 'POST'])
@login_required
def profile_from_others(username):
    user = db.execute("SELECT * FROM users WHERE username = ?;", username)

    if len(user) != 1:
        flash("Page not found", "error")
        return redirect("/")
    elif user[0]["id"] == session["user_id"]:
        return redirect("/profile")
    else:
        username = user[0]["username"]
        email = user[0]["email"]
        password = user[0]["password"]
        role = user[0]["role"]
        grade = user[0]["grade"]
        profile_pic_path = user[0]["profile_pic"]
        image_file = profile_pic_path
        groupNumber = user[0]["groupNumber"]

        navbar_data = get_navbar_data(session["user_id"])
        return render_template('other_user_profile.html', title='Account', image_file=os.path.join(app.config["UPLOAD_FODER"], image_file), username=username, email=email, password=password, role=role, grade=grade,groupNumber=groupNumber, loggedIn="True", navbar_data=navbar_data)

@app.route('/getNotificationsNumber', methods=['POST'])
@login_required
def getNotificationsNumber():
    if request.method == "POST":
        
        notificationsNumber = db.execute("SELECT * FROM notifications WHERE userId = ? AND AlreadyRead = ?;",session["user_id"], "False")

        notificationsNumber = {"notificationsNumber": len(notificationsNumber)}
        return notificationsNumber

@app.route('/setnotificationsAlreadyRead', methods=['POST'])
@login_required
def setnotificationsAlreadyRead():
    if request.method == "POST":
        db.execute("UPDATE notifications SET AlreadyRead = ? WHERE userId = ?;","True", session["user_id"])

        notificationsNumber = db.execute("SELECT * FROM notifications WHERE userId = ? AND AlreadyRead = ?;",session["user_id"], "False")

        notificationsNumber = {"notificationsNumber": len(notificationsNumber)}
        return notificationsNumber

@app.route('/searchForUsers', methods=['POST'])
@login_required
def searchForUsers():
    if request.method == "POST":

        usersUsernamelookingFor = request.args.get("username")

        users = db.execute("SELECT id, username, role, profile_pic FROM users WHERE username LIKE ?  ORDER BY username;", usersUsernamelookingFor+"%")

        if usersUsernamelookingFor == "":
            usersdict = {"users": -1}
            return usersdict 

        usersdict = {"users": users}
        return usersdict

@app.route('/test', methods=['GET'])
@login_required
def test():
    try:
        if session["user_id"]:    
            session.clear()
    except:
        pass
    db.execute("DROP TABLE users;")

    vokabulariesPlace = db.execute("SELECT * FROM vokabulariesPlace;")

    for vokabulary in vokabulariesPlace:
        db.execute("DROP TABLE ?;", vokabulary["tableName"])
    
    db.execute("DROP TABLE vokabulariesPlace;")
    db.execute("DROP TABLE joinGroupQueue;")
    db.execute("DROP TABLE notifications;")
    db.execute("DROP TABLE usersScores;")

    db.execute("CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, email TEXT NOT NULL, password TEXT NOT NULL, role TEXT NOT NULL, school TEXT NOT NULL, grade TEXT NOT NULL, profile_pic TEXT NOT NULL, groupNumber INTEGER NOT NULL);")
    db.execute("CREATE TABLE vokabulariesPlace (vokabularysId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, tableName INTEGER NOT NULL UNIQUE, vokabularysGroup INTEGER NOT NULL, dateTime DATETIME);")
    db.execute("CREATE TABLE joinGroupQueue (queueID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, userUsername INTEGER NOT NULL UNIQUE, groupToJoin INTEGER NOT NULL);")
    db.execute("CREATE TABLE notifications (notificationId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, userId INTEGER NOT NULL, notificationTitle TEXT NOT NULL, notification TEXT NOT NULL, dateTime DATETIME, AlreadyRead TEXT NOT NULL DEFAULT 'False');")
    db.execute("CREATE TABLE usersScores (userId INTEGER NOT NULL, tableName INTEGER NOT NULL, usersGroup INTEGER NOT NULL, NumberOfvokabularies INTEGER NOT NULL, usersCorrectVokabularies INTEGER NOT NULL, usersTries INTEGER NOT NULL DEFAULT 0, AlreadyDid TEXT NOT NULL DEFAULT 'False');")
    return  redirect("/")

    # userId = 8
    # username = db.execute("SELECT * FROM users WHERE id = ?;", int(userId))
    # #groupNumber = db.execute("SELECT * FROM joinGroupQueue WHERE userUsername = ?;", username[0]["username"])
    # #db.execute("UPDATE users SET groupNumber = ? WHERE id = ?;", int(groupNumber[0]["groupToJoin"]), int(userID))
    # db.execute("DELETE FROM joinGroupQueue WHERE userUsername = ?", username[0]["username"])

    # notificationTitle = "Join request declined"
    # notification = "You were declined to join group " + "138"
    # formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
    # db.execute("INSERT INTO notifications (userId, notificationTitle, notification, dateTime) VALUES (?, ?, ?, ?);", userId, notificationTitle, notification, formatted_date)

    # return redirect("/ClassMembers")