from flask import Flask, render_template
from class_search_web_scrapping import  GetOptions


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/test')
def about():
    Options = GetOptions()
    return render_template('test.html', TermOptions = Options[0] , DivisionOptions = Options[1],
    CampusOptions = Options[2], SubjectOptions =  Options[3], 
    AttributeOptions = Options[4], CreditsOptions = Options[5]  )
    
    

if __name__=='__main__':
    app.run(debug=True)

