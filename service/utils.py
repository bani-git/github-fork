from service.app_factory import GithubOAuthApp, FacebookOAuthApp

# Dictionary mapping the host server name to the OAuthApp
factorymap = {
    'github' : GithubOAuthApp,
    'facebook' : FacebookOAuthApp,
}


def get_oauth_app(hostName, logger):
    """ Simple Factory function to create the OAuth App.
    Can be enhanced to use a Factory Pattern

    :param hostName: OAuth server host name
    :param logger: Flask app logger
    :return: OAuthlib App
    """
    cls = factorymap.get(hostName)
    if not cls:
        raise RuntimeError('Fault', 'Incorrect OAuth server name')
    else:
        oauthapp = cls(logger)
        oauthapp.create_oauth_app()
        return oauthapp

