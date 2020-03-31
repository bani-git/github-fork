from config.enums import FlaskOAuthServerConfig

SECRET_KEY = 'development key'
DEBUG = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
SQLALCHEMY_DATABASE = 'SQLALCHEMY_DATABASE_URI'
SQLALCHEMY_DATABASE_NOTIF = 'SQLALCHEMY_TRACK_MODIFICATIONS'

# OAuth server config by host type
oauthserverconfig = {
    'github': {
        FlaskOAuthServerConfig.CLIENT_ID: 'b41fff3e49ea5b30ef6b',
        FlaskOAuthServerConfig.CLIENT_SECRET: 'bd0623dccf8e8d1f46c726f0ad334e8d87cc2bf3',
        FlaskOAuthServerConfig.REQUEST_TOKEN: {'scope': 'public_repo'},
        FlaskOAuthServerConfig.BASE_URL:'https://api.github.com/api/v3',
        FlaskOAuthServerConfig.REQUEST_TOKEN_URL: None,
        FlaskOAuthServerConfig.ACCESS_TOKEN_METHOD: 'POST',
        FlaskOAuthServerConfig.ACCESS_TOKEN_URL: 'https://github.com/login/oauth/access_token',
        FlaskOAuthServerConfig.AUTH_URL: 'https://github.com/login/oauth/authorize'
    },
    'facebook': {

    },
    'twitter': {

    },
}