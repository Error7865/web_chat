from flask import url_for
from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey, select, and_, or_, text
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.event import listen, listens_for
from datetime  import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_socketio import emit
import hashlib
import random
from . import db
from . import login_manager

class Permission:
    USER=1
    ADMIN=2

class Role(db.Model):
    __tablename__='roles'
    id=mapped_column('Id', Integer, primary_key=True)
    name=mapped_column('Name', String(20), nullable=False, unique=True)
    default=mapped_column('Default', Boolean, nullable=False)
    permission=mapped_column('Permission', Integer, nullable=False)
    user=relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles={
            'User': [Permission.USER],
            'Administrator': [Permission.USER, Permission.ADMIN]
        }
        for r in roles:
            default=False
            if r=="User":       #if role was user then setting defaul True
                default=True
            role=Role.query.filter_by(name=r).first()
            if role is None:
                role=Role(name=r, permission=sum(roles[r]), default=default)
                db.session.add(role)
                db.session.commit()

    
    def __repr__(self) -> str:
        return f'<id: {self.id}> <name: {self.name}> <permission: {self.permission}>'


class User(db.Model, UserMixin):
    __tablename__='users'
    id=mapped_column('Id', Integer, primary_key=True)
    username=mapped_column('Username', String(30), nullable=False)
    email=mapped_column('Email', String(20), unique=True)
    password_hash=mapped_column('Password', String(500), nullable=False)
    user_key=mapped_column('User_key', String(150), unique=True)
    timestamp=mapped_column('Timestamp', DateTime, default=datetime.now())
    last_seen=mapped_column('Last_seen', DateTime, default=datetime.now())
    online=mapped_column('Online', Boolean, default=False)
    role_id=mapped_column('Role_id', Integer, ForeignKey('roles.Id'))
    connection_id=mapped_column('Sid_id', String(200), unique=True)
    today_update=mapped_column('Today_update', Boolean(), default=False)
    profile=mapped_column('Profile_pic', String(200), nullable=True)

    # Operation for Messages table 
    sender=relationship('Messages', backref='sender_user', lazy='dynamic', foreign_keys='Messages.sender')
    receiver=relationship('Messages', backref="receiver_user", lazy='dynamic', foreign_keys='Messages.receiver')

    #Contact table operation
    owner=relationship('Contact', backref='owner_user', foreign_keys='Contact.owner_id', lazy='dynamic')
    friend=relationship('Contact', backref='friend_user', foreign_keys='Contact.friend_id', lazy='dynamic')
    
    #Update table relationship
    update=relationship('Update', backref='owner', lazy='dynamic')

    #Viewer table relationship (one to one)
    viewes=relationship('Viewer', backref='viewer', lazy='dynamic')
    
    def __init__(self, *args, **kwargs) -> None:
        super(User, self).__init__(*args, **kwargs)
        if self.role is None:
            self.role=Role.query.filter_by(default=True).first()
        if self.username is None:
            self.username=self.email.split('@')[0]
        self.user_key=self.generate_user_key()

    def generate_user_key(self):
        bl=hashlib.blake2s()
        key=f'{str(random.randint(0,69))}web{self.email}chat{str(random.randint(0,69))}'
        bl.update(key.encode('utf-8'))
        return  bl.hexdigest()

    def verify_user_key(self, val):
        '''check that provided user key match or not '''
        if self.user_key==val:
            return True
        return False

    @property
    def password(self):
        raise AttributeError('Password not accessible.')

    @password.setter
    def password(self, val):
        self.password_hash=generate_password_hash(val)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def profile_image(self, size=100, default='wavatar'):
        '''This will generate image based on gravatar'''
        url='https://gravatar.com/avatar/'
        hash=hashlib.sha256(self.email.encode('utf-8'))
        if self.profile == None:
            return url+hash.hexdigest()+f'?s={size}&d={default}'
        else:
            return url_for('static', filename='profile/'+self.profile, _external=True)

    def today_updates(self)->bool:
        '''This method handle today up user updates like have any
        media exists that is not expired.'''
        update_list=list(filter(lambda u: u.active_media(), self.update.all()))  #list of all user update instance thoes are not expired
        return update_list
    
    def connectors(self)->list:
        '''return list of users who are connect with self'''
        connectors=list()
        for contact in Contact.query.filter_by(owner_id=self.id).all():
            connectors.append(contact.friend_user)
        return connectors

    @staticmethod
    def have_media(name:str)->bool:
        '''This static methode return boolean value base on
        media with name exists or not'''
        ls=User.query.filter( User.profile != None).all()
        for item in ls:
            if item.profile==name:
                return True
        return False
    
    @staticmethod
    def generate_profile_name(name:str)->str:
        '''This will generate unique name for each time'''
        extension=name[::-1].split('.')[0][::-1]
        start, end=97, 122
        ls=list(map(lambda x: random.randint(start, end), range(0,5)))
        index=0
        possible_combination=((end-start)+1)**len(ls)
        file=''
        loop_counter=0
        while True:
            if(index==end):
                index=start
            ls[index]=random.randint(start, end)
            for item in ls:
                file+=chr(item)
            if not User.have_media(file+'.'+extension):     #extension is a import thing you know
                return file+'.'+extension
            if loop_counter==possible_combination:
                raise NameError('We reach the end of 5 digit name.')
            index+=1
            file=''
            loop_counter+=1
            
    def __repr__(self) -> str:
        return f'<id: {self.id}><email: {self.email}><password: {self.password_hash}>'
    
