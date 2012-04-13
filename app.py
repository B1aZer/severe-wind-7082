import os

from flask import Flask, redirect, url_for, session, request
from flask.ext.oauth import OAuth
app = Flask(__name__)

app.debug = True
app.secret_key = "SECRET"


oauth = OAuth()

vk = oauth.remote_app('vkontakte',
    base_url='https://api.vk.com/method/',
    request_token_url=None,
    access_token_url='https://api.vk.com/oauth/token',
    authorize_url='http://api.vk.com/oauth/authorize',
    consumer_key='2904906',
    consumer_secret='xpyuJye6NozdTazuuRvM'
)

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/login')
def login():
    return vk.authorize(callback='http://skdy.org/illarionov')

@app.route('/login/authorized')
@vk.authorized_handler
def vk_auth(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['oauth_token'] = (resp['access_token'], '')
    me = vk.get('wall.get?owner_id=771193')
    return 'Logged in as id=%s name=%s redirect=%s' % \
        (me.data['id'], me.data['name'], request.args.get('next'))


@vk.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
