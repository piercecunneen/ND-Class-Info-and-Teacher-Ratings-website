from flask import Flask, render_template, request
from class_search_web_scrapping import GetCoursesTaught,GetAllProfessors, GetOptions, Sort_dict, GetClasses, GetSubjectsInDepartments, GetClassDescriptionAndAll, GetAllProfessorDepartments
from database_functions import getClassReview, getProfReviews, addClassReview, addProfReview, calculateProfRatings

app = Flask(__name__)



Options = GetOptions()

Professors = GetAllProfessors()
ProfDepartments = GetAllProfessorDepartments()

def GetCurrentSemester():
    return '201510' 

@app.route('/')
def home():
    return render_template('home.html')

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
        #return render_template('home.html', Term = Term, Subject = Subject, Attribute = Attribute, Division = Division, Campus = Campus, Credit = Credit)
    return render_template('class_search.html', TermOptionKeys = Sort_dict(Options[0], True), TermOptions = Options[0] , 
    DivisionOptionKeys = Sort_dict(Options[1], False), DivisionOptions = Options[1],
    CampusOptionKeys = Sort_dict(Options[2], False), CampusOptions = Options[2], 
    SubjectOptionKeys = Sort_dict(Options[3], False), SubjectOptions =  Options[3], 
    AttributeOptionKeys = Sort_dict(Options[4], False), AttributeOptions = Options[4],
    CreditsOptionKeys = Sort_dict(Options[5], False), CreditsOptions = Options[5]  )

@app.route('/class_search/class_info/')
def classInfo():
    return render_template('class_info.html')
 
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

@app.route('/class_info/<Class>/<CRN>/<Term>')
def DisplayClassPage(Class, CRN, Term):
    CourseName = Class
    Descriptions = GetClassDescriptionAndAll(CRN, Term)
    CourseDescription = Descriptions[0]
    Prerequisites = ''
    Corequisites = ''
    if Descriptions[1] == "Corequisite Only":
        Corequisites = Descriptions[2]
    elif Descriptions[1] == "Both":
        Prerequisites = Descriptions[2]
        Corequisites = Descriptions[3]
    elif  Descriptions[1] == 'Prerequisite Only':
        Prerequisites = Descriptions[2]
    return render_template('class_info.html', Prerequisites = Prerequisites, Corequisites = Corequisites, CourseName = CourseName, CourseDescription = CourseDescription)


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
    Teachers = ["Teacher 1", "Teacher 2", "Teacher 3", "Teacher 4"]
    #Data = GetClasses('2)
    
    BestTeachers = ['Best Teacher 1', 'Best Teacher 2', 'Best Teacher 3','Best Teacher 4', 'Best Teacher 5']
    DepartmentOptions = Options[3]
    for option in DepartmentOptions:
        if DepartmentOptions[option] == Department:
            Department = option
    return render_template('Department.html', Department = Department,Teachers = Teachers, BestTeachers = BestTeachers)

@app.route('/instructor_info/<ProfessorName>')
def Instructor(ProfessorName):
    try:
        CoursesTaught = GetCoursesTaught(Professors[ProfessorName])
    except KeyError:
        CoursesTaught =  []
    last_name = str(ProfessorName.split(',')[0])
    first_name = str(ProfessorName.split(',')[1])
    OverallRatings = calculateProfRatings(getProfReviews(last_name, first_name, '', '')) 
    #orkloadt, gradingt, qualityt, accessiblityt, syllabust]
    workload = OverallRatings[3]
    grading = OverallRatings[4]
    quality = OverallRatings[5]
    accessibility = OverallRatings[6]
    syllabus = OverallRatings[7]
    
    ProfReviews = OverallRatings[2]
    return render_template('instructor_info.html',Courses = CoursesTaught, ProfessorName = ProfessorName ,ProfReviews = ProfReviews, workload = workload,grading = grading, quality = quality, accessibility = accessibility)

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
        CourseName = str(request.form['CoursesTaughtID'])
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
        last_name = str(ProfessorName.split(',')[0])
        first_name = str(ProfessorName.split(',')[1])
    
        department = "ACMS"
        addProfReview(last_name, first_name, OptionalDescriptionProfessor, Workload, Grading, Quality, Accessibility,Syllabus, department)
        addClassReview(last_name, first_name, CourseName, OptionalDescriptionCourse, CourseToughness, CourseInterest, TextbookNeeded, Syllabus, department)
        return render_template('PostSubmissionForm.html', test = first_name)        
         
    CoursesTaught = ["Course 1", "Course 2", "Course 3", "Course 4"]
    return render_template('ProfessorReviewForm.html', ProfessorName = ProfessorName, CoursesTaught = CoursesTaught)



if __name__=='__main__':
    app.run(debug=True)

