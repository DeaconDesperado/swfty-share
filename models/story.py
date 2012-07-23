from minimongo import Model,Index
import pymongo
from swfty.models.shared import MONGO_URI,MONGO_DATABASE

class Story(Model):
    """The base model for all geo stories"""
    class Meta:
        database = MONGO_DATABASE
        collection = 'stories'
        host = MONGO_URI
        indices = (
            #Index([('loc',pymongo.GEO2D)])
        )

