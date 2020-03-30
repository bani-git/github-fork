from unittest import TestCase

import requests
from flask_oauth import OAuthRemoteApp

from config.enums import FlaskOAuthServerConfig
from service.app_factory import GithubOAuthApp
from unittest.mock import Mock, patch
import unittest
import logging
from flask import jsonify


class GithubOAuthAppTest(TestCase):
    def setUp(self):
        self.githubapp = GithubOAuthApp(logging.getLogger())

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

    def _mock_response(
            self,
            status=200,
            content="CONTENT",
            json_data=None,
            raise_for_status=None):
        mock_resp = Mock()
        # mock raise_for_status call w/optional error
        mock_resp.raise_for_status = Mock()
        if raise_for_status:
            mock_resp.raise_for_status.side_effect = raise_for_status
        # set status code and content
        mock_resp.status_code = status
        mock_resp.content = content
        # add json data if provided
        if json_data:
            mock_resp.json = Mock(
                return_value=json_data
            )
        return mock_resp

    @patch('service.app_factory.requests.get')
    def test_handleoauthloginSuccess(self, mock_get):
        json_data = {'id': '1234', 'name': 'test login'}
        test_token = ('some test access token', '')
        mock_resp = self._mock_response(json_data=json_data)
        mock_get.return_value = mock_resp

        returnmsg = self.githubapp.handleoauthlogin(oauthtoken=test_token)
        self.assertEqual(returnmsg, 'Logged in as id={} name={}'.format('1234', 'test login '))

    @patch('service.app_factory.requests.get')
    def test_handleoauthloginFailure(self, mock_get):
        json_data = {'id': '1234', 'name': 'test login'}
        mock_resp = requests.models.Response()
        mock_resp.status_code = 404
        mock_resp.json = Mock(
            return_value=json_data
        )
        mock_get.return_value = mock_resp
        test_token = ('some test access token', '')
        with self.assertRaises(requests.exceptions.HTTPError) as err_msg:
            self.githubapp.handleoauthlogin(oauthtoken=test_token)
            mock_resp.raise_for_status()


if __name__ == '__main__':
    unittest.main()
