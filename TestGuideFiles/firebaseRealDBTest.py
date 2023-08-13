import pyrebase
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for

config = {
    'apiKey': "AIzaSyDUjywVxsBCzTyacMEhR8bQAJrHuXHGUEY",
    'authDomain': "classspace-f6144.firebaseapp.com",
    'projectId': "classspace-f6144",
    'databaseURL': "https://classspace-f6144-default-rtdb.firebaseio.com/",
    'storageBucket': "classspace-f6144.appspot.com",
    'messagingSenderId': "431898875718",
    'appId': "1:431898875718:web:49c812b3d49fed140fb747",
    'measurementId': "G-S5TLSP8JNH",
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

# userdata = {"uid": "", "username": "", "email": ""}

# userdata["uid"] = "12345"
# userdata["username"] = "username"
# userdata["email"] = "email@gmail.com"

#Create with push and set
#db.push(userdata) #this will generate random ID to put down the info  #Push
# db.child("users").child(userdata["uid"]).set(userdata) #Use this for no duplication

#Update
# test1 = db.child("users").get() #This access the endpoint child and get the value and keys .child("8ZYBMAin7pMuhBTNQxXqpz9p3Cm2")
# for person in test1.each():
#     print(person.val())
#     print(person.key())
    
#     if(person.val()['username']=='username'):
#         print("found")
#         # to update
#         db.child("users").child(person.key()).update({'username': "newUsername"})

#Delete, can remove a single key only or the whole node
# db.child("users").child("uid").remove()
# for person in test1.each():
#     if(person.val()['username']=='username'):
#         print("found")
#         # to update
#         db.child("users").child(person.key()).child("username")

#Read
test2 = db.child("users").child("8ZYBMAin7pMuhBTNQxXqpz9p3Cm2").get() #This access the endpoint child and get the value and keys .child("8ZYBMAin7pMuhBTNQxXqpz9p3Cm2")
print(test2.val())
#it prints OrderedDict([('email', 'Kenny@gmail.com'), ('uid', '8ZYBMAin7pMuhBTNQxXqpz9p3Cm2'), ('username', 'KennyVu1')])









