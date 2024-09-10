import unittest
from flask import current_app
from application import create_app, db

class BasicTestCase(unittest.TestCase):
    '''Just a basic test'''
    def setUp(self) -> None:
        self.app=create_app('testing')
        self.app_context=self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.app.testing=True
        self.client=self.app.test_client(use_cookies=True)

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        response=self.client.get('/main/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Welcome to WebChat !', response.get_data(as_text=True))
        
    