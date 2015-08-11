from flask import Flask, render_template
from class_search_web_scrapping import  GetOptions, Sort_by_value


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/class_search/')
def test():
    Options = GetOptions()
    return render_template('class_search.html', TermOptionKeys = Sort_by_value(Options[0], True), TermOptions = Options[0] , 
    DivisionOptionKeys = Sort_by_value(Options[1], False), DivisionOptions = Options[1],
    CampusOptionKeys = Sort_by_value(Options[2], False), CampusOptions = Options[2], 
    SubjectOptionKeys = Sort_by_value(Options[3], False), SubjectOptions =  Options[3], 
    AttributeOptionKeys = Sort_by_value(Options[4], False), AttributeOptions = Options[4],
    CreditsOptionKeys = Sort_by_value(Options[5], False), CreditsOptions = Options[5]  )
    


if __name__=='__main__':
    app.run(debug=True)

