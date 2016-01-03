#databaseFunctions.py
#functions to deal with saving/retrieving reviews

import sqlite3 as lite
from class_search_web_scrapping import Sort_dict, GetAllProfessors
from Get_Sorted_CRNs import Get_CRN_List, is_Valid

database = 'reviews.sqlite'

def addNumber(number, crn):
	""" Watches the crn @crn
		 for phone number @number
	"""
	data = [crn, number, 0]
	conn = lite.connect(database)
	with conn:
		c = conn.cursor()
		c.executemany('INSERT INTO textAlerts VALUES(?,?,?)', (data,))
		print "Inserted phone number and crn into database"

def addProfReview(lastName, firstName, review, workload, grading, quality, accessibility, syllabus, department, id, username, submit_date):
    # department comes in as list, needs to be changed to string
    if len(department) > 1:
        department = ' '.join(department)
    else:
        department = department[0]
    data = [lastName, firstName, review, workload, grading, quality, accessibility,syllabus, department, id, username, submit_date]
    conn = lite.connect(database)
    with conn:
        c = conn.cursor()
        c.executemany('INSERT INTO profReview VALUES(?,?,?,?,?,?,?,?,?,?,?,?)',(data,))
        #conn.close()
        
def addClassReview(lastName, firstName, title, review, toughness, interest, textbook, department, crn, date, id, username, submit_date):
    if len(department) > 1:
        department = ' '.join(department)
    else:
        department = department[0]
    data = [lastName, firstName, title, review, toughness, interest, textbook, department, crn, date, id, username, submit_date]
    conn = lite.connect(database)
    with conn:
        c = conn.cursor()    
        c.executemany('INSERT INTO classReview VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)',(data,))

def getProfReviews(id):
    '''if lastName != "":
        # pull list of professors by last name
        conn = lite.connect(database)
        with conn:
            c = conn.cursor()
            query = 'SELECT * FROM profReview WHERE LastName = "' + lastName + '" AND FirstName = "' + firstName + '"'
            c.execute(query)
            profReviews = c.fetchall()
            return profReviews
            
    if department != "":
        #pull prof list by department
        conn = lite.connect(database)
        with conn:
            c = conn.cursor()
            query = 'SELECT * FROM profReview WHERE Department LIKE "%' + department + '%"'
            c.execute(query)
            profReviews = c.fetchall()
            return profReviews    '''    
        
    conn = lite.connect(database)
    with conn:
        c = conn.cursor()
        query = 'SELECT * FROM profReview WHERE ID = ' + str(id) 
        c.execute(query)
        profReviews = c.fetchall()
        return profReviews

def getDepartmentReviews(department):
    conn = lite.connect(database)
    with conn:
        c = conn.cursor()
        query = 'SELECT * FROM profReview WHERE Department = "' + department + '"'
        c.execute(query)
        profReviews = c.fetchall()
        return profReviews    

def getClassReviews(department, title):
    #pull reviews by department
    if department != "":
        conn = lite.connect(database)
        with conn:
            c = conn.cursor()
            query = 'SELECT * FROM classReview WHERE Department = "' + department + '"'
            c.execute(query)
            classList = c.fetchall()
            return [classList, "department"]
    else:
        conn = lite.connect(database)
        with conn:
            c = conn.cursor()
            query = 'SELECT * FROM classReview WHERE Title = "' + title + '"'
            c.execute(query)
            classList = c.fetchall()
            return [classList, "title"]
    
# REFACTOR HERE    
    
