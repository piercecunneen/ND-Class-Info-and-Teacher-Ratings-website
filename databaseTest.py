import sqlite3
import os.path


sqlite_file = 'review.sqlite'
x = os.path.isfile(sqlite_file);
print x
x = True

reviewData = 'reviewData'
columnOne = 'Last Name'
type = 'TEXT'

if x == True:
    # connect to database file
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()

    # creating a new SQLite table with 1 column
    c.execute('CREATE TABLE {tn} ({nf} {ft})'\
            .format(tn=reviewData, nf=columnOne, ft=type))
    
    # add columns
    columnList = ['First Name', 'Review', 'Workload', 'Grading', 'Quality', 'Accessiblility', 'Syllabus']
    
    for listItem in columnList:
        print listItem
        c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
            .format(tn=reviewData, cn=listItem, ct=type))


    print 'database created successfully exists' 
    # Committing changes and closing the connection to the database file
    conn.commit()
    conn.close()
    
