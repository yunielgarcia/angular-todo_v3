import unittest
import os
import tempfile

from app import app


class TodoTestCase(unittest.TestCase):

    def setUp(self):
        self.db, app.config['DATABASE'] = tempfile.mkstemp()
        app.testing = True
        self.app = app.test_client()

    def tearDown(self):
        os.close(self.db)
        os.unlink(app.config['DATABASE'])

    def test_empty_db(self):
        rv = self.app.get('/')
        assert b'No entries here so far' in rv.data
