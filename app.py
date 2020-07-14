from flask import Flask, render_template, session, request, send_file, Response, redirect, url_for, flash
from flask_session import Session
import random

app = Flask(__name__)

app.secret_key = "hello there"

# alert = {
#     "type": "invite", # invite, delete, or doctor update
#     "from": admin,
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
    "vaccines": ["1/7/2021"],
    "exposure": ["Tested Positive: 9/9/2020", "Recovered: 10/17/2020"],
    "conditions": ["Asthma (lifelong)"],
    "trips": ["Canada (returned 8/24/2020)"],
    "profile": "/profile_4.jpg",
    "alerts": [],
    "patients": []
}

alert = {
    "type": "invite",
    "from": admin
}

kevin = {
    "email": "kevinlewis@gmail.com",
    "password": "hello123",
    "name": "Kevin Lewis",
    "dob": "1992-07-21",
    "type": "Member",
    "organization": "VMware",
    "id": "6U8LJY87",
    "vaccines": [],
    "exposure": [],
    "conditions": [],
    "trips": [],
    "profile": "/profile_1.jpeg",
    "alerts": [],
    "patients": []
}

rob = {
    "email": "robtrevor@gmail.com",
    "password": "hello123",
    "name": "Rob Trevor",
    "dob": "1981-03-04",
    "type": "Member",
    "organization": "VMware",
    "id": "C54N521B",
    "vaccines": [],
    "exposure": [],
    "conditions": [],
    "trips": [],
    "profile": "/profile_2.jpg",
    "alerts": [],
    "patients": []
}

nancy = {
    "email": "nancydavis@gmail.com",
    "password": "hello123",
    "name": "Nancy Davis",
    "dob": "1996-01-29",
    "type": "Member",
    "organization": "VMware",
    "id": "9E9V5XQ1",
    "vaccines": [],
    "exposure": [],
    "conditions": [],
    "trips": ["New Zealand (returned 12/6/20)"],
    "profile": "/profile_3.jpg",
    "alerts": [],
    "patients": []
}

joe = {
    "email": "joesmith@gmail.com",
    "password": "hello123",
    "name": "Joe Smith",
    "dob": "1984-05-29",
    "type": "Doctor",
    "hospital": "Stanford Health",
    "id": "34B46AA0",
    "vaccines": ["3/2/2021"],
    "exposure": [],
    "conditions": [],
    "trips": [],
    "profile": "/profile_5.jpg",
    "alerts": [],
    "patients": [nancy]
}

fired = {
    "type": "delete",
    "from": rob
}

kevin["alerts"].append(fired)

users.append(admin)
users.append(kevin)
users.append(rob)
users.append(nancy)
users.append(joe)

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
        org = request.form["organization"]
        if type == "1":
            type = "Member"
            org = None
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
            "organization": org,
            "id": generateID(),
            "vaccines": [],
            "exposure": [],
            "conditions": [],
            "trips": [],
            "profile": "/default_profile.png",
            "alerts": [],
            "patients": []
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

    if "currentUser" in session:
        if session["currentUser"]["type"] == "Manager":
            return render_template("members.html")
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))

@app.route("/patients", methods=["POST", "GET"])
def patients():
    global users

    if "currentUser" in session:
        
        if session["currentUser"]["type"] == "Doctor":
            session.modified = True
            return render_template("patients.html")
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))

@app.route("/alerts", methods=["POST", "GET"])
def alerts():
    global users

    if "currentUser" in session:
        if session["currentUser"]["type"] == "Member":
            return render_template("alerts.html")
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))

@app.route("/settings", methods=["POST", "GET"])
def settings():
    global users

    if "currentUser" in session:
        return render_template("settings.html")
    else:
        return redirect(url_for('login'))

@app.route("/edit", methods=["POST", "GET"])
def edit():
    global users

    if request.method == "POST":
        
        currentUser = session["currentUser"]

        exposure = request.form["exposure"].split(", ")
        if len(exposure) != 1 or exposure[0] != '':
            currentUser["exposure"] = request.form["exposure"].split(", ")

        conditions = request.form["conditions"].split(", ")
        if len(conditions) != 1 or conditions[0] != '':
            currentUser["conditions"] = request.form["conditions"].split(", ")

        trips = request.form["trips"].split(", ")
        if len(trips) != 1 or trips[0] != '':
            currentUser["trips"] = request.form["trips"].split(", ")
        
        session["currentUser"] = currentUser
        session.modified = True

        return redirect(url_for('settings'))

    if "currentUser" in session:
        return render_template("edit.html")
    else:
        return redirect(url_for('login'))

