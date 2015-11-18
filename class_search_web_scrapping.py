import requests
from bs4 import BeautifulSoup

def CleanUpString(string):
    """Cleans up a string by getting rid of '\\t', '\\r', '\\n', and double spaces (i.e. '  ').
    Input: string
    Returns: String
    """
    return string.replace('\t', '').replace('\r','').replace('\n', '').replace('  ', '')

    
    
    
def GetOptions():
    """Gets the options for the 6 categories (Term, Division, Campus, Subject, Attribute, and Credits)..
    Gets both the option that is displayed on class-search.nd.edu as well as the option_key that is neccessary 
    to submit the post request in order to navigate to the correct page
    Returns: dictionary of option_descriptions (what is displayed on class-search.nd.edu)
        that point to option_keys{option_description: option_key}
    """
    
    #
    url = 'https://class-search.nd.edu/reg/srch/ClassSearchServlet'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "lxml")
    data = soup.find_all('select')
    
    # Dictionaries used to store both option description and the form data value required for post requests
    TermOptions = {}
    DivisionOptions = {}
    CampusOptions  = {}
    SubjectOptions = {}
    AttributeOptions= {}
    CreditsOptions = {}
    
    OptionCategories = [TermOptions, DivisionOptions, CampusOptions, SubjectOptions, AttributeOptions, CreditsOptions]
    
    for i, category in zip(data, OptionCategories):
        options = i.find_all('option')
        for option in options:
            # check if option is selected. If so, then use 4th item in list
            option_split = str(option).split('"')
            if 'selected' in option_split[0]:
                category[CleanUpString(str(option.text))] = str(option).split('"')[3]
            else:
                category[CleanUpString(str(option.text))] = str(option).split('"')[1]
    
    # Get rid of all Year entries for TermOptions
    New_Term_Options = OptionCategories[0].copy()
    for entry in New_Term_Options:
        if 'Year' in entry:
            del OptionCategories[0][entry]
    return OptionCategories
        



    

