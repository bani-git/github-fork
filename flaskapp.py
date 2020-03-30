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
flaskapp = Flask(__name__)
flaskapp.debug = DEBUG
flaskapp.secret_key = SECRET_KEY
flaskapp.config[SQLALCHEMY_DATABASE] = SQLALCHEMY_DATABASE_URI
flaskapp.config[SQLALCHEMY_DATABASE_NOTIF] = False

# Create database to hold user data
db = SQLAlchemy(flaskapp)
lm = LoginManager(flaskapp)
lm.login_view = 'index'

# Call Factory function to create OAuth App. This can be enhanced to take a custom hostname(github, facebook, etc.)
oauthflaskapp = getOAuthApp('github', flaskapp.logger)


@flaskapp.route('/')
def index():
    return render_template('index.html')


@flaskapp.route('/login')
def login():
    return oauthflaskapp.oauthapp.authorize(callback=url_for('github_authorized',
                                                             next=request.args.get('next') or request.referrer or None,
                                                             _external=True))


@flaskapp.route('/login/authorized')
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
        flaskapp.logger.info('github_authorized: Login Authorization {} {}'.format(returnmsg, session['oauth_token']))
        return render_template('login.html')
    except Exception as exc:
        flaskapp.logger.exception('handleoauthlogin : {} {}'.format('Login Authorization failed', exc))
        return render_template('500.html')


@oauthflaskapp.oauthapp.tokengetter
def get_oauth_token():
    return session.get('oauth_token')


@flaskapp.route('/login/fork', methods=['POST', 'GET'])
def create_fork():
    try:
        if not current_user.is_anonymous:
            return redirect(url_for('login'))
        returnmsg = oauthflaskapp.createfork(request)
        flaskapp.logger.info('create_fork : Successfully created fork {} {}'.format(returnmsg, session['oauth_token']))
        return render_template('fork.html')
    except ValueError as err:
        return render_template('malformeddata.html')
    except Exception as exc:
        flaskapp.logger.exception('create_fork : {} {}'.format('Fork creation failed', exc))
        return render_template('500.html')

@flaskapp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@flaskapp.errorhandler(404)
def notfounderror(error):
    return render_template('404.html'), 404


@flaskapp.errorhandler(500)
def internalerror(error):
    db.session.rollback()
    return render_template('500.html'), 500

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
    flaskapp.run()