def calculateProfRatings(profReviews): #must pull profReviews by name, not department or college 
    i = len(profReviews)
    if (i == 0):
        return ["","","","","","","",""] #change if number of categories change
    else: 
        workload = [0] * i
        grading = [0] * i
        quality = [0] * i
        accessiblity = [0] * i
        syllabus = [0] * i
        for j in range(0,i):
            workload[j] = profReviews[j][3]
            grading[j] = profReviews[j][4]
            quality[j] = profReviews[j][5]
            accessiblity[j] = profReviews[j][6]
            syllabus[j] = profReviews[j][7]
        
        workloadTotal = 0
        gradingTotal = 0 
        qualityTotal = 0
        accessiblityTotal = 0
        syllabusTotal = 0
        
        for k in range(0,i):
            workloadTotal += workload[k]
            gradingTotal += grading[k]
            qualityTotal += quality[k]
            accessiblityTotal += accessiblity[k]
            syllabusTotal += syllabus[k]
    
        workloadTotal /= float(i)
        gradingTotal /= float(i)
        qualityTotal /= float(i)
        accessiblityTotal /= float(i)
        syllabusTotal /= float(i)
        
        last_name = profReviews[0][0]
        first_name = profReviews[0][1]
        review = profReviews[0][2]

        review = [last_name, first_name, review, workloadTotal, gradingTotal, qualityTotal, accessiblityTotal, syllabusTotal]
        return review

# REFACTOR HERE

def calculateClassRatings(classReviews):
    i = len(classReviews[0])
    if (i == 0):
        return ["","","","","","",""] #change if number of categories change
    elif classReviews[1]=="title":
        classReviews = classReviews[0] # destroy weird indexing
        i = len(classReviews)
        toughness = [0] * i
        interest = [0] * i
        textbook = [0] * i
        for j in range(0,i):
            toughness[j] = classReviews[j][4]
            interest[j] = classReviews[j][5]
            textbook[j] = classReviews[j][6]   
        toughnessTotal = 0
        interestTotal = 0
        textbookTotal = 0
        for k in range(0,i):
            toughnessTotal += toughness[k]
            interestTotal += interest[k]
            textbookTotal += textbook[k]
            
        toughnessTotal /= float(i)
        interestTotal /= float(i)
        textbookTotal /= float(i)
        last_name = classReviews[0][0]
        first_name = classReviews[0][1]
        title = classReviews[0][2]
        crn = classReviews[0][8]
        date = classReviews[0][9]
        review = [last_name, first_name, title, toughnessTotal, interestTotal, textbookTotal, crn, date]
        return review
        
    elif classReviews[1] == "department": 
        # get number of different courses then run calculateClassRatings() for each different course title
        course_title_list = [] #* len(classReviews[0])
        for i in range(0,len(classReviews[0]) + 1):
            title = classReviews[0][i][2]
            if title not in course_title_list:
                course_title_list.append(title)
        classReviews = [] #* len(course_title_list)
        for i in range(0, len(course_title_list)):
            classReviews.append(calculateClassRatings(getClassReviews("",course_title_list[i])))    
        return classReviews
    
def bestProf(department):
    profList = getDepartmentReviews(department)
    professors = GetAllProfessors()
    profs = []

    profIDs = {}
    for prof in profList:
        if professors[prof[0] + prof[1]] not in profIDs:
            profs.append(prof)
            profIDs[professors[prof[0] + prof[1]]] = 1
        
    workload_index = 3
    grading_index = 4
    quality_index = 5
    # get each prof overall rating into dictionary, with key being the name
    profDict = {}
    num_profs = len(profs)
    profRating = [] * num_profs
    for j in range(0, num_profs):
        profFirst = profs[j][1]
        profLast = profs[j][0]
        profName = profLast +  profFirst
        # need to get prof ID
        id = professors[profName]
        profRatingList = calculateProfRatings(getProfReviews(id))

        # Average of workload, grading, and quality
        profRating = round(profRatingList[quality_index],2)
        profDict[profName] = profRating
    profDictSorted = Sort_dict(profDict, 1)
   
    return profDict, profDictSorted
   
