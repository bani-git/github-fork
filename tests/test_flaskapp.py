import unittest
from app import flaskapp, db
import os
from unittest.mock import Mock, patch

TEST_DB = 'test.db'


class AppTest(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        flaskapp.config['TESTING'] = True
        flaskapp.config['WTF_CSRF_ENABLED'] = False
        flaskapp.config['DEBUG'] = False
        flaskapp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + TEST_DB
        self.app = flaskapp.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True
        db.drop_all()
        db.create_all()

        self.assertEqual(flaskapp.debug, False)

    def test_main_page(self):
        print(self.app)
        response = self.app.get('/')
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

    @patch('flaskapp.github_authorized')
    def test_login(self, mock_get):
        #json_data = {'id': '1234', 'name': 'test login'}
        #test_token = ('some test access token', '')
        #mock_resp = self._mock_response(json_data=json_data)
        mock_get.return_value = Mock()
        print(self.app)
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        print(self.app)
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
