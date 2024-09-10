from application import create_app, db, migrate, socketio
from application.models import Role, User, Messages, Contact
import os

app=create_app('Dev')

@app.shell_context_processor
def register_shell():
    # print(f'Heere was current working dir {os.getcwd()}')
    return dict(app=app, db=db, Role=Role, User=User, Msg=Messages, Contact=Contact)

with app.app_context():
    db.create_all()

@app.cli.command()
def test():
    '''Run the unittest'''
    from coverage import Coverage
    cov=Coverage()
    cov.start()

    import unittest
    tests=unittest.TestLoader().discover('tests', 'test_*.py')
    unittest.TextTestRunner(verbosity=2).run(test=tests)

    cov.stop()
    cov.save()

    cov.html_report()
    
if __name__=="__main__":
    # app.run(debug=True)
    socketio.run(app)