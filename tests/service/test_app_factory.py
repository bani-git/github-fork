from unittest import TestCase
import requests
from flask_oauthlib.client import OAuthRemoteApp
from config.enums import FlaskOAuthServerConfig
from unittest.mock import Mock, patch
import unittest
import logging
from service.utils import getOAuthApp


class GithubOAuthAppTest(TestCase):
    def setUp(self):
        self.githubapp = getOAuthApp('github', logging.getLogger())

    def test_createoauthappSuccess(self):
        self.githubapp.createoauthapp()
        self.assertIsInstance(self.githubapp.oauthapp, OAuthRemoteApp)

    def test_appconfig(self):
        self.assertIsNotNone(self.githubapp.appconfig.get(FlaskOAuthServerConfig.CLIENT_ID))
        self.assertIsNotNone(self.githubapp.appconfig.get(FlaskOAuthServerConfig.CLIENT_SECRET))
        self.assertIsNotNone(self.githubapp.appconfig.get(FlaskOAuthServerConfig.REQUEST_TOKEN))
        self.assertIsNotNone(self.githubapp.appconfig.get(FlaskOAuthServerConfig.BASE_URL))
        self.assertIsNotNone(self.githubapp.appconfig.get(FlaskOAuthServerConfig.ACCESS_TOKEN_METHOD))
        self.assertIsNotNone(self.githubapp.appconfig.get(FlaskOAuthServerConfig.ACCESS_TOKEN_URL))
        self.assertIsNotNone(self.githubapp.appconfig.get(FlaskOAuthServerConfig.AUTH_URL))

    @patch('flask_oauthlib.client.OAuthRemoteApp.get')
    def test_handleoauthloginSuccess(self, mock_get):
        data = {'id': '1234', 'login': 'test login'}
        mock_resp = Mock()
        mock_resp.data = data
        mock_get.return_value = mock_resp
        returnmsg = self.githubapp.handleoauthlogin()
        self.assertEqual(returnmsg, 'Logged in as id={} name={}'.format('1234', 'test login '))

    @patch('flask_oauthlib.client.OAuthRemoteApp.get')
    def test_handleoauthloginFailure(self, mock_get):
        json_data = {'id': '1234', 'name': 'test login'}
        mock_resp = requests.models.Response()
        mock_resp.data = json_data
        mock_resp.status_code = 404
        mock_get.return_value = mock_resp
        with self.assertRaises(requests.exceptions.HTTPError) as err_msg:
            self.githubapp.handleoauthlogin()
            mock_resp.raise_for_status()

    @patch('flask_oauthlib.client.OAuthRemoteApp.post')
    def test_createforkSuccess(self, mock_get):
        data = {'id': '1234', 'login': 'test login', 'full_name': 'full name'}
        mock_resp = Mock()
        mock_resp.data = data
        mock_get.return_value = mock_resp
        request = Mock()
        request.args = {'repoowner' : 'test owner', 'reponame' : 'repo name'}
        returnmsg = self.githubapp.createfork(request)
        self.assertEqual(returnmsg, 'Created fork for repository with name {} '.format('full name'))

    @patch('flask_oauthlib.client.OAuthRemoteApp.post')
    def test_createforkFailure(self, mock_get):
        data = {'id': '1234', 'login': 'test login'}
        mock_resp = Mock()
        mock_resp.data = data
        mock_get.return_value = mock_resp
        request = Mock()
        request.args = {'repoowner': 'test owner', 'reponame' : 'repo name'}
        with self.assertRaises(ValueError) as err_msg:
            self.githubapp.createfork(request)
            mock_resp.raise_for_status()

if __name__ == '__main__':
    unittest.main()
