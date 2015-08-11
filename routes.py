# -*- coding: utf-8 -*-
from flask import Flask, render_template
from class_search_web_scrapping import  GetOptions


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/class_search/')
def test():
    Options = GetOptions()
    return render_template('class_search.html', TermOptions = Options[0] , DivisionOptions = Options[1],
    CampusOptions = Options[2], SubjectOptions =  Options[3], 
    AttributeOptions = Options[4], CreditsOptions = Options[5]  )
    
@app.route('/instructor_eval/')
def eval():
    return render_template('instructor_eval.html')
    

if __name__=='__main__':
    app.run(debug=True)

