from flask import Blueprint, render_template, abort, redirect, request, g, session, url_for
import json
from werkzeug.wrappers import Request,Response
from functools import wraps
from twython import Twython
from pymongo.errors import DuplicateKeyError
from passlib.hash import sha256_crypt

from pxquilt.config import CONFIGURATION
from pxquilt.models.user import User

Twitter = Blueprint('twitter',__name__)

@Twitter.route('/oauth/twitter')
def oauth_twitter():
    """
    Go to twitter and prompt for permissions if necessary
    """
    t = Twython(
            app_key=CONFIGURATION.TW_OAUTH_KEY,
            app_secret=CONFIGURATION.TW_OAUTH_SECRET,
            callback_url=url_for('.save_twitter_user',_external=True)
    )
    auth_props = t.get_authentication_tokens()
    session['request_token'] = auth_props
    return redirect(auth_props['auth_url'])


@Twitter.route('/login/twitter')
def save_twitter_user():
    """
    Save the user received from twitter auth or log them in if already registered
    """
    t = Twython(
            app_key=CONFIGURATION.TW_OAUTH_KEY,
            app_secret=CONFIGURATION.TW_OAUTH_SECRET,
            oauth_token=session['request_token']['oauth_token'],
            oauth_token_secret=session['request_token']['oauth_token_secret'],
    )
    authorized_tokens = t.get_authorized_tokens()
    try:
        user = User.collection.find_one({'username':authorized_tokens['screen_name']})
        if user:
            session['user'] = user
        else:
            #create a new user via twitter
            #oauth = dict(authorized_tokens.items() + dict(provider='twitter').items())
            oauth = {'twitter': dict(authorized_tokens.items() + dict(auth=True).items())}
            session['user'] = User.create(username=authorized_tokens['screen_name'],oauth=oauth)
            print session['user']
        return redirect(url_for('.root'))
    except DuplicateKeyError:
        #user is trying to reinsert
        return 'fail'

