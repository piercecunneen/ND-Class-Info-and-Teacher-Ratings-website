from flask import Flask, render_template, redirect, url_for, request
from class_search_web_scrapping import GetCoursesTaught,GetAllProfessors, GetOptions, Sort_dict, GetClasses, GetSubjectsInDepartments, GetClassDescriptionAndAll


app = Flask(__name__)


Options = GetOptions()

Professors = GetAllProfessors()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/class_search/', methods = ['GET', 'POST'])
def ClassSearch():
    if request.method == 'POST':
        Term = request.form['TermOptions']
        Subject = request.form['SubjectOptions']
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
    ClassList = GetClasses(term, subject, credit, attr, divs, campus)
    # Keys specifies what exactly we want to show up on our class search
    Keys = ['Title', 'Course - Sec','View_Books', 'Cr', 'Max', 'Opn', 'CRN','Teacher_Info', 'Instructor', 'When','Begin','Where']
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
    return render_template('InstructorByCollege.html', College = College)
    
@app.route('/Department/<Department>')
def InstructorByDepartment(Department):
    # Place holder lists
    Teachers = ["Teacher 1", "Teacher 2", "Teacher 3", "Teacher 4"]
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
    Courses = ['Course 1', 'Course 2', 'Course 2']
    return render_template('instructor_info.html', Courses = CoursesTaught, ProfessorName = ProfessorName)

@app.route('/BestClassesFor/')
def BestClassesFor():
    # Dummy list until we can access classes from database
    DummyClassList= ['Class 1', 'Class 2', 'Class 3', 'Class 4', 'Class 5', 'Class 6']
    Attributes = {'2nd Theology':'THE2', '2nd Philosophy':'Phil2', 'Social Science': 'SOSC', 'University Seminars':'USEM', 'Natural Science (req)': 'NASC','Fine Arts':'FNAR', 'Literature':'LIT', 'History': 'HIST'}
    SubjectsSorted = ['2nd Theology', '2nd Philosophy', 'Social Science', 'University Seminars', 'Natural Science (req)','Fine Arts', 'Literature', 'History']

    return render_template('BestClassesFor.html', Subjects = Attributes, SubjectsSorted = SubjectsSorted, Courses = DummyClassList)









@app.route('/ProfessorReviewForm/<ProfessorName>', methods = ['GET', 'POST'])
def ProfessorReview(ProfessorName = None):
    if request.method == 'POST':
        # Instructor evaluation
        CourseName = request.form['CoursesTaughtID']
        Grading = request.form['GradingID']
        Quality = request.form['QualityID']
        Workload = request.form['WorkloadID']
        #Accessibility = request.form['AccessibilityID']
        #Syllabus = request.form['Syllabus']
        OptionalDescriptionProfessor = request.form['OptionalResponseProfessor']

        # Course Evaluation
        CourseToughness = request.form['ToughnessID']
        CourseInterest = request.form['InterestID']
        TextbookNeeded =  request.form['TextbookNeeded']
        OptionalDescriptionCourse = request.form['OptionalResponseCourse']
        
        # Add to database
        
        
        return render_template('PostSubmissionForm.html', test = CourseToughness)        
         
    CoursesTaught = ["Course 1", "Course2", "Course 3", "Course3"]
    return render_template('ProfessorReviewForm.html', ProfessorName = ProfessorName, CoursesTaught = CoursesTaught)



if __name__=='__main__':
    app.run(debug=True)

