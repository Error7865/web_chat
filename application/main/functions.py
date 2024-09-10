from ..models import User, db

def deactivate_user(user:User)->None:
    '''This will set user offline by set online False and connection_id
    None'''

    user.online=False
    user.connection_id=None
    db.session.commit()
