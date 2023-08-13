import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# we're using this file as a placeholder for now, not planning to use it long term
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

userId = "oHi3QapZwJMn4vWRnSpe8dEWG5d2"
friendId = "iLm5i7dAzFNmf3qf7WihBf67wLm2"

# Add documents with auto IDs
data = {'name': 'Tester'}
# db.collection('persons').add(data) #use this to auto generate ID

# set ID by using the .document() method
# db.collection('persons').document("Tester").set(data) #set ID

#Merging, if set to False, the document will be override (collection unaffected)
db.collection('persons').document("Tester").set({'address': 'Long Beach1'}, merge = True) #set ID

#Subcollection
# db.collection('persons').document("Tester").collection('movies').add({'name': 'Computer Science'})

# Read file/documents with known ID
result = db.collection('persons').document("Tester").get()
if result.exists:
    print(result.to_dict()) # get all document in the collection




#How to get an element from a field of array
user_ref = db.collection('users').document(userId)
friend_ref = db.collection('users').document(friendId)
user = user_ref.get()
friend = friend_ref.get()
print(user_ref.get().get("friends")) # note, the get() method is call twice

#######################################################################
#TESTING ZONE#
