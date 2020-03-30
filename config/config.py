from config.enums import FlaskOAuthServerConfig

SECRET_KEY = 'development key'
DEBUG = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
SQLALCHEMY_DATABASE = 'SQLALCHEMY_DATABASE_URI'
SQLALCHEMY_DATABASE_NOTIF = 'SQLALCHEMY_TRACK_MODIFICATIONS'

oauthserverconfig = {
    'github' : {
        FlaskOAuthServerConfig.CLIENT_ID: '0b5c2b15c791de6195c2',
        FlaskOAuthServerConfig.CLIENT_SECRET: 'b526ce79b92b12c7578c50403370c36775be6ced',
        FlaskOAuthServerConfig.REQUEST_TOKEN : {'scope': 'repo'},
        FlaskOAuthServerConfig.BASE_URL:'https://api.github.com/api/v3',
        FlaskOAuthServerConfig.REQUEST_TOKEN_URL: None,
        FlaskOAuthServerConfig.ACCESS_TOKEN_METHOD: 'POST',
        FlaskOAuthServerConfig.ACCESS_TOKEN_URL: 'https://github.com/login/oauth/access_token',
        FlaskOAuthServerConfig.AUTH_URL: 'https://github.com/login/oauth/authorize'
    },
    'facebook' : {

    },
    'twitter' : {

    },
}