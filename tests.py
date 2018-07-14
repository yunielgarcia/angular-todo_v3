import unittest
from playhouse.test_utils import test_database
from peewee import *
import os
import tempfile

from app import app
from models import User, Todo

TEST_DB = SqliteDatabase(':memory:')


class TodoTestCase(unittest.TestCase):

    def setUp(self):
        self.db, app.config['DATABASE'] = tempfile.mkstemp()
        app.testing = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.tester = app.test_client()

    def login(self, email, password):
        return self.tester.post('/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    # testing routes
    def test_login_page_loads(self):
        resp = self.tester.get('/login', content_type='html/text')
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Login', resp.data)

    def test_register_page_loads(self):
        resp = self.tester.get('/register', content_type='html/text')
        self.assertEqual(resp.status_code, 200)

    def test_todos_page_redirects(self):
        resp = self.tester.get('/', content_type='html/text')
        self.assertEqual(resp.status_code, 302)

    # testing user registration
    def test_user_register(self):
        resp = self.tester.post('/register', data=dict(
            username='admin22',
            email='admin22@email.com',
            password='admin22',
            password2='admin22'), follow_redirects=True)
        # import pdb;pdb.set_trace()
        self.assertIn(b'Login', resp.data)


if __name__ == '__main__':
    with test_database(TEST_DB, [User, Todo]):
        unittest.main()
