#databaseFunctions.py
#functions to deal with saving/retrieving reviews

import sqlite3 as lite
import sys


database = 'reviews.sqlite'

def addProfReview(lastName, firstName, review, workload, grading, quality, accessibility, department):
    data = [lastName, firstName, review, workload, grading, quality, accessibility, department]
    
    conn = lite.connect(database)
    with conn:
    
        c = conn.cursor()
        c.executemany('INSERT INTO reviewTable VALUES(?,?,?,?,?,?,?,?)',(data,))
        #conn.close()
        
def addClassReview(lastName, firstName, title, review, toughness, interest, textbook, syllabus, department):
    data = [lastName, firstName, title, review, toughness, interest, textbook, syllabus, department]
    conn = lite.connect(database)
    with conn:
        c = conn.cursor()    
        c.executemany('INSERT INTO classReviewTable VALUES(?,?,?,?,?,?,?,?)',(data,))

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
        
        
def getClassReview(department):
    #pull reviews by department
    conn = lite.connect(database)
    with conn:
        c = conn.cursor()
        c.execute("SELECT * FROM classReview WHERE Department=:dept", {"dept":department})
        classList = c.fetchall()
        return classList
    
    
def calculateProfRatings(profReviews): 
    i = len(profReviews)
    print i
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
    
    workloadt = 0
    gradingt = 0 
    qualityt = 0
    accessiblityt = 0
    syllabust = 0
    
    for k in range(0,i):
        workloadt += workload[k]
        gradingt += grading[k]
        qualityt += quality[k]
        accessiblityt += accessiblity[k]
        syllabust += syllabus[k]
        
    workloadt /= i
    gradingt /= i
    qualityt /= i
    accessiblityt /= i
    syllabust /= i
    
    review = [profReviews[0][0], profReviews[0][1], profReviews[0][2], workloadt, gradingt, qualityt, accessiblityt, syllabust]
    return review
    
def calculateClassRatings(classReviews):
    i = len(classReviews)
    toughness = [0] * i
    interest = [0] * i
    textbook = [0] * i
    syllabus = [0] * i
    for j in range(0,i):
        toughness[j] = classReviews[j][3]
        interest[j] = classReviews[j][4]
        textbook[j] = classReviews[j][5]
        syllabus[j] = syllabus[j][6]
        
    toughnesst = 0
    interestt = 0
    textbookt = 0
    syllabust = 0
    
    for k in range(0,i):
        toughnesst += toughness[k]
        interestt += interest[k]
        textbookt += textbook[k]
        syllabust += syllabus[k]
        
    toughnesst /= i
    interestt /= i
    textbookt /= i
    syllabust /= i
    review = [classReviews[0][0], classReviews[0][1], classReviews[0][2],  toughnesst, interestt, textbookt, syllabust]
    return review
    
def bestProf(department):
    #a = calculateProfRatings(getProfReviews("", "", department, ""))
    #return a
    x = 1  
def easiestProf(review):
    x=1
   
    
def bestClass(review):
    x = 1
    
def easiestClass(review):
    x =1