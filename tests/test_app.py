from app import app, db
from unittest.mock import Mock, patch
import unittest
import logging
from service.utils import get_oauth_app
TEST_DB = 'test.db'


class AppTest(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        self.app = get_oauth_app('github', logging.getLogger())
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + TEST_DB
        # propagate the exceptions to the test client
        self.app.testing = True
        db.drop_all()
        db.create_all()

    @patch('flask_oauthlib.client.OAuthRemoteApp.get')
    def test_main_page(self, mock_get):
        mock_resp = self._mock_response()
        mock_get.return_value = mock_resp
        response = self.app.oauthapp.get('/')
        self.assertEqual(response.status_code, 200)

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

    @patch('flask_oauthlib.client.OAuthRemoteApp.get')
    def test_login(self, mock_get):
        mock_resp = self._mock_response()
        mock_get.return_value = mock_resp
        response = self.app.oauthapp.get('/login')
        self.assertEqual(response.status_code, 200)


    @patch('flask_oauthlib.client.OAuthRemoteApp.get')
    def test_logout(self, mock_get):
        mock_resp = self._mock_response()
        mock_get.return_value = mock_resp
        response = self.app.oauthapp.get('/logout')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
