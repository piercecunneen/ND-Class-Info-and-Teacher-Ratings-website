#databaseFunctions.py
#functions to deal with saving/retrieving reviews

import sqlite3 as lite
import sys
from class_search_web_scrapping import Sort_dict

database = 'reviews.sqlite'

def addProfReview(lastName, firstName, review, workload, grading, quality, accessibility,syllabus, department):
    data = [lastName, firstName, review, workload, grading, quality, accessibility,syllabus, department]
    
    conn = lite.connect(database)
    with conn:
    
        c = conn.cursor()
        c.executemany('INSERT INTO profReview VALUES(?,?,?,?,?,?,?,?,?)',(data,))
        #conn.close()
        
def addClassReview(lastName, firstName, title, review, toughness, interest, textbook, department):
    data = [lastName, firstName, title, review, toughness, interest, textbook, department]
    conn = lite.connect(database)
    with conn:
        c = conn.cursor()    
        c.executemany('INSERT INTO classReview VALUES(?,?,?,?,?,?,?,?)',(data,))

def getProfReviews(lastName, firstName, department, college):
    if lastName != "":
        # pull list of professors by last name
        
        conn = lite.connect(database)
        with conn:
            c = conn.cursor()
            c.execute("SELECT * FROM profReview WHERE LastName=:last AND FirstName=:first", {"last":lastName, "first":firstName})
            profReviews = c.fetchall()
            return profReviews
            
    if department != "":
        #pull prof list by department
        conn = lite.connect(database)
        with conn:
            c = conn.cursor()
            c.execute("SELECT * FROM profReview WHERE Department=:dept", {"dept":department})
            profReviews = c.fetchall()
            return profReviews
        
    if college != "":
        #pull prof list by college
        x = 1  
        
        
def getClassReviews(department, title):
    #pull reviews by department
    if department != "":
        conn = lite.connect(database)
        with conn:
            c = conn.cursor()
            c.execute("SELECT * FROM classReview WHERE Department=:dept", {"dept":department})
            classList = c.fetchall()
            return classList
    else:
        conn = lite.connect(database)
        with conn:
            c = conn.cursor()
            c.execute("SELECT * FROM classReview WHERE Title=:title", {"title":title})
            classList = c.fetchall()
            return classList
    
    
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
    
        review = [profReviews[0][0], profReviews[0][1], profReviews[0][2], workloadTotal, gradingTotal, qualityTotal, accessiblityTotal, syllabusTotal]
        return review
    
def calculateClassRatings(classReviews):
    i = len(classReviews)
    if (i == 0):
        return ["","","","","","",""] #change if number of categories change
    else:
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
            
        toughnessTotal /= i
        interestTotal /= i
        textbookTotal /= i
        review = [classReviews[0][0], classReviews[0][1], classReviews[0][2],  toughnessTotal, interestTotal, textbookTotal]
        return review
    
def bestProf(department):
    #a = calculateProfRatings(getProfReviews("", "", department, ""))
    #return a
    profList = getProfReviews("","", department, "")
    profs = []
    for prof in profList:
        if prof not in profs:
            # change to add only names
            profs.append(prof)
    
    
    # get each prof overall rating into dictionary, with key being the name
    profDict = {}
    num_profs = len(profs)
    profRating = [] * num_profs
    for j in range(0, num_profs):
        profFirst = profs[j][1]
        profLast = profs[j][0]
        profName = profLast +  profFirst
        profRatingList = calculateProfRatings(getProfReviews(profLast, profFirst, "", ""))
        profRating = profRatingList[3]
        profDict[profName] = profRating
    profDictSorted = Sort_dict(profDict, 1)
   
    return profDict, profDictSorted
   
def easiestProf(department):
    #a = calculateProfRatings(getProfReviews("", "", department, ""))
    #return a
    profList = getProfReviews("","", department, "")
    profs = []
    for prof in profList:
        if prof not in profs:
            # change to add only names
            profs.append(prof)
    
    workload_index = 3
    # get each prof overall rating into dictionary, with key being the name
    profDict = {}
    num_profs = len(profs)
    profRating = [] * num_profs
    for j in range(0, num_profs):
        profFirst = profs[j][1]
        profLast = profs[j][0]
        profName = profLast +  profFirst
        profRatingList = calculateProfRatings(getProfReviews(profLast, profFirst, "", ""))
        profRating = profRatingList[workload_index]
        profDict[profName] = profRating
    profDictSorted = Sort_dict(profDict, 1)
   
    return profDict, profDictSorted
   
    
def bestClass(department):
    courseList = getClassReviews(department, "")
    courses = []
    for course in courseList:
        if course not in courses:
            # change to add only names
            courses.append(course)
    
    rating_index = 3
    # get each prof overall rating into dictionary, with key being the name
    courseDict = {}
    num_courses = len(courses)
    courseRating = [] * num_courses
    for j in range(0, num_courses):
        courseName = courses[j][2]
        courseRatingList = calculateClassRatings(getClassReviews(department,""))
        courseRating = courseRatingList[rating_index]
        courseDict[courseName] = courseRating
    courseDictSorted = Sort_dict(courseDict, 1)
   
    return courseDict, courseDictSorted
    
def easiestClass(department):
    courseList = getClassReviews(department, "")
    courses = []
    for course in courseList:
        if course not in courses:
            # change to add only names
            courses.append(course)
    
    workload_index = 3
    # get each prof overall rating into dictionary, with key being the name
    courseDict = {}
    num_courses = len(courses)
    courseRating = [] * num_courses
    for j in range(0, num_courses):
        courseName = courses[j][2]
        courseRatingList = calculateClassRatings(getClassReviews(department,""))
        courseRating = courseRatingList[workload_index]
        courseDict[courseName] = courseRating
    courseDictSorted = Sort_dict(courseDict, 1)
   
    return courseDict, courseDictSorted