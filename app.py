import os

from flask import Flask, redirect, url_for, session, request, render_template, jsonify, g
from flask.ext.oauth import OAuth
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String



app = Flask(__name__)

app.debug = True
app.secret_key = "SECRET"

engine = create_engine(os.environ.get('DATABASE_URL'), echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
sess = Session()


class Acode(Base):
    __tablename__ = 'acode'

    id = Column(Integer, primary_key=True)
    code = Column(String)

    def __init__(self, code):
         self.code = code

oauth = OAuth()

vk = oauth.remote_app('vkontakte',
    base_url='https://api.vk.com/method/',
    request_token_url=None,
    access_token_url='https://api.vk.com/oauth/token',
    authorize_url='http://api.vk.com/oauth/authorize',
    consumer_key='2904906',
    consumer_secret='xpyuJye6NozdTazuuRvM'
)

@app.before_request
def before_request():
    g.code=getattr(g,'code',None)
    if not 'access_token' in session:
        g.code = sess.query(Acode).last()

@app.route('/')
def hello():
    if g.code:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))

@app.route('/json/<int:offset>')
def jsony(offset):
    if g.code:
        me=vk.get('wall.get?owner_id=771193&count=20&filter=others&offset=%s&access_token=%s' % (offset,g.code))
        return jsonify(result=me.data['response'][1:],
                    access_token = g.code)
    return jsonify(result=None)

@app.route('/login')
def login():
    return vk.authorize(callback=url_for('vk_auth',
        next=request.args.get('next') or request.referrer or None,
        _external=True))

@app.route('/login/authorized')
@vk.authorized_handler
def vk_auth(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['access_token'] = resp['access_token']
    code = Acode(resp['access_token'] )
    sess.add(code)
    sess.commit(code)
    session['oauth_token'] = (resp['access_token'], '')
    return redirect('/')


@vk.tokengetter
def get_vk_oauth_token():
    return session.get('oauth_token')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
