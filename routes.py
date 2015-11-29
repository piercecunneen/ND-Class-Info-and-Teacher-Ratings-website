from flask import Flask, render_template, request, jsonify
from class_search_web_scrapping import GetCoursesTaught,GetAllProfessors, GetOptions, Sort_dict, GetClasses, GetSubjectsInDepartments, GetClassDescriptionAndAll, GetAllProfessorDepartments
from database_functions import easiestClass, bestClass, easiestProf,bestProf,getClassReviews, getProfReviews, addClassReview, addProfReview, calculateProfRatings, calculateClassRatings

app = Flask(__name__)


Options = GetOptions()

Professors = GetAllProfessors()
ProfDepartments = GetAllProfessorDepartments()

def GetCurrentSemester():
    return '201520' 

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/class_search/quick-search=<ATTR>', methods = ["POST", "GET"])
def QuickSearch(ATTR):
    if request.method == "POST":
        Term = request.form['TermOptions']
        Subject = request.form.getlist('SubjectOptions')
        Credit = request.form['CreditsOptions']
        Attribute = request.form['AttributeOptions']
        Division = request.form['DivisionOptions']
        Campus = request.form['CampusOptions']
        return DisplayClasses(Term, Subject, Credit, Attribute, Division, Campus)
    Attributes = {'2nd Theology':'THE2', '2nd Philosophy':'PHI2', 'Social Science': 'SOSC',  'Natural Science (req)': 'NASC', 'Fine Arts':'FNAR', 'Literature':'LIT', 'History': 'HIST'}
    Subjects = Options[3].values()
    Semester = GetCurrentSemester()
    Attribute = Attributes[ATTR]
    return DisplayClasses(Semester, Subjects, Options[5]["All"],Attribute,"A", Options[2]["Main"])


@app.route('/search/<query>/', methods = ['POST'])
def Search(query):
	unicode_profs = {} 
	for prof in Professors:
		prof_name = unicode(prof, "utf-8")
		if query.lower() in prof_name.lower():
			unicode_profs[prof_name] = '/instructor_info/' + prof_name
	return jsonify(unicode_profs)

@app.route('/class_search/', methods = ['GET', 'POST'])
def ClassSearch():
    if request.method == 'POST':
        Term = request.form['TermOptions']
        Subject = request.form.getlist('SubjectOptions')
        Credit = request.form['CreditsOptions']
        Attribute = request.form['AttributeOptions']
        Division = request.form['DivisionOptions']
        Campus = request.form['CampusOptions']

         
        return DisplayClasses(Term, Subject, Credit, Attribute, Division, Campus)
    return render_template('class_search.html', TermOptionKeys = Sort_dict(Options[0], True), TermOptions = Options[0] , 
    DivisionOptionKeys = Sort_dict(Options[1], False), DivisionOptions = Options[1],
    CampusOptionKeys = Sort_dict(Options[2], False), CampusOptions = Options[2], 
    SubjectOptionKeys = Sort_dict(Options[3], False), SubjectOptions =  Options[3], 
    AttributeOptionKeys = Sort_dict(Options[4], False), AttributeOptions = Options[4],
    CreditsOptionKeys = Sort_dict(Options[5], False), CreditsOptions = Options[5]  )

# @app.route('/class_search/<class_info>/')
# def classInfo(class_info):
#     CourseRatings = calculateClassRatings(getClassReviews('', class_info))
#     Course_text_review = str(CourseRatings[3])
#     toughness = str(CourseRatings[4])
#     interest = str(CourseRatings[5])
#     Textbook = str(CourseRatings[6])
#     return render_template('class_info.html', Textbook = Textbook, interest = interest,toughness = toughness,Course_text_review = Course_text_review )
 
@app.route('/instructor_eval/')
def eval():
    return render_template('instructor_eval.html', DepartmentKeys= Sort_dict(GetOptions()[3], False), DepartmentOptions =  GetOptions()[3])
    

