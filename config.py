# config file 
import os

class Base:
    SECRET_KEY='Hard to guess 69'
    FILE_UPLOAD_FOLDER=os.path.join('application', 'static', 'updates')
    ALLOW_EXETENSION={'png', 'jpg', 'jpeg', 'mp4', 'avi'}

class Test(Base):
    '''This class only for testing.'''
    SECRET_KEY='Do not show that anyone.'
    SQLALCHEMY_DATABASE_URI="mysql+pymysql://root:2209@localhost/test"
    WTF_CSRF_ENABLED=False
    TESTING=True
    MEDIA_UPLOAD_FOLDER=os.path.join('application', 'static', 'test_media')
    PROFILE_UPLOAD_FOLDER=os.path.join('application', 'static', 'test_profile')

class Development(Base):
    # SQLALCHEMY_DATABASE_URI="mysql://username:password@localhost/db_name"
    SQLALCHEMY_DATABASE_URI="mysql+pymysql://root:2209@localhost/webchat"
    MEDIA_UPLOAD_FOLDER=os.path.join('application', 'static', 'media')
    PROFILE_UPLOAD_FOLDER=os.path.join('application', 'static', 'profile')


class Production(Base):
    SQLALCHEMY_DATABASE_URI="mysql+pymysql://root:2209@localhost/webchat"
    MEDIA_UPLOAD_FOLDER=os.path.join('application', 'static', 'media')
    PROFILE_UPLOAD_FOLDER=os.path.join('application', 'static', 'profile')

config={
    'Dev': Development,
    'Pro': Production,
    'testing': Test
}