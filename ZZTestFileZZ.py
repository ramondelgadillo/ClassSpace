from flask import Flask, redirect, url_for, render_template #flask routing library
from flask import session, request #cookies and CRUD library
#from flask_wtf import FlaskForm
import firebase_admin #firebase SDK
from firebase_admin import credentials
from firebase_admin import firestore
import ratemyprofessor
import pyrebase #Allow the use of Firebase services with python
import os
import time
import requests


app = Flask(__name__)

#Kenny: config flask with all firebase functionalities
config = {
    'apiKey': "AIzaSyDUjywVxsBCzTyacMEhR8bQAJrHuXHGUEY", #key for access
    'authDomain': "classspace-f6144.firebaseapp.com",
    'databaseURL': "https://classspace-f6144-default-rtdb.firebaseio.com/", #needed to get this from realDB
    'projectId': "classspace-f6144",
    'storageBucket': "classspace-f6144.appspot.com",
    'messagingSenderId': "431898875718",
    'appId': "1:431898875718:web:49c812b3d49fed140fb747",
    'measurementId': "G-S5TLSP8JNH",
}

#pyrebase simplify the process of utilizing firebase authorization methods
firebase = pyrebase.initialize_app(config) #connect pyrebase with flask by using the config disctionary 
auth = firebase.auth() #variable point to access to firebase authorization 
realDB = firebase.database() #realDB is assignto real time database

#secret key encrypt the cookie session code
app.secret_key = 'secretkey'
# app.secret_key = os.urandom(24) #use this in final code

#Kenny: link key for access to firestore database
cred = credentials.Certificate("serviceAccountKey.json") #This also help link other Google's services
firebase_admin.initialize_app(cred) #need to link flask with firebase admin SDK
db = firestore.client() #db is assignto real time database

userId = "xcTZ4e9TQnRKDsWAaik9ktEV4CD3"
friendId = "d1QzjHEqMfZH2NEBRyIQbZJyrB63"
email = "Tester77@gmail.com"


######################################################################
# #function to add a friend

# # get user and friend documents
# userReference = db.collection('users').document(userId)
# friendReference = db.collection('users').document(friendId)
# userData = db.collection('users').document(userId).get()
# friendData = db.collection('users').document(friendId).get()
# #print(userData.to_dict()) #use this to print out all the data in the variable (when .get() is called)

# # add friend to user's friend list
# if 'friends' not in db.collection('users').document(userId).get().to_dict():
#     db.collection('users').document(userId).set({'friends': ''}, merge = True)
#     time.sleep(4) #delay 4 second to help firebase catch up
#     delayDone = True
# else:
#     delayDone = True
# if delayDone:
#     userFriendsList = userData.get('friends')
# if not isinstance(userFriendsList, list): #if field friend doesn't exist, add it in
#     userFriendsList = []
# if friendId not in userFriendsList: #if friend is not already added
#     userFriendsList.append(friendId)
#     userReference.update({'friends': userFriendsList})

# # add user to the other-user's friend list
# if 'friends' not in db.collection('users').document(friendId).get().to_dict():
#     db.collection('users').document(friendId).set({'friends': ''}, merge = True)
#     time.sleep(3)
# otherFriendsList = friendData.get('friends')
# if not isinstance(otherFriendsList, list):
#     otherFriendsList = []
# if userId not in otherFriendsList:
#     otherFriendsList.append(userId)
#     friendReference.update({'friends': otherFriendsList})

##########################################################

# # function to remove a friend

# # get user and friend documents
# user_ref = db.collection('users').document(userId)
# friend_ref = db.collection('users').document(friendId)
# user = user_ref.get()
# friend = friend_ref.get()
# # print(user_ref.get().get("friends"))

# userFriendList = user.get("friends")
# friendFriendList = friend.get("friends")


# # remove friend from user's friend list
# if friendId in userFriendList:
#     userFriendList.remove(friendId)
#     user_ref.update({"friends": userFriendList})

# # remove user from friend's friend list
# if userId in friendFriendList:
#     friendFriendList.remove(userId)
#     friend_ref.update({"friends": friendFriendList})

################################################################

#########################################################

# # retrieve a user's friends list

# # Get a reference to the user document
# user_ref = db.collection('users').document(user_id)

# # Get the user document data
# user_data = user_ref.get().to_dict()
# print(user_data, "\n")

# # If the user has no friends, return an empty list
# if 'friends' not in user_data:
#     print()

# # Otherwise, get a list of the user's friend ids
# friend_ids = user_data['friends']

# # Create a list to hold the friend data
# friends = []

# # Loop through each friend id and get their data
# for friend_id in friend_ids:
#     friend_ref = db.collection('users').document(friend_id)
#     friend_data = friend_ref.get().to_dict()
#     friends.append(friend_data)

# print(friends)
################################################################

# #BEST WAY
# #Getting a user's username
# user_ref = db.collection('users').where('email', '==', email).limit(1)
# user_doc = user_ref.get()[0].to_dict()

# #user_ref is still in the user collection but haven't access a UID (document) 
# # yet, so we use index [0] to access it and then call to_dict() to display 
# # all field contents
# print(user_ref.get()[0].to_dict())

# userFriend = user_doc['friends']

# print(userFriend)

########################################################################

#Another way to navigate

# userReference = db.collection('users').document(userId).get().to_dict()

# friend = userReference['friends']
# friendNames = []
# for friend in friend:
#     fName = db.collection('users').document(friend).get().to_dict()['username']
#     friendNames.append(fName)
# print(friendNames)
# content = {'professor': 'None', 'content': 'poo poo', 'rating': '6',
#             'difficulty': 'Very Easy', 'title': 'pee pee', 'take_again': 'yes'}

# posts = db.collection('posts').document(userId).get().to_dict()
# db.collection('users').document(userId).collection("posts").add(content)

# posts = db.collection('posts').document(userId).collection('posts').document('M6hUZzyHsLwfGkqW9Esx').get().to_dict()
# content = db.collection('posts').document(userId).collection('posts').document('M6hUZzyHsLwfGkqW9Esx').get().to_dict()['content']

# print(content)


#####################Google API Tests######################

# Making a get request
ip_address = request.remote_addr
url = f'http://ip-api.com/json/{ip_address}'
response = requests.get(url).json()
 
# print response
print(response)
 
# print json content
print(response.json())

# Check if the response contains an error message
if 'message' in response:
    print(f"Error: {response['message']}")

# Check if the response contains the expected keys
if 'lat' not in response or 'lon' not in response:
    print("Error: Invalid response from IP API service")











