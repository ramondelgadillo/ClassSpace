from flask import Flask, redirect, url_for, render_template #flask routing library
from flask import session, request #cookies and CRUD library
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import firebase_admin #firebase SDK
from firebase_admin import credentials
from firebase_admin import firestore
import ratemyprofessor
import pyrebase #Allow the use of Firebase services with python
import os
import time
import jinja2
import datetime
from flask_wtf.csrf import CSRFProtect
import requests
import sys
import uuid


global school_name 

app = Flask(__name__)
app.config['DEBUG'] = True

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

#Ryan: Secret key for FlaskForm
app.config['SECRET_KEY'] = "SUPER_SECRET_KEY"

# This is for commenting on the homepage:   csrf = CSRFProtect(app)

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

########################## Professor Class #############################################################################################################
#Ryan: Professor Class for database
class Professors(object):
    def __init__(self, name, department, school, rating, difficulty, num_ratings, would_take_again):
        self.name = name
        self.department = department
        self.school = school
        self.rating = rating
        self.difficulty = difficulty
        self.num_ratings = num_ratings
        self.would_take_again = would_take_again
    @staticmethod
    def from_dict(source):
        # [START_EXCLUDE]
        professor = Professors(source[u'name'], source[u'department'], source[u'school'], source[u'rating'], 
                               source[u'difficulty'], source[u'num_ratings'], source[u'would_take_again'],)
        return professor
        # [END_EXCLUDE]
    def to_dict(self):
        # [START_EXCLUDE]
        prof = {
            u'name': self.name,
            u'department': self.department,
            u'school': self.school,
            u'rating': self.rating,
            u'difficulty': self.difficulty,
            u'num_ratings': self.num_ratings,
            u'would_take_again': self.would_take_again, }
        return prof
        # [END_EXCLUDE]
    def __repr__(self):
        return (
            f'Professors(\
                name={self.name}, \
                department={self.department}, \
                school={self.school}, \
                rating={self.rating}, \
                difficulty={self.difficulty}, \
                num_ratings={self.num_ratings}, \
                would_take_again={self.would_take_again}\ )' )
# [END firestore_data_custom_type_definition]

#Ryan: def to addProfessor to database
def addProfessor(Name, Department, School, Rating, Difficulty, Num_ratings, Would_take_again):
    prof = Professors(name=Name, department=Department, school=School, 
                  rating=Rating, difficulty=Difficulty, num_ratings=Num_ratings, would_take_again=Would_take_again)
    db.collection(u'Professors').document(Name).set(prof.to_dict())
############################### end of Professor Class ###################################################################################################

########################## Review Class ##################################################################################################################
#Ryan: Professor Class for database
class Reviews(object):
    def __init__(self, Title, Review, Difficulty, Rating, Would_take_again):
        self.Title = Title
        self.Review = Review
        self.Difficulty = Difficulty
        self.Rating = Rating
        self.Would_take_again = Would_take_again
    @staticmethod
    def from_dict(source):
        # [START_EXCLUDE]
        review = Reviews(source[u'Title'], source[u'Review'], source[u'Difficulty'], source[u'Rating'], 
                            source[u'Would_take_again'],)
        return review
        # [END_EXCLUDE]
    def to_dict(self):
        # [START_EXCLUDE]
        rev = {
            u'Title': self.Title,
            u'Review': self.Review,
            u'Difficulty': self.Difficulty,
            u'Rating': self.Rating,
            u'Would_take_again': self.Would_take_again, }
        return rev
        # [END_EXCLUDE]
    def __repr__(self):
        return (
            f'Reviews(\
                Title={self.Title}, \
                Review={self.Review}, \
                Difficulty={self.Difficulty}, \
                Rating={self.Rating}, \
                Would_take_again={self.Would_take_again}\ )' )
# [END firestore_data_custom_type_definition]

#Ryan: def to addReview to database
def addReview(prof, Title, Review, Difficulty, Rating, Would_take_again):
    rev = Reviews(Title=Title, Review=Review, Difficulty=Difficulty,
                  Rating=Rating, Would_take_again=Would_take_again)
    db.collection(u'Professors').document(prof).collection(u'Reviews').document(rev.Title).set(rev.to_dict())