class Messages(db.Model):
    '''Here have a column name seen which indicate that receiver
    seen that msg or not'''

    __tablename__='message'
    id=mapped_column('Id', Integer, primary_key=True)
    sender=mapped_column('Sender', Integer, ForeignKey('users.Id'))
    msg=mapped_column('Message', String(900), nullable=False)
    timestamp=mapped_column('Time', DateTime, default=datetime.now())
    receiver=mapped_column('Reciver', Integer, ForeignKey('users.Id'))
    seen=mapped_column('Seen', Boolean, default=False)
    is_media=mapped_column('Media', Boolean(), default=False, nullable=False)
    media_name=mapped_column('Media_Name', String(200), nullable=True)

    @staticmethod
    def set_msges_seen(sender_id:int, receiver_id:int)->None:
        '''This will set all unseen messages seen in message table 
        only send by sender to receiver'''

        unseen_msg_list=Messages.query.filter(and_(Messages.sender==sender_id, Messages.receiver==receiver_id, \
                                                   Messages.seen==False)).all()
        for msg in unseen_msg_list:
            # print(f'{msg} \n here {msg.seen}')
            msg.seen=True
        db.session.commit()

    @staticmethod
    def have_media(name:str)->bool:
        '''This static methode return boolean value base on
        media with name exists or not'''
        ls=Messages.query.filter_by(is_media=True).all()
        for item in ls:
            if item.media_name==name:
                return True
        return False
            

    @staticmethod
    def generate_media_name(name:str)->str:
        '''This will generate unique name for each time'''
        extension=name[::-1].split('.')[0][::-1]
        start, end=97, 122
        ls=list(map(lambda x: random.randint(start, end), range(0,5)))
        index=0
        possible_combination=((end-start)+1)**len(ls)
        file=''
        loop_counter=0
        while True:
            if(index==end):
                index=start
            ls[index]=random.randint(start, end)
            for item in ls:
                file+=chr(item)
            if not Messages.have_media(file+'.'+extension):     #extension is a import thing you know
                return file+'.'+extension
            if loop_counter==possible_combination:
                raise NameError('We reach the end of 5 digit name.')
            index+=1
            file=''
            loop_counter+=1
    
    @staticmethod
    def convert_for_client(ls:list, user_id: int)->list:
        '''This methode contvert Message instances to a list of 
        dict which contain msg, owner, url of media'''
        clients_data=list()
        # print('Here ls ', ls[0])
        for message in ls:
            owner=False
            if message.sender==user_id:
                owner=True
            if message.is_media==True:
                url=url_for('static', filename='media/'+message.media_name, _external=True)
            else:
                url=None
            clients_data.append(dict(msg=message.msg, owner=owner, url=url))
        return clients_data

    def __repr__(self) -> str:
        return f'<id: {self.id}><sender: {self.sender}><msg: {self.msg}><reciver: {self.receiver}>'

class Contact(db.Model):
    '''This will records all user and their contacts
    last seen column hold last time when user seen his/her msg'''
    __tablename__="contact"
    id=mapped_column('Id', Integer, primary_key=True)
    owner_id=mapped_column('User', Integer, ForeignKey('users.Id'))
    timestamp=mapped_column('Timestamp', DateTime, default=datetime.now())
    is_msg=mapped_column('Is_contact', Boolean, default=True)         #This column indicate that owner have sent messages any time(True) or not
    friend_id=mapped_column('Friend', Integer, ForeignKey('users.Id'))
    last_seen=mapped_column('Last_Seen', DateTime, nullable=True)
    
    @staticmethod
    def check_instance_exits(owner_id:int, friend_id:int)->bool:
        '''This function just check that instance exits or not
        and return boolean value based on it'''

        contact=db.session.execute(select(Contact).where(and_(Contact.owner_id==owner_id, Contact.friend_id==friend_id))).first()
        if contact is None:
            return False
        return True
    
    @staticmethod
    def contactinstance_to_dict(contact_instance)->list:
        '''This will take contact instance and retrive data and
        return a list where only have list of users who was connect with
        current user'''

        ls=list()
        for i in contact_instance:
            instance=i[0]
            unseen_msges=Messages.query.filter(and_(Messages.sender==instance.friend_id, \
                                Messages.receiver==instance.owner_id, Messages.seen==False)).count()
            ls.append(dict(email=instance.friend_user.email, profile=instance.friend_user.profile_image(), unseen=unseen_msges))
        return ls
    
    @staticmethod
    def connect_users(user:User)->list:
        '''Return list of users who are connect with user'''
        users=list()
        contacts=Contact.query.filter_by(owner_id=user.id, is_msg=True).all()
        for i in contacts:
            users.append(i)
        return users

    def __repr__(self) -> str:
        return f'<id: {self.id}><user_id: {self.owner_id}><friend: {self.friend_id}>'

