"""Flask OAuth App to connect to host servers such as github, facebook, etc and
execute host server requests
"""
from flask import Flask, redirect, url_for, session, request
from service.utils import get_oauth_app
import logging
from flask import render_template
from config.config import SECRET_KEY, DEBUG, SQLALCHEMY_DATABASE_URI, \
     SQLALCHEMY_DATABASE, SQLALCHEMY_DATABASE_NOTIF
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

# Call Factory function to create OAuth App.
# This can be enhanced to take a custom hostname(github, facebook, etc.)
oauthflaskapp = get_oauth_app('github', app.logger)

@app.route('/')
def index():
    """ First page view of web service

    :return: index html
    """
    return render_template('index.html')


@app.route('/login')
def login():
    """ Login view handler

    :return: Callback to oauth_authorized
    """
    return oauthflaskapp.oauthapp.authorize(callback=url_for('oauth_authorized',
                                                             next=request.args.get('next') \
                                                             or request.referrer or None,
                                                             _external=True))


@app.route('/login/authorized')
@oauthflaskapp.oauthapp.authorized_handler
def oauth_authorized(resp):
    """ Callback from host server login page

    :param resp:
    :return: login html
    """
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
        resp_status = oauthflaskapp.handle_oauth_login()
        app.logger.info('github_authorized: Login Authorization {} {}'.\
                        format(resp_status, session['oauth_token']))
        return render_template('login.html')
    except Exception as exc:
        app.logger.exception('handleoauthlogin : {} {}'.format('Login Authorization failed', exc))
        return render_template('500.html')


@oauthflaskapp.oauthapp.tokengetter
def get_oauth_token():
    """ Retrieve OAuth token for service

    :return: host server access token
    """
    return session.get('oauth_token')


@app.route('/fork', methods=['POST', 'GET'])
def create_fork():
    """ Create repository fork

    :return: fork html
    """
    try:
        if not current_user.is_anonymous:
            return redirect(url_for('login'))
        resp_status = oauthflaskapp.create_fork(request)
        app.logger.info('create_fork : Successfully created fork {} status {}'.\
                        format(session['oauth_token'], resp_status))
        return render_template('fork.html')
    except ValueError as err:
        app.logger.exception('create_fork : {} {}'.format('Fork creation failed', err))
        return render_template('malformeddata.html')
    except Exception as exc:
        app.logger.exception('create_fork : {} {}'.format('Fork creation failed', exc))
        return render_template('500.html')

# Handle user logout
@app.route('/logout')
def logout():
    """ Logout handler

    :return: index html
    """
    logout_user()
    return redirect(url_for('index'))


@app.errorhandler(404)
def notfounderror(error):
    """ Handle not found error

    :param error:
    :return: 404 html
    """
    return render_template('404.html'), 404


@app.errorhandler(500)
def internalerror(error):
    """ Handle internal error

    :param error:
    :return: 500 html
    """
    db.session.rollback()
    return render_template('500.html'), 500


class User(UserMixin, db.Model):
    """ User database table

    """
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
