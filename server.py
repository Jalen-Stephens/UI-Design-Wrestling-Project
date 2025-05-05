#!/usr/bin/env python3
# coding: utf-8

from flask import Flask
from flask import render_template
from flask import Response, request, jsonify, redirect, url_for
import re
import json
import datetime
app = Flask(__name__)

#quiz questions
questions = {
    0:{
        "type": "drag_drop",
        "text": "What position is the wrestler in 'Irish' in before and after the move?",
        "drag_options": ["Top", "Bottom", "Neutral"],
        "drop_options": ["Start", "End"],
        "media": "https://i.postimg.cc/BnC8WwGz/Scramble-Takedown.gif"
    },
    1:{
        "type": "textbox",
        "text": "How many points were scored by orange in this exchange?", 
        "media":  "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExdHFrbXVnMXFuNjB5NXRuZWcwcWp0aXZ4MWN2emJsZXplenQwNnR6ayZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/upJkEoxKC97OO3wv4q/giphy.gif"
    },
    2:{
        "type": "multiple_choice",
        "text": "How many points are scored in a takedown?", 
        "media": "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExbzlhNGVob3R1eG8wZ3AwbXRtNWV2Nzh5ZTE5eW4xbXFycWV1a2s5MiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/bM1uXhDYFMzU4GfJdq/giphy.gif",
        "options": ["2", "4", "3"]
    },
    3:{
        "type": "multiple_choice",
        "text": "What type of score was this from the wrestler in Orange?", 
        "media":  "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExdHFrbXVnMXFuNjB5NXRuZWcwcWp0aXZ4MWN2emJsZXplenQwNnR6ayZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/upJkEoxKC97OO3wv4q/giphy.gif",
        "options": ["Nearfall", "Escape", "Takedown", "Reversal"]
    },
    4:{
        "type": "drag_drop",
        "text": "What position was the Cornell wrestler in before scoring? What about after scoring?",
        "drag_options": ["Top","Bottom","Neutral"],
        "drop_options": ["Before","After"],
        "media": "https://i.postimg.cc/FFMwj4KX/9rn289.gif"
    },
}

answers = {
    0:{
        "answer": {"Start":"Neutral","End":"Top"},
        "submission":{}
    },
    1:{
        "answer": 3,
        "submission":None
    },
    2:{
        "answer": 3,
        "submission":None
    },
    3:{
        "answer": "Takedown",
        "submission":None
    },
    4:{
        "answer": {"Before":"Bottom","After":"Top"},
        "submission": {}
    },
}

