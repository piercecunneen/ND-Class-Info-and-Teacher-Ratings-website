from flask import Flask, render_template
from class_search_web_scrapping import  GetOptions, Sort_dict, GetClasses, GetClassDescriptionAndAll


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
    #
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
    
@app.route('/departments/')
def DepartmentsMainPage():
    return render_template('departments.html')

if __name__=='__main__':
    app.run(debug=True)

