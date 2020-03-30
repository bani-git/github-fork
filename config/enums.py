from enum import Enum

# Enumeration defining config parameters for the OAuth app
class FlaskOAuthServerConfig(Enum):
    CLIENT_ID = 1
    CLIENT_SECRET = 2
    REQUEST_TOKEN = 3
    BASE_URL = 4
    REQUEST_TOKEN_URL = 5
    ACCESS_TOKEN_METHOD = 6
    ACCESS_TOKEN_URL = 7
    AUTH_URL = 8

