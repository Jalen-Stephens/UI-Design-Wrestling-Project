from flask import Flask
from flask import render_template
from flask import Response, request, jsonify

import re
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/test')
def test():
    return "Test page is working!"

if __name__ == '__main__':
   app.run(debug = True, port=5001)
