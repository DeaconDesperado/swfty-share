from flask import Flask, redirect, url_for, session, request,Blueprint
from flaskext.oauth import OAuth
from werkzeug.serving import run_simple
from pxquilt.config import CONFIGURATION

FACEBOOK_APP_ID = CONFIGURATION.FB_APP_ID 
FACEBOOK_APP_SECRET = CONFIGURATION.FB_APP_SECRET

FB = Blueprint('facebook',__name__)

oauth = OAuth()

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': 'email'}
)


@FB.route('/')
def index():
    return redirect(url_for('.login'))


@FB.route('/login')
def login():
    return facebook.authorize(callback=url_for('.facebook_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True))


@FB.route('/login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['oauth_token'] = (resp['access_token'], '')
    me = facebook.get('/me')
    return 'Logged in as id=%s name=%s redirect=%s' % \
        (me.data['id'], me.data['name'], request.args.get('next'))


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')