############################### END of Review Class #####################################################################################################


# Kenny: implemented follower functions
################################# START of Follower Functions ###########################################################################################
# function to add a friend
def follow(userId, friendId):
    # get user and friend documents
    userReference = db.collection('users').document(userId)
    friendReference = db.collection('users').document(friendId)
    userData = db.collection('users').document(userId).get()
    friendData = db.collection('users').document(friendId).get()
    #print(userData.to_dict()) #use this to print out all the data in the variable (when .get() is called)

    # add friend to user's friend list
    if 'friends' not in db.collection('users').document(userId).get().to_dict():
        db.collection('users').document(userId).set({'friends': ''}, merge = True)
        time.sleep(4) #delay 4 second to help firebase catch up
        delayDone = True
    else:
        delayDone = True
    if delayDone:
        userFriendsList = userData.get('friends')
    if not isinstance(userFriendsList, list): #if field friend doesn't exist, add it in
        userFriendsList = []
    if friendId not in userFriendsList: #if friend is not already added
        userFriendsList.append(friendId)
        userReference.update({'friends': userFriendsList})

    # add user to the other-user's friend list
    if 'friends' not in db.collection('users').document(friendId).get().to_dict():
        db.collection('users').document(friendId).set({'friends': ''}, merge = True)
        time.sleep(3)
    otherFriendsList = friendData.get('friends')
    if not isinstance(otherFriendsList, list):
        otherFriendsList = []
    if userId not in otherFriendsList:
        otherFriendsList.append(userId)
        friendReference.update({'friends': otherFriendsList})

# function to remove a friend
def unFollow(userId, friendId):
    # get user and friend documents
    userReference = db.collection('users').document(userId)
    friendReference = db.collection('users').document(friendId)
    user = userReference.get()
    friend = friendReference.get()
    # print(userReference.get().get("friends")) #Note, get() is called twice to get to the array in the field
    userFriendList = user.get("friends")
    friendFriendList = friend.get("friends")

    # remove friend from user's friend list
    if friendId in userFriendList:
        userFriendList.remove(friendId)
        userReference.update({"friends": userFriendList})
    # remove user from friend's friend list
    if userId in friendFriendList:
        friendFriendList.remove(userId)
        friendReference.update({"friends": friendFriendList})

################################## END of Follower Func ##################################################################################################


#Ramon: Home Page route ##################################################################################################################################
@app.route('/')
def home():
    if 'user' in session:
        userId = session['localId']
        user = db.collection('users').document(userId).get().to_dict()
        user_post_id_ref = db.collection('user_post_ids').document(userId).get()
        user_post_id_list = user_post_id_ref.get('post_ids')
        if not isinstance(user_post_id_list, list):
            user_post_id_list = []
            user_post_id_list.append("placeholder")
            return render_template("home.html")
        if isinstance(user_post_id_list, list):
            for posts in user_post_id_list:
                postReference = db.collection('post_stats').document(posts).get().to_dict()
                post_likes = postReference['post_likes']
                post_dislikes = postReference['post_dislikes']
                post_id = postReference['post_id']

                context = {
                "post_id" : post_id, 
                "post_likes": post_likes,
                "post_dislikes": post_dislikes,}
                posts = user.get('posts', [])
                return render_template("home.html", posts=posts, **context)
    
    # Pass a boolean variable to the template to indicate whether the user is logged in or not
    # logged_in=False
    return render_template("home.html")

#Ramon: This is for commenting on the homepage, It works until you logout then you won't be able to log back in. #################################
# @app.route('/add_comment', methods=['POST'])
# @csrf.exempt
# def add_comment():
#     if 'user' not in session:
#         return redirect(url_for('login'))

#     form = CommentForm()

#     if form.validate_on_submit():
#         reply = form.reply.data
#         userId = session['localId']

#         # Add comment to Firestore database
#         db.collection('comments').add({
#             'user_id': userId,
#             'reply': reply,
#             'timestamp': firestore.SERVER_TIMESTAMP
#         })

