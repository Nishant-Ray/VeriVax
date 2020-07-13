from flask import Flask, render_template, session, request, send_file, Response, redirect, url_for, flash
from flask_session import Session
import random

app = Flask(__name__)

app.secret_key = "hello there"

# alert = {
#     "type": "invite", # invite, delete, or doctor update
#     "from": "N4I2N521",
# }

users = []

admin = {
    "email": "janedoe@gmail.com",
    "password": "hello123",
    "name": "Jane Doe",
    "dob": "1990-08-24",
    "type": "Manager",
    "organization": "VMware",
    "id": "2VDMPG18",
    "vaccine": True,
    "profile": "/profile_4.jpg",
    "alerts": []
}

kevin = {
    "email": "kevinlewis@gmail.com",
    "password": "hello123",
    "name": "Kevin Lewis",
    "dob": "1992-07-21",
    "type": "Member",
    "organization": "VMware",
    "id": "6U8LJY87",
    "vaccine": True,
    "profile": "/profile_1.jpeg",
    "alerts": []
}

rob = {
    "email": "robtrevor@gmail.com",
    "password": "hello123",
    "name": "Rob Trevor",
    "dob": "1981-03-04",
    "type": "Member",
    "organization": "VMware",
    "id": "C54N521B",
    "vaccine": False,
    "profile": "/profile_2.jpg",
    "alerts": []
}

nancy = {
    "email": "nancybush@gmail.com",
    "password": "hello123",
    "name": "Nancy Bush",
    "dob": "1996-01-29",
    "type": "Member",
    "organization": "VMware",
    "id": "9E9V5XQ1",
    "vaccine": True,
    "profile": "/profile_3.jpg",
    "alerts": []
}

users.append(admin)
users.append(kevin)
users.append(rob)
users.append(nancy)

@app.route("/", methods=["POST", "GET"])
@app.route("/home", methods=["POST", "GET"])
def index():
    global users

    if "currentUser" not in session:
        return redirect(url_for('login'))
    
    return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    global users

    if request.method == "POST":
        # Get login form data

        newUser = {
            "email": request.form["em"],
            "password": request.form["pw"]
        }

        accountMatch = False

        for user in users:
            if newUser.get("email") == user.get("email") and newUser.get("password") == user.get("password"):
                session["currentUser"] = user
                accountMatch = True

        if accountMatch:
            return redirect(url_for('index'))
        else:
            print("Incorrect email or password!")
            return render_template("login.html")
        
    elif "currentUser" in session:
        return redirect(url_for('index'))
    elif request.method == "GET" or "currentUser" not in session:
        return render_template("login.html")

@app.route("/register", methods=["POST", "GET"])
def register():
    global users

    if request.method == "POST":
        # Get register form data
        
        type = request.form["type"]
        if type == "1":
            type = "General User"
        elif type == "2":
            type = "Doctor"
        else:
            type = "Manager"

        newUser = {
            "email": request.form["em"],
            "password": request.form["pw"],
            "name": request.form["nm"],
            "dob": request.form["dob"],
            "type": type,
            "organization": None,
            "id": generateID(),
            "vaccine": False,
            "profile": "/default_profile.png",
            "alerts": []
        }

        accountExists = False

        for user in users:
            if newUser.get("email") == user.get("email"):
                accountExists = True
        
        if not accountExists:
            print("Registration successful!")

            users.append(newUser)
            session["currentUser"] = newUser

            return redirect(url_for('index'))
        else:
            print("Account with that email exists!")
            return render_template("register.html")
    
    elif "currentUser" in session:
        return redirect(url_for('index'))
    elif request.method == "GET" or "currentUser" not in session:
        return render_template("register.html")

@app.route("/members", methods=["POST", "GET"])
def members():
    global users

    return render_template("members.html")

@app.route('/<id>')
def user(id):

    for user in users:
        if user["id"] == id:
            return render_template("user.html", specifiedUser=user)

    return redirect(url_for("members"), code=302)

@app.route('/delete:<id>')
def delete(id):
    global users

    for user in users:
        if user["id"] == id:

            deleteAlert = {
                "type": "delete", # invite, delete, or doctor update
                "from": session["currentUser"]["id"]
            }
            user["alerts"].append(deleteAlert)

            user["organization"] = None
            break

    return redirect(url_for("members"), code=302)

@app.route("/logout")
def logout():
    session.pop("currentUser", None)
    return redirect(url_for("index"), code=302)

# @app.route("/userlist")
# def userlist():
#     str = ""

#     for user in users:
#         str += user["email"] + ", " + user["password"] + ", " + user["name"] + ", " + user["dob"] + ", " + user["type"] + "<br>"

#     return str

def generateID():

    id = ''
    unique = True

    while True:
        unique = True
        id = randomSequence(8)

        for user in users:
            if id == user["id"]:
                unique = False

        if unique:
            break
        # else:
        #     continue

    return id

def randomSequence(length):
    id = ''
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    nums = '1234567890'

    for x in range(length):
        if random.randint(0, 1) == 0:
            id += letters[random.randint(0, 25)] 
        else:
            id += nums[random.randint(0, 9)] 
    
    return id

@app.route('/default_profile.png')
def default_profile():
    filename = 'default-profile.png'
    return send_file(filename, mimetype='image/png')

@app.route('/profile_1.jpeg')
def profile_1():
    filename = 'profile_1.jpeg'
    return send_file(filename, mimetype='image/jpeg')

@app.route('/profile_2.jpg')
def profile_2():
    filename = 'profile_2.jpg'
    return send_file(filename, mimetype='image/jpg')

@app.route('/profile_3.jpg')
def profile_3():
    filename = 'profile_3.jpg'
    return send_file(filename, mimetype='image/jpg')

@app.route('/profile_4.jpg')
def profile_4():
    filename = 'profile_4.jpg'
    return send_file(filename, mimetype='image/jpg')

@app.context_processor
def context_processor():
    global users

    isLoggedIn = False
    currentUser = None

    if "currentUser" in session:
        isLoggedIn = True
        currentUser = session["currentUser"]

    return dict(isLoggedIn=isLoggedIn, users=users, currentUser=currentUser)

if __name__ == "__main__":
    app.run(debug=True)