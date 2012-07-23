from swfty.frontend.swfty import app
from werkzeug.serving import run_simple

application = app
if __name__ == '__main__':
    application.debug = True
    run_simple('localhost',5050,application,use_reloader=True,use_debugger=True)