#     return redirect(url_for('home'))

# class CommentForm(FlaskForm):
#     reply = StringField('Reply', validators=[DataRequired()])

################################## END of Home page ######################################################################################################

################################# Rating posts ###########################################################################################################

#Ramon: class for professor rating
class ProfessorPost:
    def __init__(self, title, content, take_again, difficulty, help, attendance, professor, rating, post_id):
        self.title = title
        self.content = content
        self.rating = rating
        self.professor = professor
        self.take_again = take_again
        self.difficulty = difficulty
        self.help = help
        self.attendance = attendance
        self.post_id = post_id
        self.timestamp = datetime.datetime.now().strftime('%b  %d')
#Ramon: class for course rating
class CoursePost:
    def __init__(self, title, content, take_again, difficulty, homework, course, rating, post_id):
        self.title = title
        self.content = content
        self.rating = rating
        self.homework = homework
        self.course = course
        self.take_again = take_again
        self.difficulty = difficulty
        self.post_id = post_id
        self.timestamp = datetime.datetime.now().strftime('%b  %d')

#Ramon: class for school rating
class SchoolPost:
    def __init__(self, title, content, take_again, quality, campus, social, rating, post_id):
        self.title = title
        self.content = content
        self.rating = rating
        self.take_again = take_again
        self.quality = quality
        self.campus = campus
        self.social = social
        self.post_id = post_id
        self.timestamp = datetime.datetime.now().strftime('%b  %d')

#Ramon: Rating Professor Page route
@app.route('/postProfessor', methods=['GET', 'POST'])
def postProfessor():
    if 'localId' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        userId = session['localId']
        title = request.form['title']
        content = request.form['content']
        take_again = request.form['take_again']
        difficulty = request.form['difficulty']
        help = request.form['help']
        attendance = request.form['attendance']
        professor = request.form['professor']
        rating = request.form['rating']
        post_id = uuid.uuid4().hex
        post = ProfessorPost(title, content, take_again, difficulty, help, attendance, professor, rating, post_id)
        
        db.collection('users').document(userId).update({
            'posts': firestore.ArrayUnion([post.__dict__])
        })
        #Ryan: Reviews added to database
        prof_rev = professor
        check_db = db.collection(u'Professors').document(prof_rev).get()
        if check_db.exists:
            print("exists, creating title")
            addReview(professor, title, content, difficulty, rating, take_again)
            print("added review to db")
        else:
            print("doesn't exist")
        postdata = {"post_id": "", "post_likes": "", "post_dislikes": ""}
        postdata["post_id"] = post_id
        postdata["post_likes"] = 0
        postdata["post_dislikes"] = 0
        db.collection('post_stats').document(post_id).set(postdata, merge = True)

        userData = db.collection('user_post_ids').document(userId).get()
        user_post_id_list = userData.get('post_ids')
        if not isinstance(user_post_id_list, list):
            user_post_id_list = []
        user_post_id_list.append(post_id)
        db.collection('user_post_ids').document(userId).set({'post_ids': user_post_id_list}, merge = True)

        return redirect(url_for('home'))
    return render_template('ratingProfessor.html')

#Ramon: Rating Course Page route
@app.route('/postCourse', methods=['GET', 'POST'])
def postCourse():
    if 'localId' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        userId = session['localId']
        title = request.form['title']
        content = request.form['content']
        take_again = request.form['take_again']
        difficulty = request.form['difficulty']
        homework = request.form['homework']
        course = request.form['course']
        rating = request.form['rating']
        post_id = uuid.uuid4().hex
        post = CoursePost(title, content, take_again, difficulty, homework, course, rating, post_id)
        
        db.collection('users').document(userId).update({
            'posts': firestore.ArrayUnion([post.__dict__])
        })
        postdata = {"post_id": "", "post_likes": "", "post_dislikes": ""}
        postdata["post_id"] = post_id
        postdata["post_likes"] = 0
        postdata["post_dislikes"] = 0
        db.collection('post_stats').document(post_id).set(postdata, merge = True) 

        userData = db.collection('user_post_ids').document(userId).get()
        user_post_id_list = userData.get('post_ids')
        if not isinstance(user_post_id_list, list):
            user_post_id_list = []
        user_post_id_list.append(post_id)
        db.collection('user_post_ids').document(userId).set({'post_ids': user_post_id_list}, merge = True)

        return redirect(url_for('home'))
    return render_template('ratingCourse.html')

