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

lessons = {
    0:{
        "lesson_id": "0",
        "Section": "Posistions", 
        "title": "Neutral",
        "main-text": "Every match starts in “Neutral”, where both wrestlers are on their feet facing each other.",
        "sub-text": ['Crouched down in their “stances”','Looking for offensive and defensive scoring'],
        "media": "https://images2.minutemediacdn.com/image/upload/c_crop,w_4010,h_2255,x_0,y_0/c_fill,w_2160,ar_16:9,f_auto,q_auto,g_auto/images%2FImagnImages%2Fmmsport%2Fall_penn_state%2F01jpxxdds2hs0ce4jydd.jpg",
    },
    1:{
        "lesson_id": "1",
        "Section": "Posistions", 
        "title": "Top",
        "main-text": '“Top” is when one wrestler is on top of the other (Black Singlet)',
        "sub-text": ['May be chosen as starting position for 2nd and 3rd periods','Results after one wrestler takes the other from neutral to the mat'],
        "media": "https://www.wrestlingmindset.com/wp-content/uploads/2018/01/Top-Position.jpg",
    },
    2:{
        "lesson_id": "2",
        "Section": "Posistions", 
        "title": "Bottom",
        "main-text": '“Bottom” is when one wrestler is under the other (White Singlet)',
        "sub-text": ['May be chosen as starting position for 2nd and 3rd periods','Results after one wrestler takes the other from neutral to the mat'],
        "media": "https://www.wrestlingmindset.com/wp-content/uploads/2018/01/Top-Position.jpg",
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