@app.route('/class_search/')
def DisplayClasses(term, subject, credit, attr, divs, campus):
    global Professors 
    global ProfDepartments
    ClassList = GetClasses(term, subject, credit, attr, divs, campus)
    didAddProf = False
    didAddDept = False
    
    # Checks to see if every instructor is is Professors dictionary. If they
    # are not, we add their names to the text file, and recalculate the Professors dictionary
    ProfsAdded = []
    for course in ClassList:
        try:
            profs = course['Instructor']
            Department = ''.join([char for char in course['Course - Sec'].split(' ')[0] if char.isalpha()])
            P = [course['Teacher_Info'][i].split('P=')[-1] for i in range(len(course['Teacher_Info']))]
            for i in range(len(profs)):
                if profs[i] not in Professors:
                    f  = open('TeacherList.txt', 'a')
                    f.write('<OPTION VALUE="' + str(P[i]) + '">' + str(profs[i]) + '\n')
                    f.close()
                    didAddProf = True
                if profs[i] not in ProfDepartments and (profs[i], Department) not in ProfsAdded :
                    f = open('ProfessorDepartments.txt', 'a')
                    f.write(str(profs[i]) + '; Departments:'+ Department + '\n')
                    f.close()
                    didAddDept = True
                    ProfsAdded.append((profs[i], Department))
                if Department not in ProfDepartments[profs[i]] and (profs[i], Department) not in ProfsAdded:
                    f = open('ProfessorDepartments.txt', 'a')
                    f.write(str(profs[i]) + '; Departments:'+ Department + '\n')
                    f.close()
                    didAddDept = True
                    ProfsAdded.append((profs[i], Department))


        except KeyError:
            pass
    if didAddProf:
        Professors = GetAllProfessors()
        didAddProf = False
    if didAddDept:
        ProfDepartments = GetAllProfessorDepartments()
        didAddDept = False
    # Keys specifies what exactly we want to show up on our class search


    Keys = ['Title', 'Course - Sec','View_Books', 'Cr', 'Max', 'Opn', 'CRN','Teacher_Info', 'Instructor', 'When','Begin','End','Where']
    return render_template('DisplayClassData.html', TermOptionKeys = Sort_dict(Options[0], True), TermOptions = Options[0] , 
    DivisionOptionKeys = Sort_dict(Options[1], False), DivisionOptions = Options[1],
    CampusOptionKeys = Sort_dict(Options[2], False), CampusOptions = Options[2], 
    SubjectOptionKeys = Sort_dict(Options[3], False), SubjectOptions =  Options[3], 
    AttributeOptionKeys = Sort_dict(Options[4], False), AttributeOptions = Options[4],
    CreditsOptionKeys = Sort_dict(Options[5], False), CreditsOptions = Options[5], ClassList = ClassList, Keys = Keys)

@app.route('/class_info/<Class>-<CRN>-<Term>')
def DisplayClassPage(Class, CRN, Term):
    CourseName = Class
    Descriptions = GetClassDescriptionAndAll(CRN, Term)
    CourseDescription = Descriptions[0]
    CourseRatings = calculateClassRatings(getClassReviews('', Class))
    toughness = CourseRatings[3]  
    interest = CourseRatings[4]
    Textbook = CourseRatings[5]
    if type(toughness) == str:
        Overall_Rating = ''
    else:
        Overall_Rating = (toughness + interest) / 2.0

    # Round numbers
    if type(toughness) == float:
        toughness = round(toughness,2)
    if type(interest) == float:
        interest = round(interest,2)
    if type(Textbook) == float:
        Textbook = round(Textbook,2)
    Prerequisites = ''
    Corequisites = ''
    if Descriptions[1] == "Corequisite Only":
        Corequisites = Descriptions[2]
        Attributes = Descriptions[3]
        Restrictions = Descriptions[4]
        Registration = Descriptions[5]
        CrossListed = Descriptions[6]
    elif Descriptions[1] == "Both":
        Prerequisites = Descriptions[2]
        Corequisites = Descriptions[3]
        Attributes = Descriptions[4]
        Restrictions = Descriptions[5]
        Registration = Descriptions[6]
        CrossListed = Descriptions[7]
    elif  Descriptions[1] == 'Prerequisite Only':
        Prerequisites = Descriptions[2]
        Attributes = Descriptions[3]
        Restrictions = Descriptions[4]
        Registration = Descriptions[5]
        CrossListed = Descriptions[6]

    else:
        Attributes = Descriptions[2]
        Restrictions = Descriptions[3]
        Registration = Descriptions[4]
        CrossListed = Descriptions[5]
    Restrictions = ["Must " + i for i in Restrictions.split("Must")[1:]]
    Remaining  = Registration.split("TOTAL")[1]
    Remaining = Remaining.split("\n")[1:-1]
    # Spots = []
    # if CrossListed:
    #     CrossListed = CrossListed.split("\n\n\n")[1:-1]
    #     temp = []
    #     for i in CrossListed:
    #         data = i.split("\n")
    #         Spots.append(data[2:])
    #         courseName = data[0]
    return render_template('class_info.html',CrossListed = CrossListed ,Registration = Remaining, Restrictions = Restrictions, Overall_Rating = Overall_Rating,Prerequisites = Prerequisites, Corequisites = Corequisites, CourseName = CourseName, CourseDescription = CourseDescription, Textbook = Textbook, interest = interest,toughness = toughness, Attributes = Attributes )


