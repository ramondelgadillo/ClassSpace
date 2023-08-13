

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import ratemyprofessor

# we're using this file as a placeholder for now, not planning to use it long term
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

########################## Professor Class #############################################
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
############################### end of Professor Class ##########################################
########################## Review Class #############################################
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

#Ryan: def to addProfessor to database
def addReview(prof, Title, Review, Difficulty, Rating, Would_take_again):
    rev = Reviews(Title=Title, Review=Review, Difficulty=Difficulty,
                  Rating=Rating, Would_take_again=Would_take_again)
    db.collection(u'Professors').document(prof).collection(u'Reviews').document(rev.Title).set(rev.to_dict())
############################### end of Review Class ##########################################


#lst = ratemyprofessor.get_school_by_name("California State University Long Beach")

#print(lst.name)
#lst = ratemyprofessor.get_professors_by_school_and_name(ratemyprofessor.get_school_by_name
#                                                                   ("California State University Long Beach"), "Gold")

#for i in lst:
#    print(i.name)

#sc = ratemyprofessor.get_schools_by_name("California State University Long Beach")

#for i in sc:
#    print(i.name)


#prof = Professors(name=u'Professor Tester', department=u'Engineering', school=u'California State University Long Beach', 
#                  rating=u'4.0', difficulty=u'3.0', num_ratings=u'15', would_take_again=u'96')
#db.collection(u'Professors').document(u'Professor Tester').set(prof.to_dict())



addReview("Dave Winter", "Test2", "Very very good", 3, 5, True)
    
























#Modifies school for search --Ryan
#@app.route('/msearch')
#def msearch():
#    searchschool = ratemyprofessor.get_school_by_name(request.args.get('searchschool'))
#    print("search = ", searchschool.name)
#    if searchschool.name != None:
#        print("school changed")
#        school_name = request.args.get('searchschool')
#        
#    else:
#        school_name = "California State University Long Beach"
#    school_name = searchschool.name
#    print("school name is ", school_name)
#    return render_template('search.html', school_name = school_name)





#professor = ratemyprofessor.get_professor_by_school_and_name(
#    ratemyprofessor.get_school_by_name("California State University Long Beach"), "Fei Hoffman")
#if professor is not None:
#    print("%s works in the %s Department of %s." % (professor.name, professor.department, professor.school.name))
#    print("Rating: %s / 5.0" % professor.rating)
#    print("Difficulty: %s / 5.0" % professor.difficulty)
#    print("Total Ratings: %s" % professor.num_ratings)
#    if professor.would_take_again is not None:
#        print(("Would Take Again: %s" % round(professor.would_take_again, 1)) + '%')
#    else:
#        print("Would Take Again: N/A")




#db = firestore.client()
#data = {'name': 'Ryan'}
#db.collection('persons').add(data) #use this to auto generate ID
#db.collection('persons').document("Ryan's").set(data) #set ID 

# Read file/documents with known ID
#result = db.collection('persons').document("Ryan's").get()
#if result.exists:
#    print(result.to_dict())

# get all document in the collection


#obj1 = {
#    'Name' : 'Mike',
#    'Rating' : 3
#}

#obj2 = {
#    'Name' : 'John',
#    'Rating' : 4
#}

#professors = [obj1, obj2]

# Iterate over professors
#for professor in professors:
#  professor_data = {
#    'Name': professor['Name'],
#    'AvgRating': professor['AvgRating']
#  }

# Iterate over professors
#for professor in professors:
    # Add professor to firestore
#    doc_ref = db.collection(u'Professors').document(professor['Name']) #, professor['AvgRating'])
#    doc_ref.set(professor)


#uci = "1074"

#def test_init_ratemyprof():
#    api = RateMyProfApi(uci, testing = True)

#illiamPatersonUniversity = RateMyProfApi(1205) #WPUNJ Object
#MassInstTech = RateMyProfApi(580)   #MIT Object

#WilliamPatersonUniversity.SearchProfessor("Cyril Ku")  