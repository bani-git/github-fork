from service.app_factory import GithubOAuthApp, FacebookOAuthApp

# Dictionary mapping the host server name to the OAuthApp
factorymap = {
    'github' : GithubOAuthApp,
    'facebook' : FacebookOAuthApp,
}

# Simple Factory function to create the OAuth App. Can be enhanced to use a Factory Pattern
def getOAuthApp(hostName, logger):
    cls = factorymap.get(hostName)
    if not cls:
        raise RuntimeError('Fault', 'Incorrect OAuth server name')
    else:
        oauthapp = cls(logger)
        oauthapp.createoauthapp()
        return oauthapp

