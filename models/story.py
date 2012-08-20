from minimongo import Model,Index
import pymongo
from gridfs import GridFS
from datetime import datetime
from swfty.config import CONFIGURATION


class Story(Model):
    """The base model for all geo stories"""
    class Meta:
        database = CONFIGURATION.MONGO_DB
        collection = 'stories'
        host = CONFIGURATION.MONGO_URI
        indices = (
            Index([('loc',pymongo.GEO2D)]),
        )

    @staticmethod
    def getgridfs():
        return GridFS(Story.database,'stories_files')

    @staticmethod
    def create(uploader,description,lat,lon,files=[]):
        """create a new story and add all files associated with it"""
        story_data = {
            'uploader':uploader,
            'description':description,
            'loc':[float(lat),float(lon)],
            'files':[],
            'created':datetime.utcnow()
        }
        story = Story(story_data)
        story.save()
        for file_obj in files:
            story.save_file(file_obj)
        return story

    def save_file(self,file_obj):
        grid = Story.getgridfs()
        grid_file_id = grid.put(file_obj,story_id = self._id,content_type=file_obj.content_type)
        self.files.append(grid_file_id)
        self.save()

    def get_files(self):
        grid = Story.getgridfs()
        files = []
        for file_id in self.files:
            files.append(grid.get(file_id))
        return files