#Ramon: Rating School Page route
@app.route('/postSchool', methods=['GET', 'POST'])
def postSchool():
    if 'localId' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        userId = session['localId']
        title = request.form['title']
        content = request.form['content']
        take_again = request.form['take_again']
        quality = request.form['quality']
        campus = request.form['campus']
        social = request.form['social']
        rating = request.form['rating']
        post_id = uuid.uuid4().hex
        post = SchoolPost(title, content, take_again, quality, campus, social, rating, post_id)
        
        db.collection('users').document(userId).update({
            'posts': firestore.ArrayUnion([post.__dict__])
        })
        postdata = {"post_id": "", "post_likes": "", "post_dislikes": ""}
        postdata["post_id"] = post_id
        postdata["post_likes"] = 0
        postdata["post_dislikes"] = 0
        db.collection('post_stats').document(post_id).set(postdata, merge = True)

        userData = db.collection('user_post_ids').document(userId).get()
        user_post_id_list = userData.get('post_ids')
        if not isinstance(user_post_id_list, list):
            user_post_id_list = []
        user_post_id_list.append(post_id)
        db.collection('user_post_ids').document(userId).set({'post_ids': user_post_id_list}, merge = True)

        return redirect(url_for('home'))
    return render_template('ratingSchool.html')

################################## End of RATING POSTS #####################################################################################################

# Start of Kenny's works #
######################################START of LOGIN ###############################################################################################################
#Kenny: handled all backend
#       handled login request and logic for already-sign-in
@app.route("/login", methods =["POST", "GET"])
def login():
    if ('user' in session): #if logged in, do this
        return redirect(url_for('home'))
    if request.method == 'POST': #if the form is submitted, perform this
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            #using pyrebase function, sign in with email and password
            user = auth.sign_in_with_email_and_password(email, password) #When this is sent and fail, it will raise the except statement below
            localId = user['localId']
            session['localId'] = localId
            session['user'] = email #create a session cookie
            session['username'] = db.collection('users').document(localId).get().to_dict()['username']
            return redirect(url_for('home'))
        except:
            return render_template("login.html")
            # return 'Failed to login' This would jut be a big page with small letters
    return render_template("login.html")

################################## END of LOGIN ############################################################################################################


#Kenny: handled all backend - START of SIGNUP ##############################################################################################################
#       handled registration rquest and database syncing 
@app.route("/signup", methods =["POST", "GET"])
def signup():
    if ('user' in session): #if logged in, do this
        return render_template("home.html")
    if request.method == 'POST': #if the form is submitted, perform this
        userdata = {"uid": "", "username": "", "email": "", "friends": "", "likes": "", "hate": "", "progress": "", "level": "", "desc": "", "post_ids": "", "posts": ""}
        username = request.form.get('username')
        
        email = request.form.get('email')
        password = request.form.get('password')
        confirmepassword = request.form.get('confirm')
        if (password != confirmepassword):
            return redirect(url_for('signup'))
        try:
            #using pyrebase function, create an account with email and password
            user = auth.create_user_with_email_and_password(email, password) #When this is sent and fail, it will raise the except statement below

            userdata["uid"] = user["localId"]
            userdata["username"] = username
            userdata["email"] = email
            userdata["likes"] = 0
            userdata["hate"] = 0
            userdata["progress"] = 0
            userdata["level"] = 0
            userdata["desc"] = "I love ClassSpace!"
            userdata["darkmode"] = False
            userdata["bg_color"] = "white"
            userdata["post_ids"] = ""
            userdata["posts"] = ""
            

            #append user information to firestore to store their username and etc.
            db.collection("users").document(userdata["uid"]).set(userdata, merge = True) 
            return redirect(url_for('login')) #go back to home page if success
        except:
            email_exist = "Please try a different email"
            return render_template("signUp.html", emailExist = email_exist)
    else:
        if ('user' in session): #if logged in, do this
            return redirect(url_for('home'))
        else:
            return render_template("signUp.html")
    
        