def GetClasses(term, subj, credit, Attr, divs, campus):
    """
    Given the inputs, function will find the class data from class-search.nd.edu.
    Inputs: Academic term, Academic subject, number of credits, Attribute type, Academic division, and finally campus. 
       All should be in the form of strings
    Returns: A list of dictionaries, with each dictionary being a specific class at Notre Dame
       Each dictionary has the same keys and gives the same information for each class 
    """
    url = 'https://class-search.nd.edu/reg/srch/ClassSearchServlet'
   
    #divs = 'A'
    #campus = 'M'
    #Attr = '0ANY'
    #credit = 'A'
    
    # stores data for the post request
    FormData = {'TERM': term, 'SUBJ': subj, 'CREDIT':credit, 'ATTR':Attr, 'DIVS':divs, 'CAMPUS' : campus}
    
    response = requests.post(url, data = FormData)
    soup = BeautifulSoup(response.content, "lxml")
    ClassTable = soup.find_all('table', {'id':'resulttable'})
    
    # If no classes listed on class search, return an empty []
    if len(ClassTable) == 0:
        return []
    else:
        ClassTable = ClassTable[0].find_all('tr')

        Headers = ClassTable[0].find_all('th')
        
        # Class_Headers stores the column headers for the class data
        Class_Headers = []
        for header in Headers:
            Class_Headers.append(str(header.text))
        
        
        Classes = ClassTable[1:]
        
        Classlist = []
        
        # Temporary counting variable
        Num_Classes = 0
        URLS = []
        for Class in Classes:
            Classlist.append({})
            Info = Class.find_all('td')
            URLS.append([])
            for i, header in zip(Info,Class_Headers):                
                url = ''
                url = i.find_all('a')
                if url:
                    URLS[Num_Classes].append(url)
                try:
                    if header == 'Instructor':
                        names = i.find_all('a')
                        professors = []
                        for name in names:
                            try:
                                x = CleanUpString(str(name.text).replace('\t', ''))
                                if x[-1] == ' ':
                                    x = x[:-1]
                                professors.append(x)
                            except:
                                x = CleanUpString(name.text.replace('\t', ''))
                                if x[-1] == ' ':
                                    x = x[:-1]
                                professors.append(x)
                            Classlist[Num_Classes][header]  = professors
                    else:
                        Classlist[Num_Classes][header] = CleanUpString(str(i.text).replace('\t', ''))
                except UnicodeEncodeError:
                    Classlist[Num_Classes][header] = CleanUpString(i.text.replace('\t', ''))
            Classlist[Num_Classes]['Campus'] = campus
            Classlist[Num_Classes]['Term'] = term
            Classlist[Num_Classes]['Attribute'] = Attr
            Num_Classes += 1
        
        # Reassign temporary counting variable
        Num_Classes = 0
        for url in URLS:
            ClassUrlData = url[0]
            ClassDescriptionUrl = ClassUrlData[0].get('href')
            BookStoreUrlData = ClassUrlData[1]
            BookStoreUrl = BookStoreUrlData.get('href')
            ClassUrlExtension = CleanUpString(ClassDescriptionUrl.split("'")[1])
            
            Classlist[Num_Classes]['Course_Info'] = 'https://class-search.nd.edu/reg/srch/' + ClassUrlExtension
            Classlist[Num_Classes]['View_Books'] =  BookStoreUrl
            
            # Some classes have no teacher yet announced. If they do not have a teacher, then len(url) == 1. 
            # If the teacher is announced, len(url) == 2
            if len(url) == 2:
                url_data = []
                for i in range(len(url[1])):
                    InstructorUrlData = url[1][i].get('href')
                    TeacherUrlExtension = CleanUpString(InstructorUrlData.split("'")[1])
                    url_data.append(TeacherUrlExtension)
                Classlist[Num_Classes]['Teacher_Info'] = [ ('https://class-search.nd.edu/reg/srch/' + i) for i in url_data]           
            else:
                Classlist[Num_Classes]['Teacher_Info'] = 'NONE'
            Num_Classes += 1
        
        # Clean up Course - sec in Classlist
        for i in Classlist:
            i['Course - Sec'] = i['Course - Sec'].replace('*View Books', '').replace('View Books', '')
    
        return Classlist




def GetClassDescriptionAndAll(CRN, Term):
    """Gets the class description, the course prerequisites, and the course corequisites
    Input: a url of a class specific page
    returns: A list with the course description, a string that reveals the contents of the rest of the list, 
            the prerequisites (if any), and corequisites (if a
            String options: 'Both', 'Neither', 'Prerequisote Only', or 'Corequisite Only'
    """
    url = 'https://class-search.nd.edu/reg/srch/ClassSearchServlet?CRN=' + str(CRN) + '&TERM=' + str(Term)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "lxml")
    
    
    Data = soup.find_all('td')[2].text.split('Restrictions:')
    DataText = Data[0]
    try:
        # Catch index error if class has no attributes
        AttributeText = CleanUpString(Data[1].split("Course Attributes:")[1].split(".syllabus")[0])
        AttributeText = [str(i) for i in AttributeText.split(u"\xa0")]
    except IndexError:
        AttributeText = []
    
    Course_Description = DataText.split('Associated Term:')[0]
    
    
    if 'Prerequisites' in DataText:
        if 'Corequisites' in DataText:
            Temporary = DataText.split('Prerequisites:')[1].split('Corequisites:')
            Prerequisites = CleanUpString(str(Temporary[0]))
            Corequisites = CleanUpString(str(Temporary[1]))
            return [Course_Description, 'Both', Prerequisites, Corequisites, AttributeText]
        else:
            Prerequisites = CleanUpString(DataText.split('Prerequisites:')[1])
            return [Course_Description, 'Prerequisite Only', Prerequisites, AttributeText]
    elif 'Corequisites' in DataText:
            Corequisites = CleanUpString(DataText.split('Corequisites:')[1])
            return [Course_Description, 'Corequisite Only', Corequisites, AttributeText]
    else:
        return [Course_Description, 'Neither', AttributeText]




