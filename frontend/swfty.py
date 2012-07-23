from flask import Flask,render_template,request
from werkzeug.wrappers import Request,Response

app = Flask(__name__)

@app.route('/')
def root():
    """render out homepage, where user can upload a file or search existing"""
    return render_template('home.html')

