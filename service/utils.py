from service.app_factory import GithubOAuthApp, FacebookOAuthApp


factorymap = {
    'github' : GithubOAuthApp,
    'facebook' : FacebookOAuthApp,
}

# Factory function to create the OAuth App
def getOAuthApp(hostName, logger):
    cls = factorymap.get(hostName)
    if not cls:
        raise RuntimeError('Fault', 'Incorrect OAuth server name')
    else:
        oauthapp = cls(logger)
        oauthapp.createoauthapp()
        return oauthapp