def Sort_dict(data, isTerms):
    """ Takes the keys in a dictionary, sorts them by their corresponding value, and then puts
    the keys in an ordered list. For the Terms, want highest numbers first, so need to reverse the keys list"""
    
    if isTerms:
        keys = sorted(data, key=data.get)
        keys.reverse()
        return keys
    else:
        return sorted(data)


#CollegeDepartments = []
#for i in Colleges:
#    CollegeDepartments.append([])
#Subjects = GetOptions()[3]
#for subject in Subjects:
#    index = 0
#    for i in Colleges:
#        print i + ': ' + str(index)
#        index += 1
#    print subject
#    Department = input("Department = ")
#    print ' '
#    print ' ----------------------'
#    CollegeDepartments[Department].append(subject)
def GetSubjectsInDepartments():
    Colleges = ['School of Architecture', 'College of Arts & Letters', 'College of Engineering','First Year of Studies', 'The Law School','Mendoza College of Business', 'College of Science', "St. Mary's College",'Other']
    Colleges_with_deparments = []
    for i in Colleges:
        Colleges_with_deparments.append([])
    f = open('SubjectsInColleges.txt', 'r')
    department_index = 0
    for line in f.read().split('\n'):
        if line == '-----':
            department_index += 1
        else:
            if line == '':
                continue
            else:
                Colleges_with_deparments[department_index].append(line)
    sorted_Colleges_with_deparments = []
    for college in Colleges_with_deparments:
        new_college = [college[0]] + sorted(college[1:])
        sorted_Colleges_with_deparments.append(new_college)
    f.close()
    return sorted_Colleges_with_deparments
    




def GetAllProfessors():
    f = open('TeacherList.txt', 'r')
    Professors = {}
    
    line = f.readline()
    while line != '':
        name = line.split('>')[-1].replace('\n', '')
        
        # get rid of any trailing spaces
        while name[-1] == ' ':
            name = name[:-1]
        # get last name
        last_name = CleanUpString(name.split(',')[0])
        
        # get list of all middle and first names
        surname = [CleanUpString(string) for string in name.split(',')[1].split(' ') if string != ' ' and string != '']
        surname_combinations = []
        for i in range(1,len(surname)+1):
            surname_combinations.append(' '.join(surname[0:i]))
        name_combinations = [last_name + ', ' + surname_option for surname_option in surname_combinations]
        ID = CleanUpString(line.split('"')[1])
        for i in name_combinations:
            Professors[i] = ID
        line = f.readline()
    return Professors

def GetAllProfessorDepartments():
    f = open('ProfessorDepartments.txt', 'r')
    line  = f.readline()
    ProfDepartments = {}
    while line != '':
        name = CleanUpString(line.split('; Departments:')[0])
        Department = CleanUpString(line.split('; Departments:')[1].replace('\n', ''))
        if name in ProfDepartments:
            ProfDepartments[name].append(Department)
        else:
            ProfDepartments[name] = [Department]
        line = f.readline()
    f.close()
    return ProfDepartments
def GetCoursesTaught(Prof_ID):
    url = 'https://class-search.nd.edu/reg/srch/InstructorClassesServlet?TERM=201510&P=' + str(Prof_ID)
    response = requests.get(url)
    soup = BeautifulSoup(response.content)
    rows = soup.find_all('tr')[2:]
    CoursesTaught = []
    for course in rows:
        # gives string that specifies url extension for each course
        url_data = str(course.find_all('a')[0]).split("'")[1].split('P=')[0].replace('&amp;', '')
        url_data = url_data.split('CRN=')[1].split('TERM=')
        CoursesTaught.append(course.text.split('\n')[1:-1] + url_data)
    return CoursesTaught
    


    