################################## END of SIGNUP#############################################################################################################

################################## START of FOLLOWERS ####################################################################################################

@app.route('/followers')
def followers():
    if 'user' in session:
        # get user and friend documents
        #Using a different way than Follow Functions to navigate the firestore db to get the ID
        userId = session.get('localId')
        userReference = db.collection('users').document(userId).get().to_dict()
        friendList = userReference['friends']

        friendNames = []
        for friend in friendList:
            fName = db.collection('users').document(friend).get().to_dict()['username']
            friendNames.append(fName)

        #Note the left side of a parameter is the variable will be use for the html
        return render_template("followers.html", friendNames = friendNames)
    
    # return redirect(url_for('login')) #uncomment in final
    return render_template("followers.html")             

#Problem: response don't have 'lat' or 'lon'
# Getting current location
@app.route('/map')
def map():
    # Render the map template with the list of schools and user's location
    return render_template('map.html')  

################################## END of FOLLOWER ##########################################################################################################
#End of Kenny's work #



################################## START of USERPROFILE #####################################################################################################

@app.route('/userprofile/')
def userprofile():
    #Check if user is logged in
    if 'user' in session:
    #Get the email address of the logged-in user from the session
        email = session['user']
        userId = session.get('localId')
    else:
        return render_template("login.html")
    #Get the user's document from the Firestore database using the email address
    userReference = db.collection('users').where('email', '==', email).limit(1)
    userDoc = userReference.get()[0].to_dict()
    
    # Get the user's name from the document


    #Done by Kenny
    #Used for the brief follower list on the side
    if 'user' in session:
        # get user and friend documents
        #Using a different way than Follow Functions to navigate the firestore db to get the ID
        userId = session.get('localId')
        userReference = db.collection('users').document(userId).get().to_dict()
        friendList = userReference['friends']

    userId = session.get('localId')
    userReference = db.collection('users').document(userId).get().to_dict()
    friendList = userReference['friends']

    friendNames = []
    for friend in friendList:
        fName = db.collection('users').document(friend).get().to_dict()['username']
        friendNames.append(fName)

    context = {
            "darkmode": userReference['darkmode'],
            "desc": userReference['desc']}
    
    #Ryan: Added to get user posts
    #Send to userprofile
    postlist = userReference['posts']
    if not isinstance(postlist, list):
        return render_template("userprofile.html", friendNames = friendNames, **context)

    
    return render_template("userprofile.html", friendNames = friendNames, urevs = postlist, **context)

################################## END of USERPROFILE #####################################################################################################

################################## START OF HELP ##########################################################################################################
@app.route('/help')
def help():
    return render_template('help.html')

################################## END of HELP ##############################################################################################################

################################## START OF NOTIFICATIONS ###################################################################################################

@app.route('/notifications')
def notifications():
    return render_template('notifications.html')

################################## END OF NOTIFICATIONS #####################################################################################################

################################## START of INBOX ###########################################################################################################
#Ramon: inbox.message system - I still can get messages to display
@app.route('/inbox', methods=['GET', 'POST'])
def inbox():
    if 'user' not in session:
        return redirect(url_for('login')) 
    # Retrieve messages from Firebase database
    messages = db.collection('messages').where('recipient', '==', session['user']).get()
    message_list = []
    for message in messages:
        message_dict = message.to_dict()
        message_dict['sender'] = db.collection('users').document(message_dict['sender']).get().to_dict()['username']
        message_dict['recipient'] = db.collection('users').document(message_dict['recipient']).get().to_dict()['username']
        message_dict['timestamp'] = message.id
        if message_dict:
            message_list.append(message_dict)
    # Render messages in HTML template
    return render_template('inbox.html', messages=message_list, user=session['user'])
    

