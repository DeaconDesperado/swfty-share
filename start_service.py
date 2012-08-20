"""Creates the WSGI application object.  If ran directly, fires a test instance on port 5050"""
from swfty.frontend.swfty_frontend import app
from werkzeug.serving import run_simple
import sys
sys.path.append('/home/mark/projects')

application = app
if __name__ == '__main__':
    application.debug = True
    run_simple('localhost',5050,application,use_reloader=True,use_debugger=True)
