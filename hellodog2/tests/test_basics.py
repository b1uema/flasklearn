import unittest
from flask import current_app
from hellodog2 import create_app,db

class BasicsTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context=self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exit(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['testing'])