lessons = {
    0:{
        "lesson_id":"0",
        "Section":"Neutral",
        "title":"Positions",
        "main-text":"Every match starts in “Neutral”, where both wrestlers are on their feet facing each other.",
        "sub-text":[
            "Crouched down in their “stances”",
            "Looking for offensive and defensive scoring"
        ],
        "expanded-text":[
            "Wrestlers in this position try to establish grip control and test each other’s balance.",
            "Effective hand-fighting here often determines who will initiate the first takedown attempt."
        ],
        "image":"https://i.postimg.cc/Ss7hBMts/neutral-lesson.jpg",
    },
    1:{
        "lesson_id":"1",
        "Section":"Top",
        "title":"Positions",
        "main-text":"“Top” is when one wrestler is on top of the other (Black Singlet)",
        "sub-text":[
            "May be chosen as starting position for 2nd and 3rd periods",
            "Results after one wrestler takes the other from neutral to the mat"
        ],
        "expanded-text":[
            "From the top, the wrestler aims to ride their opponent and look for back-exposure (nearfall).",
            "Proper leg-riding and hip pressure increase control and set up near-fall opportunities."
        ],
        "image":"https://i.postimg.cc/15W9RDRV/top-lesson.jpg",
    },
    2:{
        "lesson_id":"2",
        "Section":"Bottom",
        "title":"Positions",
        "main-text":"“Bottom” is when one wrestler is under the other (White Singlet)",
        "sub-text":[
            "May be chosen as starting position for 2nd and 3rd periods",
            "Results after one wrestler takes the other from neutral to the mat"
        ],
        "expanded-text":[
            "On bottom, the wrestler works to escape or reverse to regain advantage.",
            "Quick stand-ups are key techniques to break free from under control."
        ],
        "image":"https://i.postimg.cc/x8n08RbM/bottom-lesson.jpg",
    },
    3:{
        "lesson_id":"3",
        "Section":"review",
        "title":"Positions",
        "type": "drag_drop",
        "text": "What position is the wrestler in Pennstate (Dark Blue) in before and after the move?",
        "drag_options": ["Top", "Bottom", "Neutral"],
        "drop_options": ["Start", "End"],
        "media": "https://cdn.vox-cdn.com/uploads/chorus_asset/file/15869679/tumblr_plfz1txHj31qbrivdo1_400.gif",
        "next_lesson": "4",
    },
    4:{
        "lesson_id":"4",
        "Section":"Takedown Scoring",
        "title":"Takedown",
        "main-text":"“Takedown” is when one wrestler takes another down from neutral onto the mat.",
        "sub-text":[
            "3 Points Awarded to Blue assuming he brings yellow to the ground"
        ],
        "expanded-text":[
            "A takedown is called by the ref once they deem a wrestler has gained control of the other.",
            "This can be vague and result in confusing situations."
        ],
        "image":"https://i.postimg.cc/QtTPCNd1/roman-bravo-young-ragusin.avif",
    },
    5:{
        "lesson_id":"5",
        "Section":"Takedown Scoring",
        "title":"Takedown",
        "main-text":"The wrestler in yellow demonstrates control",
        "sub-text":[
            "He hooks the ankle of his opponent!"
        ],
        "image":"https://i.postimg.cc/bJVXDVxf/Wrestling-Takedown-GIF-by-NCAA-Championships-1.gif",
    },
    6:{
        "lesson_id":"6",
        "Section":"review",
        "title":"Takedown",
        "type": "textbox",
        "text": "How many points were scored by blue in this exchange?", 
        "media":  "https://media3.giphy.com/media/6eE0hofFR3wpA7kyv7/200.gif?cid=6c09b952r3ska4pxkitg92kn7t2h3rwdxqcuuszaxztb3tvl&ep=v1_internal_gif_by_id&rid=200.gif&ct=g",
        "next_lesson": "7",
    },
    7:{
        "lesson_id":"7",
        "Section":"Nearfall Scoring",
        "title":"Nearfall",
        "main-text":"“Nearfall” or Back points are scored when a wrestler’s back is exposed within a 45° angle from the mat.",
        "sub-text":[
            "Points are counted roughly every second by the referee, visualized by a sweeping motion with their arm.",
            "Minimum of 2 points.",
            "Maximum of 4 points.",
            "Wrestler in black is scoring back points."
        ],
        "expanded-text":[
            "The referee awards nearfall when a wrestler holds their opponent’s back close to the mat.",
            "Longer exposures yield more points, so timing and pressure are crucial."
        ],
        "image":"https://i.postimg.cc/cH32JWth/temp-Image-Iy11-C0.avif",
    },
    8:{
        "lesson_id":"8",
        "Section": "review",
        "title":"Nearfall",
        "type": "multiple_choice",
        "text": "What are the maximum amount of nearfall points scored here?", 
        "media": "https://slack-imgs.com/?c=1&url=http%3A%2F%2Fi.imgur.com%2FJfDYplF.gif",
        "options": ["2", "4", "3"],
        "next_lesson": "9",
    },
    9:{
        "lesson_id":"9",
        "Section":"Reversals Scoring",
        "title":"Reversals",
        "main-text":"A “Reversal” is when the wrestler on the bottom gains control over their opponent, ending up on top.",
        "sub-text":[
            "Reversals are worth 2 points.",
            "They demonstrate a significant change in control during the match.",
            "Wrestler in red performs a reversal."
        ],
        "expanded-text":[
            "Reversals highlight a dramatic shift in control by turning the bottom wrestler into the aggressor.",
            "Quick switches and sit-outs often catch the top wrestler off guard."
        ],
        "image":"https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExcng5YW8ydWgyb3NhNG91cmI3ZnRlaGJwYzdldmtmbXdqajA0cDU4ZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xT1R9XsuEBIyFgplcI/giphy.gif",
    },
    10:{
        "lesson_id":"10",
        "Section":"review",
        "title":"Reversals",
        "type": "multiple_choice",
        "text": "What type of score was this from the wrestler in Red?", 
        "media":  "https://coeweb.calstatela.edu//2019f/edit/qroura/5600/webapp/Image/Reversal3.gif",
        "options": ["Nearfall", "Escape", "Takedown", "Reversal"],
        "next_lesson": "11",
    },
    11:{
        "lesson_id":"11",
        "Section":"Escapes Scoring",
        "title":"Escapes",
        "main-text":"An “Escape” is when the wrestler on the bottom gets away from their opponent and returns to a neutral position.",
        "sub-text":[
            "Escapes are worth 1 point.",
            "They demonstrate the ability to break free from an opponent’s control.",
            "Wrestler in light grey performs an escape to return to neutral."
        ],
        "expanded-text":[
            "A successful escape returns you to neutral, preventing further back-exposure points.",
            "You'l see the bottom wrestler stand-up and break out from under control."
        ],
        "image":"https://i.makeagif.com/media/7-13-2021/rBSzRR.gif",
    }
}

rev_answers = {
    3:{
        "review_id": "3",
        "answer": {"Start":"Neutral","End":"Top"},
        "submission":{}
    },
    6:{
        "review_id": "6",
        "answer": 3,
        "submission":None
    },
    8:{
        "review_id": "8",
        "answer": 4,
        "submission":None
    },
    10:{
        "review_id": "10",
        "answer": "Reversal",
        "submission":None
    },
}


@app.route('/')
def home():
    return render_template('home.html', nav_lessons=get_nav_sections())

def get_nav_sections():
    unique_sections = {}
    for k, v in lessons.items():
        section = v['title']
        if section not in unique_sections:
            unique_sections[section] = v
    return unique_sections.values()



