from flask import Flask, render_template, request, redirect, url_for, session
import pyrebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

config = {
    'apiKey': "AIzaSyDUjywVxsBCzTyacMEhR8bQAJrHuXHGUEY",
    'authDomain': "classspace-f6144.firebaseapp.com",
    'projectId': "classspace-f6144",
    'storageBucket': "classspace-f6144.appspot.com",
    'messagingSenderId': "431898875718",
    'appId': "1:431898875718:web:49c812b3d49fed140fb747",
    'measurementId': "G-S5TLSP8JNH",
    'databaseURL' : ''
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)
app.secret_key = "secretkey"

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        username = request.form["username"]

        # create user in Firebase authentication with email and password
        user = auth.create_user_with_email_and_password(email, password)

        # store username in Firebase database
        db.child("users").child(user["localId"]).set({"username": username})

        render_template("login.html")
    return render_template("signUp.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]

        # get user from Firebase database with username
        user = db.child("users").order_by_child("username").equal_to(username).limit_to_first(1).get().val()

        # convert user to dictionary
        user = list(user.values())[0]

        # get email and password from user in Firebase database
        email = user["email"]
        password = user["password"]

        # log in user in Firebase authentication with email and password
        auth.sign_in_with_email_and_password(email, password)
        session["username"] = username

        return redirect(url_for("dashboard"))
    return render_template("login.html")

@app.route("/")
def dashboard():
    if "username" in session:
        ip_address = request.remote_addr #Grab the user IP address
        print(ip_address)
        return "Welcome, {}. Your IP address is {}".format(session["username"], ip_address)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