def easiestProf(department):
    #a = calculateProfRatings(getProfReviews("", "", department, ""))
    #return a
    profList = getDepartmentReviews(department)
    profs = []
    profIDs = {}
    professors = GetAllProfessors()
    for prof in profList:
        if professors[prof[0] + prof[1]] not in profIDs:
            profs.append(prof)
            profIDs[professors[prof[0] + prof[1]]] = 1
    workload_index = 3
    grading_index = 4
    # get each prof overall rating into dictionary, with key being the name
    profDict = {}
    num_profs = len(profs)
    profRating = [] * num_profs
    for j in range(0, num_profs):
        profFirst = profs[j][1]
        profLast = profs[j][0]
        profName = profLast +  profFirst
        id = professors[profName]
        profRatingList = calculateProfRatings(getProfReviews(id))

        # Average of workload and grading
        profRating = round((profRatingList[workload_index] + profRatingList[grading_index])/2.0,2)
        profDict[profName] = profRating
    profDictSorted = Sort_dict(profDict, 1)
   
    return profDict, profDictSorted
   
    
def bestClass(department):
    courseList = getClassReviews(department, "")
    courses = set([course[2] for course in courseList[0]])
    courses = list(courses)
    crn_index = 6
    date_index = 7
    
    toughness_index = 3
    interest_index = 4



    # get each prof overall rating into dictionary, with key being the name
    courseDict = {}
    num_courses = len(courses)
    courseRating = [] * num_courses
    for j in range(0, num_courses):
        courseName = courses[j]
        courseRatingList = calculateClassRatings(getClassReviews("",str(courseName)))

        # Best determiend by average of toughess and interest
        courseRating = [round((courseRatingList[toughness_index] + courseRatingList[interest_index])/2.0,2), int(courseRatingList[crn_index]), int(courseRatingList[date_index])]
        courseDict[courseName] = courseRating 
    courseDictSorted = Sort_dict(courseDict, 1)
   
    return courseDict, courseDictSorted
    
def easiestClass(department):
    courseList = getClassReviews(department, "")
    courses = set([course[2] for course in courseList[0]])
    courses = list(courses)
    crn_index = 6
    date_index = 7
    toughness_index = 3
    # get each prof overall rating into dictionary, with key being the name
    courseDict = {}
    num_courses = len(courses)
    courseRating = [] * num_courses
    for j in range(0, num_courses):
        courseName = courses[j]
        courseRatingList = calculateClassRatings(getClassReviews("", str(courseName)))
        courseRating = [round(courseRatingList[toughness_index],2), int(courseRatingList[crn_index]), int(courseRatingList[date_index])]
        courseDict[courseName] = courseRating
    courseDictSorted = Sort_dict(courseDict, 1)
   
    return courseDict, courseDictSorted

def getPosts():
    conn = lite.connect(database)
    with conn:
        c = conn.cursor()
        query = "SELECT * FROM posts"
        c.execute(query)
        posts = c.fetchall()
    return posts
    


def get_random_prof():
    conn = lite.connect(database)
    with conn:
        c = conn.cursor()
        query = 'SELECT * FROM profReview ORDER BY RANDOM() LIMIT 1'
        c.execute(query)
        random_prof = c.fetchall()[0]
        prof_id = random_prof[9]
        Prof_reviews = getProfReviews(prof_id)
        Prof_ratings = calculateProfRatings(Prof_reviews)
        return Prof_ratings

def count_reviews():
    conn = lite.connect(database)
    with conn:
        c = conn.cursor()
        query = 'SELECT COUNT(*) from profReview'
        c.execute(query)
        a = c.fetchone()
        query = 'SELECT COUNT(*) from classReview'
        c.execute(query)
        b = c.fetchone()
    return a[0] + b[0]
<<<<<<< HEAD

def recentReviews():
    conn = lite.connect(database)
    with conn:
        c = conn.cursor()
        query = 'SELECT * FROM profReview ORDER BY submit_date DESC LIMIT 5'
        c.execute(query)
	reviews = c.fetchall()
        return reviews
    

=======
>>>>>>> upstream/master

def recentReviews():
    conn = lite.connect(database)
    with conn:
        c = conn.cursor()
        query = 'SELECT * FROM profReview ORDER BY submit_date DESC LIMIT 5'
        c.execute(query)
	reviews = c.fetchall()
        return reviews
