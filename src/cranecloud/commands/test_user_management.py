import unittest
from unittest.mock import patch, MagicMock
from click.testing import CliRunner
from user_management import login

class TestUserManagement(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    @patch('requests.post')
    @patch('click.echo')
    @patch('keyring.set_password')
    def test_login_success(self, mock_set_password, mock_echo, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'data': {
                'access_token': 'token123',
                'id': 'user123'
            }
        }
        mock_post.return_value = mock_response

        result = self.runner.invoke(login, ['-e', 'test@example.com', '-p', 'password123'])

        mock_post.assert_called_once_with('http://api.example.com/users/login', json={
            'email': 'test@example.com',
            'password': 'password123'
        })
        mock_set_password.assert_any_call('cranecloud', 'token', 'token123')
        mock_set_password.assert_any_call('cranecloud', 'user_id', 'user123')
        mock_echo.assert_called_with('Login successful!')
        self.assertEqual(result.exit_code, 0)

    @patch('requests.post')
    @patch('click.echo')
    def test_login_failure(self, mock_echo, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_post.return_value = mock_response

        result = self.runner.invoke(login, ['-e', 'test@example.com', '-p', 'password123'])

        mock_post.assert_called_once_with('http://api.example.com/users/login', json={
            'email': 'test@example.com',
            'password': 'password123'
        })
        mock_echo.assert_called_with('Login failed. Please check your credentials.')
        self.assertEqual(result.exit_code, 0)

if __name__ == '__main__':
    unittest.main()