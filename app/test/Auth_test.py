# tests/test_auth.py

import unittest
from app import create_app, db
from models import User

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['TESTING'] = True

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_signup_login(self):
        with self.app.app_context():
            # Signup
            response = self.client.post('/signup', json={
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'password'
            })
            self.assertEqual(response.status_code, 201)

            # Login
            response = self.client.post('/login', json={
                'username': 'testuser',
                'password': 'password'
            })
            self.assertEqual(response.status_code, 200)
            self.assertIn('access_token', response.get_json())

    def test_role_protection(self):
        with self.app.app_context():
            user = User(username='user', email='user@test.com', role='User')
            user.set_password('password')
            db.session.add(user)
            db.session.commit()

            # Try accessing admin route
            response = self.client.post('/login', json={
                'username': 'user',
                'password': 'password'
            })
            access_token = response.get_json()['access_token']

            response = self.client.get('/admin-only', headers={
                'Authorization': f'Bearer {access_token}'
            })
            self.assertEqual(response.status_code, 403)

if __name__ == '__main__':
    unittest.main()
