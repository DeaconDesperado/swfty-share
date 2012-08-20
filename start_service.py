"""Creates the WSGI application object.  If ran directly, fires a test instance on port 5050"""
from swfty.frontend.swfty_frontend import app
from werkzeug.serving import run_simple
import sys

from swfty.blueprints.fb_auth import FB
from swfty.blueprints.twitter import Twitter

sys.path.append('/home/mark/projects')

app.register_blueprint(FB,url_prefix='/oauth/facebook',subdomain='www')
app.register_blueprint(Twitter,url_prefix='/oauth/twitter',subdomain='www')
app.register_blueprint(FB,url_prefix='/oauth/facebook',subdomain='')
app.register_blueprint(Twitter,url_prefix='/oauth/twitter',subdomain='')

application = app
if __name__ == '__main__':
    application.debug = True
    run_simple('localhost',5050,application,use_reloader=True,use_debugger=True)
