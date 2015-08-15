from flask import Flask, render_template
from class_search_web_scrapping import  GetOptions, Sort_dict, GetClasses, GetSubjectsInDepartments


app = Flask(__name__)


Options = GetOptions()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/class_search/')
def ClassSearch():
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
    


@app.route('/class_search/Term=<term>/Subject=<subject>/Credit=<credit>/Attr=<attr>/Division=<divs>/Campus=<campus>')
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

@app.route('/class_info/<Class>')
def DisplayClassPage(Class):
    ClassInformation = Class
    return render_template('class_info.html', ClassInfo = ClassInformation)
    
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
    Courses = ['Course 1', 'Course 2', 'Course 2']
    return render_template('instructor_info.html', Courses = Courses, ProfessorName = ProfessorName)

@app.route('/BestClassesFor/')
def BestClassesFor():
    # Dummy list until we can access classes from database
    X = ['Class 1', 'Class 2', 'Class 3', 'Class 4', 'Class 5', 'Class 6']
    Attributes = {'2nd Theology':'THE2', '2nd Philosophy':'Phil2', 'Social Science': 'SOSC', 'University Seminars':'USEM', 'Natural Science (req)': 'NASC','Fine Arts':'FNAR', 'Literature':'LIT', 'History': 'HIST'}
    SubjectsSorted = ['2nd Theology', '2nd Philosophy', 'Social Science', 'University Seminars', 'Natural Science (req)','Fine Arts', 'Literature', 'History']

    return render_template('BestClassesFor.html', Subjects = Attributes, SubjectsSorted = SubjectsSorted, Courses = X)


@app.route('/ProfessorReviewForm/<ProfessorName>')
def ProfessorReview(ProfessorName = None):
    CoursesTaught = ["Course 1", "Course2", "Course 3", "Course3"]
    return render_template('ProfessorReviewForm.html', ProfessorName = ProfessorName, CoursesTaught = CoursesTaught)
if __name__=='__main__':
    app.run(debug=True)