@app.route('/send_message', methods=['POST'])
def send_message():
    if 'user' not in session:
        return redirect(url_for('login'))

    recipient_username = request.form['recipientUsername']
    message_text = request.form['messageText']

    # Add message to Firebase database with current timestamp
    timestamp = datetime.datetime.now().strftime('%a %b %d %I:%M %p')
    db.collection('messages').add({
        'text': message_text,
        'sender': session['username'],
        'recipient': recipient_username,
        'timestamp': timestamp
    })

    return render_template('inbox.html')

################################## END of INBOX #############################################################################################################


################################## START of PROFILE-SETTING #################################################################################################
#Kevin: Profile settings route
@app.route('/psettings', methods =["POST", "GET"])
def psettings():
    #I just leave this here to remind what I can access
    userdata = {"uid": "", "username": "", "email": "", "friends": "", "likes": "", "hate": "", "progress": "", "level": "", "desc": "", "darkmode": "", "bg_color": ""}
    if 'user' in session:
        # get user and friend documents
        userId = session.get('localId')
    else:
        return render_template("login.html")
    
    userId = session.get('localId')
    
    userReference = db.collection('users').document(userId)
    userReference = db.collection('users').document(userId).get().to_dict()
    
    user_name = userReference['username']
    user_email = userReference['email']
    user_desc = userReference['desc']
    user_darkmode = userReference['darkmode']
    #user_likes = userReference['likes']
    #user_hate = userReference['hate']
    #user_progress = userReference['progress']
    #user_level = userReference['level']
    
    
    old_user = request.form.get('old_user')
    new_user = request.form.get('new_user')
    
    verr_pass= request.form.get('verr_pass')
    
    #old_email = request.form.get('old_email')
    #new_email = request.form.get('new_email')
    
    new_desc = request.form.get('profile_desc')

    

    darkmodebutton = request.form.get('darkmodebutton')

    
       
    #db.collection('users').document(userId).set({'darkmode': darkmodebutton}, merge = True)
    
    if request.method == 'POST': #if the form is submitted, perform this
        #db.collection('users').document(userId).set({'darkmode': True}, merge = True)
        #changes for username
        if (darkmodebutton):
            if (user_darkmode == True):
                db.collection('users').document(userId).set({'darkmode': False}, merge = True)
                session['darkmode'] = False
            else:
                db.collection('users').document(userId).set({'darkmode': True}, merge = True)
                session['darkmode'] = True


        elif ( (user_name == old_user) & (user_name != "") & (old_user != "" ) ):

            try:
            #using pyrebase function, sign in with email and password
                user = auth.sign_in_with_email_and_password(user_email, verr_pass)
                db.collection('users').document(userId).set({'username': new_user}, merge = True)
                
                  #refreshes the session
                #localId = user['localId']
                #session['localId'] = localId
                session['user'] = user_email #create a session cookie
                session['username'] = new_user
            except:
                #return 'FAIL'
                return render_template('userprofilesettings.html')

        elif ( (user_desc != new_desc) & (new_desc != "") & (user_desc != "" )):

            db.collection('users').document(userId).set({'desc': new_desc}, merge = True)
            #localId = user['localId']
            #session['localId'] = localId
            session['user'] = user_email #create a session cookie
            session['username'] = user_name
            session['desc'] = "new_desc"
            db.collection('users').document(userId).set({'desc': new_desc}, merge = True)
            context = {
                "darkmode": userReference['darkmode'],
                "desc": userReference['desc']}
            
            return render_template('userprofilesettings.html', **context)
        #Does not work
        #elif ( (new_email== old_email) & (new_email != "") & (old_email != "" ) ):

            #try:
            #using pyrebase function, sign in with email and password
                #user = auth.sign_in_with_email_and_password(user_email, verr_pass)
                #db.collection('users').document(userId).set({'email': new_email}, merge = True)
                #user_update = auth.create_user_with_email_and_password(new_email, verr_pass)
                #I can't find the method for updating email
                #auth.delete_user_account(auth.current_user)
                #session.clear()
                #user = auth.create_user_with_email_and_password(new_email, verr_pass)  
                #userdata["uid"] = userId
                #userdata["username"] = user_name
                #userdata["email"] = new_email
                #userdata["likes"] = user_likes
                #userdata["hate"] = user_hate
                #userdata["progress"] = user_progress
                #userdata["level"] = user_level
                #userdata["desc"] = user_desc
                  #refreshes the session
                #db.collection("users").document(userdata["uid"]).set(userdata, merge = True) 
                
              
            #except:
                #return 'FAIL EMAIL'
                #return render_template('userprofilesettings.html')
            
    context = {
        "darkmode": userReference['darkmode'],
        "desc": userReference['desc']}
       
            


    return render_template('userprofilesettings.html', **context)

