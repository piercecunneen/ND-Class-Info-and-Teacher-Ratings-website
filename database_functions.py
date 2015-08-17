#databaseFunctions.py
#functions to deal with saving/retrieving reviews

import sqlite3 as lite
import sys


database = 'reviews.sqlite'

def addReview(lastName, firstName, review, workload, grading, quality, accessibility, syllabus):
    data = [lastName, firstName, review, workload, grading, quality, accessibility, syllabus]
    
    conn = lite.connect(database)
    with conn:
    
        c = conn.cursor()
        c.executemany('INSERT INTO reviewTable VALUES(?,?,?,?,?,?,?,?)',(data,))
        #conn.close()
        
def getProfList():
    #something
    x = 1