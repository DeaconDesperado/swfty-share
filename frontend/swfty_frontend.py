"""This module contains the frontend Flask app that will serve HTML output in the browser and handle form submissions via regular HTTP"""
from flask import Flask,render_template,request,abort
from werkzeug.wrappers import Request,Response
from models.story import Story
from models.shared import HERE_LAT,HERE_LON
import json
from json_encoder import Encoder
from bson.objectid import ObjectId
from StringIO import StringIO
import Image

app = Flask(__name__)

def getstories(lat,lon,dist=10,limit=200):
    """Find all the stories in a given radius from a point"""
    stories = Story.collection.find({'loc':{'$maxDistance':dist,'$near':[lat,lon]}}).limit(limit)
    output = []
    for s in stories:
        files = s.get_files()
        s.file_data = []
        for f in files:
            s.file_data.append({'_id':f._id,'mimetype':f.content_type,'size':f.length})
        output.append(s)
    return output

@app.route('/')
def root():
    """render out homepage, where user can upload a file or search existing"""
    return render_template('home.html',default_lat=HERE_LAT,default_lon=HERE_LON)

@app.route('/stories',methods=['GET','POST'])
def stories():
    """Submit a new story/file if post, output those in range if get"""
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
        stories = getstories(lat,lon)
        return Response([json.dumps({'stories':stories},cls=Encoder)],mimetype='application/json')

@app.route('/image/<string:image_id>')
def image(image_id):
    """Content rendered endpt for image mimetypes"""
    grid = Story.getgridfs()
    file_obj = grid.get(ObjectId(image_id))
    if file_obj.content_type not in ['image/jpeg','image/png']:
        abort(400)

    if request.values.get('thumb',None):
        file_obj = resize_image(file_obj,(120,120))
    return Response(file_obj,mimetype=file_obj.content_type)

@app.route('/location_fail')
def location_fail():
    return Reponse('You must have geolocation enabled to use the app')

def resize_image(image,size=(800,600)):
    """Utility function to make thumbnails of images"""
    im = Image.open(image)
    output_buff = StringIO()
    width,height = im.size

    if width > height:
        delta = width-height
        left = int(delta/2)
        upper = 0
        right = height+left
        lower = height
    else:
        delta = height-width
        left = 0
        upper = int(delta/2)
        right = width
        lower = width+upper
    
    im.thumbnail(size, Image.ANTIALIAS)

    im.convert('RGB').save(output_buff, format = 'jpeg', quality=100)
    output_buff.seek(0)
    output_buff.content_type = 'image/jpeg'
    return output_buff

