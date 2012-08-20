import socket

production_hostnames = ['byakhee.deacondesperado.com']

class Config(object):
    DEBUG = False
    TESTING = False
    GOOGLE_MAPS_KEY = "AIzaSyAOOhzdhnps3SeCty2jzt8Ne2wbnvlSCrw"
    AVATAR_DIMENSIONS = (128,128)
    TW_OAUTH_KEY = 'l3bppwuA7CmjgePWckSZQ'
    TW_OAUTH_SECRET = 'hsSJM3Qi3Ykx44ayxXXMU9mOoXCZGI6a9jIHEnb2Ls'
    SECRET_KEY = 'antwerp'

    FB_APP_ID = '503900486304002'
    FB_APP_SECRET = '892f83df808b1432a79e34bcece9866e'

class ProductionConfig(Config):
    MONGO_URI = 'mongodb://byakhee.deacondesperado.com/'
    MONGO_DB = 'swfty'
    SERVER_NAME = 'swfty.com:80'

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    MONGO_URI = 'mongodb://byakhee.deacondesperado.com/'
    MONGO_DB = 'swfty_staging'
    SERVER_NAME = 'swfty.local:5050'


class UnitTestingConfig(TestingConfig):
    MONGO_DB = 'swfty_unittest'

if socket.gethostname() in production_hostnames:
    CONFIGURATION = ProductionConfig
else:
    CONFIGURATION = TestingConfig

