from flask import Flask
from flask import render_template
from flask import Response, request, jsonify, redirect, url_for

import re
app = Flask(__name__)

#quiz questions
questions = {
    0:{
        "type": "multiple_choice",
        "text": "Sample Question 1", 
        "options": ["opt 1", "opt 2", "opt 3"]
    },
    1:{
        "type": "textbox",
        "text": "Sample Question 2"  
    },
    2:{
        "type": "drag_drop",
        "text": "Sample Question 3",
        "pairs": {"one":"1", "two":"2"}
    }
}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/quiz/<int:question_id>', methods=['GET', 'POST'] )
def quiz(question_id):
    if question_id>=len(questions):
        return redirect(url_for('quiz_score'))
    
    question = questions[question_id]
    question_type = question['type']
    if request.method == 'POST':
        user_submission = request.form.get('submission')
        return redirect(url_for('quiz', question_id=question_id+1))
    
    # differential between the three q&a types
    template = f"quiz_{question['type']}.html"
    return render_template(template, question=question, question_id=question_id)

@app.route('/quiz_score')
def quiz_score():
    return render_template('quiz_score.html')
  
if __name__ == '__main__':
   app.run(debug = True, port=5001)
