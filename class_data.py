#class_data.py
#this file creates the original class data base by pulling all of the class info from 
#class search and will be updated daily

import sqlite3 
import os.path
from class_search_web_scrapping import GetOptions, GetClasses

#test for existence of database, and create it if it doesn't exist

sqlite_file = 'class_dat.sqlite'
x = os.path.isfile(sqlite_file);
print x
table='class_data'
cType = 'TEXT'

def createAndPopulate():
    #connect to database file
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    #create table
    c.execute("CREATE TABLE class_data(a TEXT b TEXT c TEXT d TEXT e TEXT f TEXT g TEXT h TEXT i TEXT j TEXT k TEXT l TEXT m TEXT n TEXT o TEXT p TEXT q TEXT)")
    #columns will be from list of courseInfo. parameters are arbitrary and only used to make function run properly
    courseInfo = GetClasses('201510', 'ACCT', 'A', '0ANY', 'A','M')[0].keys()
    
    for i in range(0,(len(courseInfo) - 1)):
        c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
            .format(tn=table, cn=courseInfo[i], ct=cType))
    
    #populate table with all available classes
    termOptions = GetOptions()[0].values()
    print termOptions
    divOptions = GetOptions()[1].values()
    campusOptions = GetOptions()[2].values()
    subjectOptions = GetOptions()[3].values()
    attrOptions = GetOptions()[4].values()
    creditOptions = GetOptions()[5].values()
    #GetClasses(term, subj, credit, Attr, divs, campus):
    classList = GetClasses(termOptions, subjectOptions,creditOptions, attrOptions, divOptions, campusOptions)
    #databaseInfo = classList.values()
    print len(classList)
    i = 0
    print classList[i].values()
    x = classList[i].values()
    print x[0]
    print classList
    for i in range(0,len(classList)/17):  
        j = 1 
        x = classList[i].values() 
        print x
        c.executemany("INSERT INTO class_data VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (x,))
        j+=1
        
    
if x == False:
    createAndPopulate()