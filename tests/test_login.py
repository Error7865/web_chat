import unittest
from flask import current_app, url_for
from application import create_app, db

class BasicLoginTest(unittest.TestCase):
    '''It test basic login mech'''
    def setUp(self) -> None:
        self.app=create_app('testing')
        self.app_context=self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.app.testing=True
        self.client=self.app.test_client()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register_login(self)->None:
        response=self.client.post('/main/', data={      
            'email': 'richi@example.com',
            'password': 'reba',
            'confirm': 'reba'
        },follow_redirects=True)        #register
        self.assertEqual(response.status_code, 200)
        self.assertIn('You can login now.', response.get_data(as_text=True))

        response=self.client.post('/main/', data={
            'email': 'richi@example.com',
            'password': 'reba'
        }, follow_redirects=True)       #login
        self.assertEqual(response.status_code, 200)
        self.assertIn('Login Successful', response.get_data(as_text=True))
    