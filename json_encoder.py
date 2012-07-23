#! /usr/bin/python

# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="mark"
__date__ ="$Nov 30, 2011 8:50:18 AM$"

from datetime import datetime
import json
from models.story import Story
try:
    from pymongo.objectid import ObjectId
except ImportError:
    from bson.objectid import ObjectId

class Encoder(json.JSONEncoder):
    def default(self,obj):
        if isinstance(obj,set):
            return list(obj)
        elif isinstance(obj,datetime):
            fmt = '%Y-%m-%dT%H:%M:%SZ'
            return obj.strftime(fmt)
        elif isinstance(obj,ObjectId):
            return str(obj)
        elif isinstance(obj,Story):
            return dict(obj)