################################## END of PROFILE-SETTINGS ##################################################################################################

@app.route('/post_likes_add', methods =["POST", "GET"])
def post_likes_add():
#if request.method == 'POST':
    if 'user' in session:
            # get user and friend documents
            userId = session.get('localId')
    else:
        return render_template("login.html")

    userId = session['localId']
    user = db.collection('users').document(userId).get().to_dict()
    user_post_id_ref = db.collection('user_post_ids').document(userId).get()
    user_post_id_list = user_post_id_ref.get('post_ids')
    for posts in user_post_id_list:
        postReference = db.collection('post_stats').document(posts).get().to_dict()
        post_likes = postReference['post_likes']
        post_dislikes = postReference['post_dislikes']
        post_id = postReference['post_id']

        post_likes = post_likes+1
        db.collection('post_stats').document(post_id).set({'post_likes': post_likes}, merge = True)
        context = {
        "post_id" : post_id, 
        "post_likes": post_likes,
        "post_dislikes": post_dislikes,}


        posts = user.get('posts', [])
    return render_template("home.html", posts=posts, **context)

@app.route('/post_dislikes_add', methods =["POST", "GET"])
def post_dislikes_add():
#if request.method == 'POST':
    if 'user' in session:
            # get user and friend documents
            userId = session.get('localId')
    else:
        return render_template("login.html")

    userId = session['localId']
    user = db.collection('users').document(userId).get().to_dict()
    user_post_id_ref = db.collection('user_post_ids').document(userId).get()
    user_post_id_list = user_post_id_ref.get('post_ids')
    for posts in user_post_id_list:
        postReference = db.collection('post_stats').document(posts).get().to_dict()
        post_likes = postReference['post_likes']
        post_dislikes = postReference['post_dislikes']
        post_id = postReference['post_id']

        post_dislikes = post_dislikes + 1
        db.collection('post_stats').document(post_id).set({'post_likes': post_likes}, merge = True)
        context = {
        "post_id" : post_id, 
        "post_likes": post_likes,
        "post_dislikes": post_dislikes,}


        posts = user.get('posts', [])
    return render_template("home.html", posts=posts, **context)






################################## START of SEARCH for REVIEWS ##############################################################################################
#Ryan: Form for Search Reviews
class searchReview(FlaskForm):
    prof_rev = StringField("Search Professor", validators=[DataRequired()])
    submit = SubmitField("Submit")
#Ryan: Search Reviews
@app.route('/reviews', methods=["POST", "GET"])
def reviews():
    prof_rev = None
    prof = None
    rform = searchReview()
    if rform.validate_on_submit():
        prof_rev = rform.prof_rev.data
        rform.prof_rev.data = None

    #Checks if exists in firestore database
    #If exists, used database to get results
    check_db = db.collection(u'Professors').document(prof_rev).get()
    if check_db.exists:
        print("exists")
        revs = db.collection(u'Professors').document(prof_rev).collection(u'Reviews').stream()

        professor = Professors.from_dict(check_db.to_dict())
        #prof = Professors.from_dict(check_db.to_dict())
        print("sending reviews")
        #print(revs)
        revlist = []
        for doc in revs:
            rev = Reviews.from_dict(doc.to_dict())
            print(rev.Title)
            revlist.append(rev)
        return render_template('reviews.html', prof = prof_rev, revs = revlist, form = rform)

    return render_template('reviews.html', prof = "", form = rform)

################################## END of SEARCH for REVIEWS ###############################################################################################

