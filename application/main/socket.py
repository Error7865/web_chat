from flask import jsonify, request, g, current_app, url_for
from sqlalchemy import select, or_, and_
from flask_socketio import emit
from flask_login import current_user
from werkzeug.utils import secure_filename
from .. import socketio
from ..models import User, Messages, Contact, db, Update, Viewer
from ..tools import msginstance_to_ls, select_instace_to_ls
from .errors import no_content
import os

# online_users_id=Stack()  #This one was global variable which hold all online users id

@socketio.on('connect')
def connect():
    g.current_sid=request.sid
    pass

@socketio.on('call')
def call():
    return 'yes'

@socketio.on('active user')
def user_online(user_key):
    '''This will notified when user online and it set user online'''
    user=User.query.filter_by(user_key=user_key).first_or_404()
    user.connection_id=request.sid
    user.online=True
    db.session.commit()
    # online_users_id.push(current_user.id)
    print('Connection stabilsh ')
    

@socketio.on('user')
def user_msg_list(useremail):
    '''Actually here have two types of Messages instance
    one case was current_user is sender and user was receiver
    another case was user is sender and current_user was receiver'''

    receiver=db.session.execute(select(User).where(User.email==useremail)).first()[0]
    msg_id_ls=db.session.execute(select(Messages.id).where( \
        and_(Messages.sender_user==current_user, Messages.receiver_user== \
             receiver))).all()    #here query as current_user was sender 
    msg_id_ls1=db.session.execute(select(Messages.id).where( \
        and_(Messages.sender_user==receiver, Messages.receiver_user== \
             current_user))).all()        #Here current_user was receiver
    final_ls=msg_id_ls+msg_id_ls1
    final_ls.sort()
    list_of_id=select_instace_to_ls(final_ls)   #list of id of each Messages instace that match with this case
    Get=lambda id: Messages.query.get(id)       #Just a lambda function which return a list of message instance
    ls_of_msg_instance=list(map(Get, list_of_id))
    msg_ls=Messages.convert_for_client(ls_of_msg_instance, current_user.id)
    # also need to set all messages seen  send by useremail 
    Messages.set_msges_seen(receiver.id, current_user.id)
    # print("here I am \n",msg_ls)
    emit('decorate_msg', msg_ls, to=request.sid)

@socketio.on('receive msg')
def receive_msg(msg, to):
    '''This function receive msg from current_user to target'''
    to_user=db.session.execute(select(User).where(User.email==to)).first()[0]
    message=Messages(sender_user=current_user, msg=msg, receiver_user=to_user)
    db.session.add(message)
    db.session.commit()
    emit('decorate_msg', [dict(msg=msg, owner=True)], to=request.sid)

@socketio.on('search user')
def search_user(user_eamil):
    '''This function will add connection between new user and 
    current user'''
    # print('User email ',user_eamil)
    user=User.query.filter_by(email=user_eamil).first()
    found=True
    if user is None:
        found=False
        return emit('set user', {'found': found,
                                 'error': 'No result found.'},)
    if not Contact.check_instance_exits(current_user.id, user.id):  #instance not exits so create new instance
        contact=Contact(owner_id=current_user.id, friend_id=user.id)
        db.session.add(contact)
        db.session.commit()
    emit('set user', {
        'found': found,
        'email': user.email,
        'profile': user.profile_image()
    })


@socketio.on('message')
def handle_message(data):
    print('I got your data')
    return {'name': None}

@socketio.on('upload')
def upload_update(file, name):
    filename=secure_filename(name)
    if Update.is_exits_name(filename):
        print('File exists already.')
        filename=Update.generate_file_name(filename)
    update=Update(media_name=filename, owner=current_user)
    with open(os.path.join(current_app.config['FILE_UPLOAD_FOLDER'],filename), 'wb') as media:
        media.write(file)
    current_user.today_update=True  #if user update then it will True or False
    db.session.add(update)
    db.session.commit()
    emit('successfull', "Your Update complete.")


@socketio.on('update user')
def update_users():
    '''Return connected users who update'''
    friends=Contact.connect_users(current_user) #all connectors
    updated_user=list()
    for friend in friends:
        friend_updates=friend.friend_user.today_updates()
        if friend_updates != []:
            friend_dict={'user': friend.friend_user.email,
                         'img': friend.friend_user.profile_image(),
                         'updates': list(map(lambda x: url_for('static', filename='updates/'+x.media_name, _external=True), friend_updates))}
            updated_user.append(friend_dict)
        if current_user.today_updates() != []:
            updated_user.append({
                'user': 'My Update',
                'img': current_user.profile_image(),
                'updates': list(map(lambda x: url_for('static', filename='updates/'+x.media_name, _external=True), current_user.today_updates()))
            })
    return updated_user

@socketio.on('viewing')
def set_viewer(media_url, useremail):
        '''It just for future in case implement how many user view 
        update in that case'''
        pass

@socketio.on('new media')
def save_media(msg, to, filename, file):
    filename=Messages.generate_media_name(filename)
    to_user=db.session.execute(select(User).where(User.email==to)).first()[0]
    message=Messages(sender_user=current_user, msg=msg, receiver_user=to_user, 
                     is_media=True, media_name=filename)
    db.session.add(message)
    db.session.commit()
    with open(os.path.join(current_app.config['MEDIA_UPLOAD_FOLDER'], filename), 'wb') as media:
        media.write(file)
     # emit('decorate_msg', [dict(msg=msg, owner=True)], to=request.sid)
    return {'msg': message.msg, 'owner': True, 'url': url_for('static',
                    filename='media/'+message.media_name, _external=True)}

@socketio.on('change name')
def name_change(name):
    '''This function change username'''
    current_user.username=secure_filename(name)
    db.session.commit()
    return {
        'name': current_user.username,
        'msg':'Your name successfully updated.'
        }

@socketio.on('update profile')
def update_profile_pic(filename, file):
    print('Here file name ', filename)
    path=current_app.config['PROFILE_UPLOAD_FOLDER']
    filename=User.generate_profile_name(filename)
    current_user.profile=filename
    with open(os.path.join(path, filename), 'wb') as profile:
        profile.write(file)
    db.session.commit()
    return {'url': current_user.profile_image(),
        'msg':' Your profile was updated.'
    }
        
@socketio.on('user info')    
def user_info(mail):
    user=User.query.filter_by(email=mail).first()
    if user is None:
        return no_content('No user found.')
    return {
        'mail': user.email,
        'name': user.username,
    }


@socketio.on('disconnect')
def disconnect():
    '''In case of client side any emit will not occure after disconnect
    so I need to do this mean create a function and query user by '''
    current_user.online=False
    current_user.connection_id=None
    db.session.commit()
    # online_users_id.remove(current_user.id)
    print('Connection close. ')

