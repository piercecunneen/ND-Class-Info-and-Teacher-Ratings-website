import requests
from bs4 import BeautifulSoup
from class_search_web_scrapping import  GetOptions, GetClasses
import time

# Returns a list that is redonk large. Use Write_Courses_iter to return a generator with smaller pieces
def Write_Courses():
	Options = GetOptions()
	subjects = Options[3].values()
	term = "201520"
	ATTR = '0ANY'
	Division = "UG"
	Campus = "M"
	Credit = "A"
	Courses = GetClasses(term, subjects, Credit, ATTR, Division, Campus)
	return Courses

def Write_Courses_iter():
	Options = GetOptions()
	subjects = Options[3].values()
	term = "201520"
	ATTR = '0ANY'
	Division = "UG"
	Campus = "M"
	Credit = "A"
	for subject in subjects:
		Courses = GetClasses(term, subject, Credit, ATTR, Division, Campus)
		yield Courses
	
def Get_CRN_List():
	crn_list = []
	with open('/home/flask/class_text/sorted_CRNs.txt', "r") as f:
		crn_list = f.read().split("\n")
	while crn_list[-1] == "":
		crn_list.pop()
	return [i for i in crn_list]

# def Get_Crns():
# 	Courses = Write_Courses_iter()
# 	CRNs = {}
# 	Sorted_Crns = []

# 	for course in Courses:
# 		CRNs[course["CRN"]] = course["Title"] + "|" + course["Course - Sec"] + "|" + course["CRN"] + "|" + course["Opn"]
	
# 	Sorted_Crns = sorted(CRNs.keys())
# 	return Sorted_Crns, CRNs


# Performs a binary search for value in CRN_Numbers
# returns a department if the crn value was found that cooresponds to the crn
# returns false if value not in CRN_Numbers
def is_Valid(value, CRN_Numbers):
	start = 0
	end = len(CRN_Numbers) - 1
	middle = (end) / 2

	while start <= end:
		middle_value = int(CRN_Numbers[middle].split(" ")[0])
		if middle_value > value:
			end = middle - 1
			middle = (start + end) / 2
		elif middle_value < value:
			start = middle + 1
			middle = (start + end) / 2
		else:
			return CRN_Numbers[middle].split(" ")[1]
	return False