################################## START of REWARDS PAGE ###################################################################################################
#Stuff for adding up likes and dislikes
#@author Kevin Cordray
@app.route('/rewardspage')
def rewardspage():
    from jinja2 import Environment, FileSystemLoader
    
    rewardsfile_name = "rewardspage.html"
    userdata = {"uid": "", "username": "", "email": "", "friends": "", "likes": "", "hate": "", "progress": "", "level": "", "desc": "", "darkmode": "", "bg_color": ""}
    
    if 'user' in session:
        # get user and friend documents
        #Using a different way than Follow Functions to navigate the firestore db to get the ID
        userId = session.get('localId')
        userReference = db.collection('users').document(userId).get().to_dict()
    

    userId = session.get('localId')
    userReference = db.collection('users').document(userId).get().to_dict()


    #get the likes stats through the database
    #FINALLY WORKS... FRICK YES
    user_likes = userReference['likes']
    user_hate = userReference['hate']
    user_progress = userReference['progress']
    user_progress = user_likes - user_hate
    user_level = userReference['level']
    max = 5
    if (user_progress >= 10):
        user_level = user_level + 1
        user_progress = user_progress - 10
    elif (user_progress < 0):
        user_level = user_level - 1
        user_progress = 0
    

    #user_progress = float(user_likes) - float(user_hate)
    #FINALLY WORKS... FRICK YES
    context = {
        "likes": user_likes,
        "hate": user_hate,
        "progress": user_progress,
        "level": user_level,}


    #testing stuff
    
    #user_progress.update({'progress': elem})
    print("test")

    return render_template('rewardspage.html', **context)

################################## END of REWARDS PAGE #####################################################################################################

################################## START of SEARCH #########################################################################################################

class searchForm(FlaskForm):
    school_name = StringField("Change School", validators=[DataRequired()])
    prof = StringField("Search Professor", validators=[DataRequired()])
    submit = SubmitField("Submit")


#Ryan - added routing for /search
#search.html will be able to use this data
@app.route('/search', methods = ["POST"])
def search():
    school_name = "California State University Long Beach"
    sform = searchForm()
    #Receives get request and uses it to search for professor
    searched = request.form.get('searched')
    
    if sform.validate_on_submit():
        school_name = sform.school_name.data
        searched = sform.prof.data
        print("changed: ", school_name)
        #form.school_name.data = "California State University Long Beach"
    print(searched)
    #Checks for valid search
    if searched != "" and searched != None:

        #Checks if exists in firestore database
        #If exists, used database to get results
        check_db = db.collection(u'Professors').document(searched).get()
        if check_db.exists:
            print("exists")
            professor = Professors.from_dict(check_db.to_dict())
            return render_template('search.html', name = professor.name, department = professor.department, school = professor.school,
                                        rating = professor.rating, difficulty = professor.difficulty, num_ratings = professor.num_ratings, 
                                        would_take_again =  professor.would_take_again, school_name = school_name, form = sform)

        #If professor is found
        if ratemyprofessor.get_professor_by_school_and_name(
            ratemyprofessor.get_school_by_name(school_name), searched) is not None:
            #Sets professor
            professor = ratemyprofessor.get_professor_by_school_and_name(
            ratemyprofessor.get_school_by_name(school_name), searched)
            #Adds professor to firestore database
            addProfessor(professor.name, professor.department, professor.school.name,
                                    professor.rating, professor.difficulty, professor.num_ratings, 
                                    round(professor.would_take_again, 1))
            #returns search page with results
            return render_template('search.html', name = professor.name, department = professor.department, school = professor.school.name,
                                    rating = professor.rating, difficulty = professor.difficulty, num_ratings = professor.num_ratings, 
                                    would_take_again =  round(professor.would_take_again, 1), school_name = school_name, form = sform)
        else: 
            return render_template('search.html', name = "", school_name = school_name, form = sform)
    else:
        return render_template('search.html', name = "", school_name = school_name, form = sform)
    
################################## END of SEARCH ###########################################################################################################

################################## START OF LOGOUT #########################################################################################################
#Kenny: implemented logout function
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

################################## END OF LOGOUT ###########################################################################################################

if __name__ == '__main__':
    app.run(debug=True)





    



    