@app.route("/doctoredit:<id>", methods=["POST", "GET"])
def doctoredit(id):
    global users

    if request.method == "POST":
        
        if session["currentUser"]["type"] == "Doctor":
            for user in users:
                if id == user["id"]:
                    for patient in session["currentUser"]["patients"]:
                        if patient["id"] == id:
                            vaccinations = request.form["vaccinations"].split(", ")
                            if len(vaccinations) == 1 and vaccinations[0] == '' and len(patient["vaccines"]) > 0:
                                patient["vaccines"] = []
                            elif len(vaccinations) != 1 or vaccinations[0] != '':
                                patient["vaccines"] = request.form["vaccinations"].split(", ")

                            exposure = request.form["exposure"].split(", ")
                            if len(exposure) == 1 and exposure[0] == '' and len(patient["exposure"]) > 0:
                                patient["exposure"] = []
                            elif len(exposure) != 1 or exposure[0] != '':
                                patient["exposure"] = request.form["exposure"].split(", ")

                            conditions = request.form["conditions"].split(", ")
                            if len(conditions) == 1 and conditions[0] == '' and len(patient["conditions"]) > 0:
                                patient["conditions"] = []
                            elif len(conditions) != 1 or conditions[0] != '':
                                patient["conditions"] = request.form["conditions"].split(", ")

                            trips = request.form["trips"].split(", ")
                            if len(trips) == 1 and trips[0] == '' and len(patient["trips"]) > 0:
                                patient["trips"] = []
                            elif len(trips) != 1 or trips[0] != '':
                                patient["trips"] = request.form["trips"].split(", ")
                            
                            updateAlert = {
                                "type": "doctor_update",
                                "from": session["currentUser"]
                            }

                            # patient["alerts"].append(updateAlert)
                            
                            session.modified = True
                            return render_template("user.html", specifiedUser=patient)
                            # return redirect(url_for('user', id=patient["id"]))

                    # return redirect(url_for('user', id=user["id"]))
                    return render_template("user.html", specifiedUser=user)
            return redirect(url_for('index'))
        else:
            return redirect(url_for('index'))

    if "currentUser" in session:
        if session["currentUser"]["type"] == "Doctor":
            for user in users:
                if id == user["id"]:
                    for patient in session["currentUser"]["patients"]:
                        if id == patient['id']:
                            return render_template("doctoredit.html", specifiedUser=patient)
                    return redirect(url_for('user', id=user["id"]))
            return redirect(url_for('patients'))
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))

@app.route('/user:<id>')
def user(id):
    global users

    if "currentUser" in session:
        if id == session["currentUser"]["id"]:
            return redirect(url_for("settings"))
        
        if session["currentUser"]["type"] == "Doctor":
            for user in users:
                if user["id"] == id:
                    for patient in session["currentUser"]["patients"]:
                        if patient["id"] == user["id"]:
                            return render_template("user.html", specifiedUser=patient)
        else:
            for user in users:
                if user["id"] == id:
                    return render_template("user.html", specifiedUser=user)

        return redirect(url_for("index"))
    else:
        return redirect(url_for('login'))

@app.route('/invite:<id>')
def invite(id):
    global users
    
    if "currentUser" in session:
        for user in users:
            if user["id"] == id:

                inviteAlert = {
                    "type": "invite", # invite, delete, or doctor update
                    "from": session["currentUser"]
                }
                user["alerts"].append(inviteAlert)

                break

        return redirect(url_for("index"))
    else:
        return redirect(url_for("login"))

@app.route('/delete:<id>')
def delete(id):
    global users

    if "currentUser" in session:
        for user in users:
            if user["id"] == id:

                if session["currentUser"]["type"] == "Doctor":
                    deleteAlert = {
                        "type": "doctor_delete",
                        "from": session["currentUser"]
                    }
                    session["currentUser"]["patients"].remove(user)
                    # print(session["currentUser"]["name"] + " has " + str(len(session["currentUser"]["patients"])) + " patients.")
                    user["alerts"].append(deleteAlert)
                    session.modified = True
                    return redirect(url_for("patients"))
                else:
                    deleteAlert = {
                        "type": "delete",
                        "from": session["currentUser"]
                    }
                    user["organization"] = None
                    user["alerts"].append(deleteAlert)
                    session.modified = True
                    return redirect(url_for("members"))

        return redirect(url_for("index"))
    else:
        return redirect(url_for("login"))

@app.route('/doctorrequest:<id>')
def doctorrequest(id):
    global users

    if "currentUser" in session:
        if session["currentUser"]["type"] == "Doctor":
            for user in users:
                if user["id"] == id:

                    doctorReqAlert = {
                        "type": "doctor_request", # invite, delete, or doctor update
                        "from": session["currentUser"]
                    }
                    user["alerts"].append(doctorReqAlert)
                    session.modified = True

                    break

            session.modified = True
            return redirect(url_for("alerts"))

        return redirect(url_for("index"))
    else:
        return redirect(url_for("login"))

@app.route('/removealert:<type>,<id>')
def removealert(type, id):
    global users

    if "currentUser" in session:
        if session["currentUser"]["type"] == "Member":
            for alert in session["currentUser"]["alerts"]:
                if alert["from"]["id"] == id and alert["type"] == type:

                    session["currentUser"]["alerts"].remove(alert)
                    session.modified = True
                    break

            return redirect(url_for("alerts"))

        return redirect(url_for("index"))
    else:
        return redirect(url_for("login"))

@app.route('/accept:<type>,<id>')
def accept(type, id):
    global users
    global rob

    if "currentUser" in session:
        if session["currentUser"]["type"] == "Member":
            for alert in session["currentUser"]["alerts"]:
                if alert["from"]["id"] == id and alert["type"] == type:

                    if type == "invite":
                        session["currentUser"]["organization"] = alert["from"]["organization"]
                    elif type == "doctor_request":
                        # alert["from"]["patients"].append(session["currentUser"])
                        alert["from"]["patients"].append(rob)

                    session["currentUser"]["alerts"].remove(alert)
                    
                    session.modified = True
                    return redirect(url_for("alerts"))

            # print(alert["from"]["name"] + " has " + str(len(alert["from"]["patients"])) + " patients.")
            return redirect(url_for("alerts"))

        return redirect(url_for("index"))
    else:
        return redirect(url_for("login"))

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

@app.route('/profile_5.jpg')
def profile_5():
    filename = 'profile_5.jpg'
    return send_file(filename, mimetype='image/jpg')

@app.context_processor
def context_processor():
    global users

    session.modified = True

    isLoggedIn = False
    currentUser = None

    if "currentUser" in session:
        isLoggedIn = True
        currentUser = session["currentUser"]

    return dict(isLoggedIn=isLoggedIn, users=users, currentUser=currentUser)

if __name__ == "__main__":
    app.run(debug=True)