@app.route('/quiz/<int:question_id>', methods=['GET', 'POST'] )
def quiz(question_id):
    if question_id>=len(questions):
        return redirect(url_for('quiz_score'))
    
    question = questions[question_id]
    question_type = question['type']
    is_correct = False
    
    if request.method == 'POST':
        if(question_type == "drag_drop"):
            submission = dict(request.form)
            for i in submission:
                if(len(submission[i].split(',')) > 1):
                    submission[i] = submission[i].split(',')
            answers[question_id]["submission"] = submission
            is_correct = answers[question_id]["answer"] == submission
            return jsonify({'correct': is_correct, 'correct_answer': answers[question_id]["answer"]})
        elif question_type == 'textbox':
            submission = request.form.get('answer').strip()
            answers[question_id]["submission"] = submission
            is_correct = str(answers[question_id]["answer"]) == str(submission)
            return jsonify({'correct': is_correct, 'correct_answer': answers[question_id]["answer"]})
        elif question_type == 'multiple_choice':
            submission = request.form.get('answer')
            answers[question_id]["submission"] = submission
            is_correct = str(answers[question_id]["answer"]) == str(submission)
            return jsonify({'correct': is_correct, 'correct_answer': answers[question_id]["answer"]})
        return redirect(url_for('quiz', question_id=question_id+1))
    
    template = f"quiz_{question['type']}.html"
    return render_template(template, question=question, question_id=question_id, nav_lessons=get_nav_sections(), total_questions=len(questions))

@app.route('/quiz_score')
def quiz_score():
    score = 0
    for i in answers:
        if(questions[i]["type"] == "drag_drop"):
            if(str(answers[i]["answer"]) == str(answers[i]["submission"])):
                score += 1
        elif(questions[i]["type"] == "multiple_choice"):
            if(str(answers[i]["answer"]) == str(answers[i]["submission"])):
                score += 1
        else:
            if(str(answers[i]["answer"]) == str(answers[i]["submission"])):
                score += 1
    return render_template('quiz_score.html', score=score, answers=answers, questions=questions, total_questions=len(questions), nav_lessons=get_nav_sections())
  

@app.route('/learn/<int:lesson_id>', methods=['GET'])
def learn(lesson_id):
    if lesson_id < 0 or lesson_id >= len(lessons):
        return redirect(url_for('quiz', question_id=0))  # Redirect to quiz if out of bounds
    
    lesson = lessons[lesson_id]
    
    # Check if the lesson is a review section
    if lesson.get("Section") == "review":
        review_id = int(lesson["lesson_id"])
        answer = rev_answers.get(review_id, {}).get("answer", None)
        template = f"review_{lesson['type']}.html"
        return render_template(template, question=lesson, question_id=review_id, total_questions=len(lessons), nav_lessons=get_nav_sections(), correct_answer=answer)
    
    # Render regular lesson
    return render_template('learn.html', lesson=lesson, lesson_id=lesson_id, nav_lessons=get_nav_sections(), total_lessons=len(lessons))

@app.route('/review/<int:lesson_id>', methods=['GET', 'POST'])
def review_questions(lesson_id):
    if lesson_id >= len(lessons):
        return redirect(url_for('learn', lesson_id=0))  # Redirect to the first lesson if out of bounds

    review = lessons[lesson_id]
    review_type = review['type']
    is_correct = False

    if request.method == 'POST':
        if review_type == "drag_drop":
            submission = dict(request.form)
            rev_answers[lesson_id]["submission"] = submission
            is_correct = rev_answers[lesson_id]["answer"] == submission
            return jsonify({'correct': is_correct, 'correct_answer': rev_answers[lesson_id]["answer"]})
        elif review_type == 'textbox':
            submission = request.form.get('answer').strip()
            rev_answers[lesson_id]["submission"] = submission
            is_correct = str(rev_answers[lesson_id]["answer"]) == str(submission)
            return jsonify({'correct': is_correct, 'correct_answer': rev_answers[lesson_id]["answer"]})
        elif review_type == 'multiple_choice':
            submission = request.form.get('answer')
            rev_answers[lesson_id]["submission"] = submission
            is_correct = str(rev_answers[lesson_id]["answer"]) == str(submission)
            return jsonify({'correct': is_correct, 'correct_answer': rev_answers[lesson_id]["answer"]})

    template = f"review_{review['type']}.html"
    return render_template(template, question=review, question_id=lesson_id, nav_lessons=get_nav_sections(), total_questions=len(lessons))





@app.route('/log-time', methods=['POST'])
def log_time():
    try:
        raw_data = request.data.decode('utf-8')
        data = json.loads(raw_data)

        content_type = data.get('type')  # 'quiz' or 'lesson'
        content_id = data.get('id')
        time_spent = data.get('time_spent')
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open("user_time_log.csv", "a") as f:
            f.write(f"{content_type},{content_id},{time_spent},{timestamp}\n")

        return jsonify({"status": "logged"}), 200

    except Exception as e:
        print("Log time error:", e)
        return jsonify({"status": "error"}), 400



if __name__ == '__main__':
   app.run(debug = True, port=5001)
