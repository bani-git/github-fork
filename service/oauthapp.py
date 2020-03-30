import abc


class OAuthApp(abc.ABC):

    @abc.abstractmethod
    def handleoauthlogin(self, **kwargs):
        pass

    @abc.abstractmethod
    def handleoauthlogout(self, **kwargs):
        pass