class Update(db.Model):
    __tablename__='daily'
    id=mapped_column('Id', Integer, primary_key=True)
    media_name=mapped_column('Name', String(400), nullable=False)
    timestamp=mapped_column('TimeStamp', DateTime(), default=datetime.now())
    is_expire=mapped_column('Expire', Boolean(), nullable=False, default=False)
    owner_id=mapped_column('Owner', Integer, ForeignKey('users.Id'))

    #connection with viewer table
    viewers=relationship('Viewer', backref='media', lazy='dynamic')

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
    
    def active_media(self)->bool:
        '''return boolean value base on next 24 hourafter upload
        if media active return True else False'''
        def expire():
            '''Just for not repear same line'''
            self.is_expire=True
            db.session.commit()
            return False
        
        if not self.is_expire:
            try:
                next_day=datetime(self.timestamp.year, self.timestamp.month, self.timestamp.day+1, \
                                  self.timestamp.hour, self.timestamp.minute, self.timestamp.second)
            except ValueError:  #in case of day out of range like 29, 31, 32
                try:
                    next_day=datetime(self.timestamp.year, self.timestamp.month+1, 1, \
                                    self.timestamp.hour, self.timestamp.minute, self.timestamp.second)
                except ValueError:  #in case of month out of range like 13
                    next_day=datetime(self.timestamp.year+1, 1, 1, \
                self.timestamp.hour, self.timestamp.minute, self.timestamp.second)
            today=datetime.today()
            if today.day > next_day.day:
                return expire()
            elif today.day == next_day.day:
                return True
            else:
                if today.year > next_day.year or today.month > next_day.month:
                    return expire()    
            return True
        return False

    @staticmethod
    def user_updates(user:User)->list:
        '''Return all updated resources url'''
        updates=list()
        ls=Update.query.filter(Update.owner_id==user.id, Update.is_expire==False).all()
        for item in ls:
            if item.active_media():
                updates.append(item)
        
        return updates
            
    @staticmethod
    def is_exits_name(name:str)->bool:
        '''This function check any media exits with that name
        or not and return boolean value based on it.'''
        ls=Update.query.filter_by(media_name=name).first()
        if ls==[] or ls is None:
            return False
        return True

    @staticmethod
    def generate_file_name(name:str)->str:
        '''return a valie name for media file'''
        extension=name[::-1].split('.')[0][::-1]
        generate_letter=lambda: chr(random.randint(97,123))
        i=97
        while True:
            filename=generate_letter()
            if i==123:
                filename+=generate_letter()
            fullname=filename+'.'+extension
            print('here new filename ', fullname)
            if not Update.is_exits_name(fullname ):
                i=97
                return fullname
            i+=1
    
    def __repr__(self) -> str:
        return f'<id:{self.id}><name: {self.media_name}><owner: {self.owner_id}><expire: {self.is_expire}>'


class Viewer(db.Model):
    __tablename__='viewer'
    id=mapped_column('Id', Integer, primary_key=True)
    media_id=mapped_column('Media', ForeignKey('daily.Id'), nullable=False)
    timestamp=mapped_column('TimeStamp', DateTime(), default=datetime.now())
    viewer_id=mapped_column('Viewer', Integer, ForeignKey('users.Id'))

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def __repr__(self) -> str:
        return f'<id: {self.id}> <media_id: {self.media_id}> <time: {self.timestamp}> <viewer: {self.viewer}>'

@login_manager.user_loader      #for flask-login
def load_user(user_id):
    return User.query.get(user_id)

def message_table_update(mapper, connection, target):
    '''Here task is to check where receiver is online or not
    if online then emit msg'''
    # print(f'Here mapper {mapper} \n connection {connection} \n target {target}')
    url=None
    if target.receiver_user.online and target.receiver_user.connection_id is not None: #user online
        # print('url of audio ', url_for('static', filename='sounds/new.mp3'))
        if target.is_media:
            url=url_for('static', filename='media/'+target.media_name, _external=True)
        emit('receive msg', {'sender': target.sender_user.email, 'msg': target.msg, 'audio': url_for('static', filename='sounds/new.mp3'), 'url': url}, to=target.receiver_user.connection_id)
    

listen(Messages, 'after_insert', message_table_update)

@listens_for(Update, 'after_insert')
def update_table_updated(mapper, connection, target: Update):
    owner=target.owner
    online_users=list(filter(lambda user: user.online, owner.connectors()))
    # print('url ', url_for('static', filename=f'updates/{target.media_name}', _external=True))
    for user in online_users:
        emit('new update', {
            'user': owner.email,
            'img': user.profile_image(),
            'update': url_for('static', filename=f'updates/{target.media_name}', _external=True)
        }, to=user.connection_id)
    emit('new update', {
        'user': 'My Update',
        'img': owner.profile_image(),
        'update': url_for('static', filename=f'updates/{target.media_name}', _external=True)
    }, to=owner.connection_id)

