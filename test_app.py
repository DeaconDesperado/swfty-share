import os
from listener import application
from config import TestingConfig
import unittest
import json
import logging
import logging.handlers
import re

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
sh = logging.StreamHandler()
log_format = logging.Formatter('\n%(asctime)s - %(message)s')
sh.setFormatter(log_format)
log.addHandler(sh)

class PXQuiltTest(unittest.TestCase):

    def setUp(self):
        application.config.from_object(TestingConfig)
        application.testing = True
        self.app = application.test_client()

    def test_story(self):
        self.app.post('/stories',data={
            'uploader':'unittest',
            'desc':'This is a story',
            'lat':41.167041,
            'lon':-73.204833999
        })

def tearDownModule():
    log.info('dropping database')

if __name__ == '__main__':
    unittest.main()
