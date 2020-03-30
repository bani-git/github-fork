from service.singleton import singleton
from config.enums import FlaskOAuthServerConfig
from config.config import oauthserverconfig
from flask_oauthlib.client import OAuth
from service.oauthapp import OAuthApp
from requests.exceptions import HTTPError


@singleton
class GithubOAuthApp(OAuthApp):
    appconfig = oauthserverconfig.get('github')

    def __init__(self, logger):
        self.logger = logger
        #self.createoauthapp()

    def createoauthapp(self):
        try:
            oauth = OAuth()
            self.oauthapp = oauth.remote_app(
                'github',
                consumer_key=self.appconfig.get(FlaskOAuthServerConfig.CLIENT_ID),
                consumer_secret=self.appconfig.get(FlaskOAuthServerConfig.CLIENT_SECRET),
                request_token_params=self.appconfig.get(FlaskOAuthServerConfig.REQUEST_TOKEN),
                base_url=self.appconfig.get(FlaskOAuthServerConfig.BASE_URL),
                request_token_url=None,
                access_token_method=self.appconfig.get(FlaskOAuthServerConfig.ACCESS_TOKEN_METHOD),
                access_token_url=self.appconfig.get(FlaskOAuthServerConfig.ACCESS_TOKEN_URL),
                authorize_url=self.appconfig.get(FlaskOAuthServerConfig.AUTH_URL),
            )
        except Exception as exc:
            if self.logger:
                self.logger.exception('createoauthapp : Exception creating the OAuth App {}'.format(exc))
            raise

    def _logmessage(self, message, exc):
        if self.logger:
            self.logger.exception(
                'handleoauthlogin : {} {}'.format(message, exc))

    def handleoauthlogin(self):
        try:
            resp = self.oauthapp.get('/user')
            return 'Logged in as id={} name={} '.format(resp.data.get('id'), resp.data.get('login'))
        except HTTPError as http_err:
            self._logmessage('handleoauthlogin : HTTP Error occurred in a Github GET request', http_err)
            raise
        except Exception as exc:
            self._logmessage('handleoauthlogin : Exception when getting User details from GitHub ', exc)
            raise


    def createfork(self, request):
        try:
            repoowner = request.args.get('repoowner')
            reponame = request.args.get('reponame')
            if repoowner and reponame:
                self.logger.info('create fork repoowner {} repo name {} '.format(repoowner, reponame))
                resp = self.oauthapp.post('/repos/' + repoowner + '/' + reponame + '/forks', content_type='application/json')
                if resp.data and resp.data.get('full_name'):
                    self.logger.info(' createfork data {} '.format(resp.data.get('full_name')))
                    return 'Created fork for repository from user {} '.format(resp.data.get('full_name'))
                else:
                    self.logger.info('Incorrect Repository Name or Owner Name'.format(resp.data))
                    raise ValueError('Incorrect Repository Name or Owner Name'.format(resp.data))
            else:
                self.logger.info('Missing Repository Name {} or Owner Name {} '.format(reponame, repoowner))
                raise ValueError('Missing Repository Name {} or Owner Name {} '.format(reponame, repoowner))
        except Exception as exc:
            self._logmessage('handleoauthlogin : Exception when getting User details from GitHub ', exc)
            raise


    def handleoauthlogout(self, **kwargs):
        pass


@singleton
class FacebookOAuthApp(OAuthApp):
    pass

@singleton
class TwitterOAuthApp(OAuthApp):
    pass