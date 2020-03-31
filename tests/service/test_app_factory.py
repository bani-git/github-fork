from unittest import TestCase
import requests
from flask_oauthlib.client import OAuthRemoteApp
from config.enums import FlaskOAuthServerConfig
from unittest.mock import Mock, patch
import unittest
import logging
from service.utils import get_oauth_app
from http import HTTPStatus

class GithubOAuthAppTest(TestCase):
    def setUp(self):
        self.githubapp = get_oauth_app('github', logging.getLogger())

    def test_createoauthappSuccess(self):
        self.githubapp.create_oauth_app()
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
        mock_resp.status = HTTPStatus.OK
        mock_get.return_value = mock_resp

        resp_status = self.githubapp.handle_oauth_login()
        self.assertEqual(resp_status, HTTPStatus.OK)

    @patch('flask_oauthlib.client.OAuthRemoteApp.get')
    def test_handleoauthloginFailure(self, mock_get):
        mock_resp = Exception()
        with self.assertRaises(Exception) as err_msg:
            resp_status = self.githubapp.handle_oauth_login()
            mock_resp.raise_for_status()

    @patch('flask_oauthlib.client.OAuthRemoteApp.post')
    def test_createforkSuccess(self, mock_get):
        data = {'id': '1234', 'login': 'test login', 'full_name': 'full name'}
        mock_resp = Mock()
        mock_resp.data = data
        mock_resp.status = HTTPStatus.ACCEPTED
        mock_get.return_value = mock_resp
        request = Mock()
        request.args = {'repoowner' : 'test owner', 'reponame' : 'repo name'}
        resp_status = self.githubapp.create_fork(request)
        self.assertEqual(resp_status, HTTPStatus.ACCEPTED)

    @patch('flask_oauthlib.client.OAuthRemoteApp.post')
    def test_createforkFailure(self, mock_get):
        data = {'id': '1234', 'login': 'test login'}
        mock_resp = Mock()
        mock_resp.data = data
        mock_get.return_value = mock_resp
        request = Mock()
        request.args = {'repoowner': 'test owner', 'reponame' : 'repo name'}
        with self.assertRaises(ValueError) as err_msg:
            self.githubapp.create_fork(request)
            mock_resp.raise_for_status()

if __name__ == '__main__':
    unittest.main()
