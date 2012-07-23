from flask import Flask,render_template,request
from werkzeug.wrappers import Request,Response
from models.story import Story
from models.shared import HERE_LAT,HERE_LON
import json
from json_encoder import Encoder

app = Flask(__name__)

@app.route('/')
def root():
    """render out homepage, where user can upload a file or search existing"""
    return render_template('home.html',default_lat=HERE_LAT,default_lon=HERE_LON)

@app.route('/stories',methods=['GET','POST'])
def stories():
    if request.method == 'POST':
        #save a story
        uploader = request.values.get('uploader')
        description = request.values.get('desc')
        lat = request.values.get('lat')
        lon = request.values.get('lon')
        files = [request.files[f] for f in request.files]
        story = Story.create(uploader,description,lat,lon,files)
        return Response([json.dumps({'flag':1,'story':story},cls=Encoder,indent=4)],mimetype='application/json')
    elif request.method == 'GET':
        #browse stories
        lat = float(request.values.get('lat',HERE_LAT))
        lon = float(request.values.get('lon',HERE_LON))
        stories = Story.collection.find({'loc':{'$maxDistance':10,'$near':[lat,lon]}}).limit(200)
        return Response([json.dumps({'stories':[s for s in stories]},cls=Encoder)],mimetype='application/json')
