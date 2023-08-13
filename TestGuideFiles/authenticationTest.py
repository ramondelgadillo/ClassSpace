import pyrebase
from flask import session, request #cookies and CRUD library

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

email = 'tester11@gmail.com' #this will be replaced by a form from the html page later
password = '123456'  # need to be 6 character long

#create new user
# user = auth.create_user_with_email_and_password(email, password)
# print(user)

#sign in
user = auth.sign_in_with_email_and_password(email, password)

print(user)

#get account info, also need the statement above to work (need to sign in)
# info = auth.get_account_info(user['idToken'])
# print(info)

#send email verification to the provided email
# auth.send_email_verification(user['idToken'])

#reset email
# auth.send_password_reset_email(email)

