from flask import Flask, redirect, url_for, session, request
from service.utils import getOAuthApp
import logging
from flask import render_template
from config.config import SECRET_KEY, DEBUG, SQLALCHEMY_DATABASE_URI, SQLALCHEMY_DATABASE, SQLALCHEMY_DATABASE_NOTIF
from flask_sqlalchemy import SQLAlchemy
from flask_login.login_manager import LoginManager
from flask_login import logout_user, current_user
from flask_login.mixins import UserMixin

logging.basicConfig(level=logging.DEBUG)

# Create Flask App
app = Flask(__name__)
app.debug = DEBUG
app.secret_key = SECRET_KEY
app.config[SQLALCHEMY_DATABASE] = SQLALCHEMY_DATABASE_URI
app.config[SQLALCHEMY_DATABASE_NOTIF] = False

# Create database to hold user data
db = SQLAlchemy(app)
lm = LoginManager(app)
lm.login_view = 'index'

# Call Factory function to create OAuth App. This can be enhanced to take a custom hostname(github, facebook, etc.)
oauthflaskapp = getOAuthApp('github', app.logger)

# Handle main page view
@app.route('/')
def index():
    return render_template('index.html')


# Handle login page view
@app.route('/login')
def login():
    return oauthflaskapp.oauthapp.authorize(callback=url_for('github_authorized',
                                                             next=request.args.get('next') or request.referrer or None,
                                                             _external=True))

# Handle the callback from the OAuth server(github, facebook, etc)
@app.route('/login/authorized')
@oauthflaskapp.oauthapp.authorized_handler
def github_authorized(resp):
    try:
        if not current_user.is_anonymous:
            return redirect(url_for('login'))
        if resp is None:
            return 'Access denied: reason=%s error=%s' % (
                request.args['error_reason'],
                request.args['error_description']
            )
        session['oauth_token'] = (resp['access_token'], '')
        # Handle OAuth server login
        returnmsg = oauthflaskapp.handleoauthlogin()
        app.logger.info('github_authorized: Login Authorization {} {}'.format(returnmsg, session['oauth_token']))
        return render_template('login.html')
    except Exception as exc:
        app.logger.exception('handleoauthlogin : {} {}'.format('Login Authorization failed', exc))
        return render_template('500.html')

# Handle retrieving the access token on future HTTP requests
@oauthflaskapp.oauthapp.tokengetter
def get_oauth_token():
    return session.get('oauth_token')

# Handle repository fork creation
@app.route('/login/fork', methods=['POST', 'GET'])
def create_fork():
    try:
        if not current_user.is_anonymous:
            return redirect(url_for('login'))
        returnmsg = oauthflaskapp.createfork(request)
        app.logger.info('create_fork : Successfully created fork {} {}'.format(returnmsg, session['oauth_token']))
        return render_template('fork.html')
    except ValueError as err:
        return render_template('malformeddata.html')
    except Exception as exc:
        app.logger.exception('create_fork : {} {}'.format('Fork creation failed', exc))
        return render_template('500.html')

# Handle user logout
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.errorhandler(404)
def notfounderror(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internalerror(error):
    db.session.rollback()
    return render_template('500.html'), 500

# User database table
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(64), nullable=False, unique=True)
    email = db.Column(db.String(64), nullable=True)


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

if __name__ == '__main__':
    db.create_all()
    app.run()
