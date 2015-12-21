"""
 Try and get professors to get their students to submit reviews
 For Courses: For big classes, have people pick best professor for a certain class (think Orgo)
 Who's the best professor to take for ...
 Highest rated classes in each subject/department
"""

class Course(object):
    """
    Course Class that keeps track of a Course's name, ID, when it was taught, and the professor who taught it
    """
    def __init__(self, Course_Name, Course_ID, semester_taught, professor):
        self.Course_Name = Course_Name
        self.Course_ID = Course_ID
        self.semester_taught = semester_taught
        self.professor = professor
        self.ratings = []
        self.toughness = None

    def add_rating(self, rating):
	"""
	Adds a rating to the course
	"""
        self.ratings.append(rating)

class Professor(object):
    """ Professor Class stores information about the professor, including name,
    college, department, courses they've taught, any and all ratings, and a link to the ND.edu page

    Methods: 1. add_rating(rating)
                Input: Professor Rating (type == TeacherRating)
             2. add_course_taught(course)
                Input: Course (type == Course)
    """
    def __init__(self, name, college, department, page=None):
        self.name = name
        self.college = college
        self.department = department
        self.courses_taught = []
        self.ratings = []
        self.page = page
        self.grading_rating = None
        self.workload_rating = None
        self.quality_rating = None
        self.overall_rating = None

    def add_rating(self, rating):
        """
        Adds a rating to a professor and updates ratings
        """
        self.ratings.append(rating)
        self.update_ratings()

    def add_course_taught(self, course):
	"""
	Adds a course to the list this professor has taught
	"""
        self.courses_taught.append(course)


    def get_grading(self):
        """
        returns the grading rating of a professor
        """
        return sum([rating.grading for rating in self.ratings]) / float(len(self.ratings))

    def get_workload(self):
        """
        returns the workload rating of a professor
        """
        return sum([rating.workload for rating in self.ratings]) / float(len(self.ratings))

    def get_quality(self):
        """
        returns the quality rating of a professor
        """

        return sum([rating.quality for rating in self.ratings]) / float(len(self.ratings))

    def update_ratings(self):
        """
        Updates professor ratings. Called by add_rating whenever a rating is added
        """
        self.grading_rating = self.get_grading()
        self.workload_rating = self.get_workload()
        self.quality_rating = self.get_quality()
        self.overall_rating = (self.quality_rating + self.grading_rating + self.workload_rating) / 3

class Rating(object):
    """
    A generic rating for either a course or professor
    """
    def __init__(self, author, date, course, text=None):
        self.author = author
        self.date = date
        self.course = course
        self.text = text

class TeacherRating(Rating):
    """
    A rating for a single Professor
    """
    def __init__(self, author, date, course, grading, workload, quality, syllabus, accessibility, text=None):
        super(TeacherRating, self).__init__(author, date, course, text)
        self.grading = grading
        self.workload = workload
        self.quality = quality
        self.syllabus = syllabus # 0 == throw syllabus out; 1 == syllabus is useful; 2 == syllabus is your lifeline
        self.accessibility = accessibility

class CourseRating(Rating):
    """
    A rating for a single Course
    """
    def __init__(self, author, date, course, toughness_rating, interest_rating, text=None):
        super(CourseRating, self).__init__(author, date, course, text)
        self.toughness_rating = toughness_rating
        self.interest_rating = interest_rating
        # Add something about breakdown for work (essays, tests, labs, homework, etc)
