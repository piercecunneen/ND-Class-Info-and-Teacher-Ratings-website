#!/usr/bin/python

'''
This file is for emailing someone when a spot opens in a class they are watching
'''

import smtplib
from class_search_web_scrapping import GetClasses, GetCurrentSemester

crn = '24680'
openSpots = 0
courseName = 'Unamed Course'
classes = GetClasses(GetCurrentSemester(), "CSE", "A", "0ANY", "A", "M")
for course in classes:
	if course['CRN'] == crn:
		openSpots = course['Opn']
		courseName = course['Title']

if int(openSpots) > 0:
	sender = 'DO-NOT-REPLY@ndreviews.com'
	receivers = ['dmattia@nd.edu', 'david.j.mattia.2@nd.edu']
	subject = 'A spot has opened up!'
	body = "A spot has recently opened up in a class you are watching on ndreviews.com\n\
The course %s now has %s open spots\n\
\n\
Good luck NOVOing as quick as you can!\n\
-ndreviews staff" % (courseName, openSpots)
	
	for recipient in receivers:
		message = """\
from: %s
to: %s
subject: %s

%s
""" % (sender, recipient, subject, body)
	
		smtpObj = smtplib.SMTP('localhost')
		smtpObj.sendmail(sender, receivers, message)         
	print "Spots are now open. Email sent."
else:
	print "No spots open. No email sent."
