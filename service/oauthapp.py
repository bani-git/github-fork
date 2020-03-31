import abc

# OAuth app interface defining the core use cases that need to be supported by this Flask OAuth App
class OAuthApp(abc.ABC):

    @abc.abstractmethod
    def handle_oauth_login(self, **kwargs):
        pass