@app.route('/DepartmentsMain/')
def DepartmentsMainPage():
    DepartmentsByCollege = GetSubjectsInDepartments()
    return render_template('DepartmentsMain.html', DepartmentsByCollege = DepartmentsByCollege)


@app.route('/InstructorByCollege/<College>')
def InstructorByCollege(College):
    Departments = [i for i in GetSubjectsInDepartments() if College in i[0]][0][1:]
    Teachers = ["Teacher 1", "Teacher 2", "Teacher 3", "Teacher 4"]
    return render_template('InstructorByCollege.html', College = College ,Departments = Departments, Teachers = Teachers)
    
@app.route('/Department/<Department>')
def InstructorByDepartment(Department):
    # Place holder lists
    #Teachers = set([''.join([i[0], i[1]]) for i in getProfReviews('', '',Options[3][Department], '')])
    
    Teachers = [prof for prof in ProfDepartments if Options[3][Department] in ProfDepartments[prof]]
    Teachers_Sorted = Sort_dict(Teachers, False)
    Best_Professors = bestProf(Options[3][Department])
    Best_Teachers,Best_Teachers_Sorted  = bestProf(Options[3][Department])#Best_Professors[0], Best_Professors[1]
    Easiest_Teachers,Easiest_Teachers_Sorted  = easiestProf(Options[3][Department])
    Best_Classes,Best_Classes_Sorted  = bestClass(Options[3][Department])

    Crn_and_Term = {}
    for course in Best_Classes_Sorted:
        Course = getClassReviews('', course)[0][0]
        Crn_and_Term[Course[2]] = ((Course[-2], Course[-1]))
    
    Easiest_Classes,Easiest_Classes_Sorted  = easiestClass(Options[3][Department])
    DepartmentOptions = Options[3]
    for option in DepartmentOptions:
        if DepartmentOptions[option] == Department:
            Department = option
    return render_template('Department.html',Teachers_Sorted = Teachers_Sorted,Best_Teachers_Sorted = Best_Teachers_Sorted,Best_Teachers = Best_Teachers, 
    Easiest_Teachers = Easiest_Teachers,Easiest_Teachers_Sorted = Easiest_Teachers_Sorted, Department = Department,Teachers = Teachers,
    Best_Classes = Best_Classes,Best_Classes_Sorted = Best_Classes_Sorted,Easiest_Classes = Easiest_Classes, Easiest_Classes_Sorted = Easiest_Classes_Sorted
    ,Crn_and_Term = Crn_and_Term)

@app.route('/instructor_info/<ProfessorName>')
def Instructor(ProfessorName):
    try:
        CoursesTaught = GetCoursesTaught(Professors[ProfessorName])
        num_items = len(CoursesTaught[0]) - 1 # need this to be index of semester code 
    except KeyError:
        CoursesTaught =  []
    RevisedCoursesTaught = []
    for i in xrange(len(CoursesTaught)):
        if i != 0:
            if (CoursesTaught[i][0].split()[0] != CoursesTaught[i-1][0].split()[0]) or (CoursesTaught[i][num_items] != CoursesTaught[i-1][num_items]):
                RevisedCoursesTaught.append(CoursesTaught[i])
        else:
            RevisedCoursesTaught.append(CoursesTaught[i])


    last_name = str(ProfessorName.split(',')[0]) + ','
    first_name = str(ProfessorName.split(',')[1])
    Reviews = getProfReviews(Professors[last_name + first_name])
    OverallRatings = calculateProfRatings(Reviews) 

    ProfessorDescriptions = [review[2] for review in Reviews]
    ReviewCount = len(Reviews)
    
    workload = OverallRatings[3]
    if type(workload) == float:
        workload = round(workload,2)

    grading = OverallRatings[4]
    if type(grading) == float:
        grading = round(grading,2)
    quality = OverallRatings[5]
    if type(quality) == float:
        quality = round(quality, 2)
    accessibility = OverallRatings[6]
    if type(accessibility) == float:
        accessibility = round(accessibility,2)
    syllabus = OverallRatings[7]
    if type(syllabus) == float:
        accessibility = round(accessibility,2)
    
    ProfReviews = OverallRatings[2]
    return render_template('instructor_info.html',Courses = RevisedCoursesTaught,ProfessorDescriptions = ProfessorDescriptions, ProfessorName = ProfessorName ,ProfReviews = ProfReviews, workload = workload,grading = grading, quality = quality, accessibility = accessibility, ReviewCount = ReviewCount)

