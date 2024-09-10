import unittest
from flask import current_app
from application import create_app, db, socketio

class BasicSocketio(unittest.TestCase):
    def setUp(self) -> None:
        self.app=create_app('testing')
        self.app_context=self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client=self.app.test_client()
        self.socket_client=socketio.test_client(self.app, flask_test_client=self.client)
    
    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_socket_connect(self)->None:
        self.assertTrue(self.socket_client.is_connected())