from flask import Flask,render_template,request
from werkzeug.wrappers import Request,Response

app = Flask(__name__)

@app.route('/')
def root():
    return render_template('root.html')