@app.route('/BestClassesFor/', methods = ['GET', 'POST'])
def BestClassesFor(page = 1):
    # Dummy list until we can access classes from database
    if page == 1:
        Attributes = {'2nd Theology':'THE2', '2nd Philosophy':'PHI2', 'Social Science': 'SOSC',  'Natural Science (req)': 'NASC'}
    elif page == 2:
        Attributes = {'Fine Arts':'FNAR', 'Literature':'LIT', 'History': 'HIST'}
    ClassList = []
    if page == 1:
        SubjectsSorted = ['2nd Theology', '2nd Philosophy', 'Social Science', 'Natural Science (req)']
    elif page == 2:
        SubjectsSorted = ['Fine Arts', 'Literature', 'History']
    Indexs = range(len(SubjectsSorted))
    for attr in SubjectsSorted:
        courses = GetClasses('201510', Options[3].values(), 'A', Attributes[attr],'A', 'M')
        course_container = []
        for i in courses:
            course_container.append([i['Title'], i['CRN'], i['Term']])
        ClassList.append(course_container)
    

    return render_template('BestClassesFor.html', Subjects = Attributes, SubjectsSorted = SubjectsSorted, Courses = ClassList, Indexs = Indexs)









@app.route('/ProfessorReviewForm/<ProfessorName>', methods = ['GET', 'POST'])
def ProfessorReview(ProfessorName):
    if request.method == 'POST':
        # Instructor evaluation
        CourseName = ' '.join(request.form['CoursesTaughtID'].split(' ')[:-2])
        CRN = ''.join(request.form['CoursesTaughtID'].split(' ')[-2])
        Term = ''.join(request.form['CoursesTaughtID'].split(' ')[-1])
        Grading = int(request.form['GradingID'])
        Quality = int(request.form['QualityID'])
        Workload = int(request.form['WorkloadID'])
        Accessibility = request.form['AccessibilityID']
        Syllabus = int(request.form['SyllabusID'])
        OptionalDescriptionProfessor = str(request.form['OptionalResponseProfessor'])
        # Course Evaluation
        CourseToughness = int(request.form['ToughnessID'])
        CourseInterest = int(request.form['InterestID'])
        TextbookNeeded =  int(request.form['TextbookNeeded'])
        OptionalDescriptionCourse = str(request.form['OptionalResponseCourse'])
        
        # Add to database
        last_name = str(ProfessorName.split(',')[0]) + ','
        first_name = str(ProfessorName.split(',')[1])
        try:
            department = ProfDepartments[ProfessorName]
        except:
            department = "Unknown"
        
        addProfReview(last_name, first_name, OptionalDescriptionProfessor, Workload, Grading, Quality, Accessibility,Syllabus, department, Professors[last_name + first_name])
        addClassReview(last_name, first_name, CourseName, OptionalDescriptionCourse, CourseToughness, CourseInterest, TextbookNeeded, department, CRN, Term, Professors[last_name + first_name])
        return render_template('PostSubmissionForm.html', test =' ' )        
         
    try:
        CoursesTaught = GetCoursesTaught(Professors[ProfessorName])
    except KeyError:
        CoursesTaught =  ["No courses listed"]
    

    num_items = len(CoursesTaught[0]) - 1
    RevisedCoursesTaught = []

    for i in xrange(len(CoursesTaught)):
        if i != 0:
            if (CoursesTaught[i][2] != CoursesTaught[i-1][2]) or (CoursesTaught[i][num_items] != CoursesTaught[i-1][num_items]):
                RevisedCoursesTaught.append(CoursesTaught[i])
        else:
            RevisedCoursesTaught.append(CoursesTaught[i])
    return render_template('ProfessorReviewForm.html', ProfessorName = ProfessorName, CoursesTaught = RevisedCoursesTaught)

@app.route('/SubmitReviewMain/')
def SubmitReviewMain():
    global Professors
    ProfessorKeys = Sort_dict(Professors, False) 
    ProfessorKeys = [i.decode('utf-8') for i in ProfessorKeys]
    return render_template('SubmitReviewMain.html', DepartmentKeys = Sort_dict(Options[3], False), DepartmentOptions =  Options[3], Professors = Professors, ProfessorKeys = ProfessorKeys)

if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)

