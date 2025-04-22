#!/usr/bin/env python3
# coding: utf-8

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
        "image": "https://i.postimg.cc/Ss7hBMts/neutral-lesson.jpg",
    },
    1:{
        "lesson_id": "1",
        "Section": "Posistions", 
        "title": "Top",
        "main-text": '“Top” is when one wrestler is on top of the other (Black Singlet)',
        "sub-text": ['May be chosen as starting position for 2nd and 3rd periods','Results after one wrestler takes the other from neutral to the mat'],
        "image": "https://i.postimg.cc/15W9RDRV/top-lesson.jpg",
    },
    2:{
        "lesson_id": "2",
        "Section": "Posistions", 
        "title": "Bottom",
        "main-text": '“Bottom” is when one wrestler is under the other (White Singlet)',
        "sub-text": ['May be chosen as starting position for 2nd and 3rd periods','Results after one wrestler takes the other from neutral to the mat'],
        "image": "https://i.postimg.cc/x8n08RbM/bottom-lesson.jpg",
    },
    3:{
        "lesson_id": "3",
        "Section": "Takedown", 
        "title": "Takedown",
        "main-text": 'Takedown” is when one wrestler takes another down from neutral onto the mat.',
        "sub-text": ['3 Points Awarded to Blue assuming he brings yellow to the ground'],
        "expanded-text": ['A takedown is called by the ref once they deem a wrestler has gained control of the other.', 'This can be vague and result in confusing situations.'],
        "image": "https://i.postimg.cc/QtTPCNd1/roman-bravo-young-ragusin.avif",
    },
    4:{
        "lesson_id": "4",
        "Section": "Takedown", 
        "title": "Takedown",
        "main-text": 'The wrestler in yellow demonstrates control',
        "sub-text": ['He hooks the ankle of his opponent!'],
        "image": "https://i.postimg.cc/bJVXDVxf/Wrestling-Takedown-GIF-by-NCAA-Championships-1.gif",
    },
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
  

@app.route('/positions')
def positions():
    return render_template('positions.html')

@app.route('/api/positions')
def api_positions():
    return jsonify(lessons)

@app.route('/learn/<int:lesson_id>', methods=['GET'])
def learn(lesson_id):
    if lesson_id < 0 or lesson_id >= len(lessons):
        return redirect(url_for('quiz', question_id=0))  # Redirect to quiz if out of bounds
    lesson = lessons[lesson_id]
    return render_template('learn.html', lesson=lesson, lesson_id=lesson_id)


if __name__ == '__main__':
   app.run(debug = True, port=5001)
