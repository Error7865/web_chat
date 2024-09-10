from flask import render_template, redirect, url_for, flash, request, g, current_app
from flask_login import login_required, login_user, current_user, logout_user
from sqlalchemy import select, and_
from werkzeug.utils import secure_filename
from .. import socketio
from . import main
from .forms import Register, Login
from ..models import db, User, Messages, Contact
import os

# g.list_online_users_id=list()        #This one will hold all online users id
                        #after login user id will append and 
# after disconnect event of socketio will remove from this list 

@main.route('/', methods=['GET', 'POST'])
def index():
    register_form=Register()
    login_form=Login()
    if register_form.validate_on_submit():  #register operation 
        email=register_form.email.data
        password=register_form.password.data
        user=User.query.filter_by(email=email).first()
        if user is not None:
            flash('This email already exits. Try to Log in.')
            return redirect(url_for('main.index'))
        #email is not exits
        user=User(email=email, password=password)
        db.session.add(user)
        db.session.commit()
        flash('Register Successful')
        flash('You can login now.')
        return redirect(url_for('main.index'))
    if login_form.validate_on_submit():     #login operation
        email=login_form.email.data
        password=login_form.password.data
        user=User.query.filter_by(email=email).first()
        if user is None or not user.verify_password(password):    #No result found or wrong password
            flash('Please check your email and password.')
            return redirect(url_for('.index'))
        login_user(user=user, remember=False)
        # g.list_online_user_users_id.append(user.id)
        flash('Login Successful')
        return redirect(url_for('main.home'))
    return render_template('index.html', register_form=register_form, login_form=login_form)

@main.route('/home')
@login_required
def home():
    # print('Here form g ', g.name)
    # print('Here g was ',g.forms)
    contact_ls=db.session.execute(select(Contact).where(and_(Contact.owner_id==current_user.id, \
                    Contact.is_msg==1))).all()
    msg_ls=Contact.contactinstance_to_dict(contact_ls)

    return render_template('home.html', msg_ls=msg_ls)

@main.route('/register', methods=['POST'])
def register():
    form=Register()
    if form.validate_on_submit():
        email=form.email.data
        password=form.password.data
        user=User.query.filter_by(email=email).first()
        if user is not None:
            flash('This email already exits. Try to Log in.')
            return redirect(url_for('main.index'))
        #email is not exits
        user=User(email=email, password=password)
        db.session.add(user)
        db.session.commit()
        flash('Register Successful')
        flash('You can login now.')
        return redirect(url_for('main.index'))
    return 'Sorry you can\'t login.'
    

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/call', methods=['GET', 'POST'])
def call():
    print(request.get_json())
    return {'msg': "Hello from backend."}

@main.route('/daily', methods=['GET', 'POST'])
def daily_update():
    if request.method=='POST':
        print('Here I am inside daily update.')
        # if 'file' not in request.files:
        #     print(f'Inside function {}')
        #     flash('No file found')
        #     return redirect(url_for('.home'))
        file=request.files['file']
        print('Here filename ', file.name)
        if file.filename=='':
            flash('No selected file.')
            return redirect(url_for('.home'))
        filename=secure_filename(file.filename)
        file.save(os.path.join(current_app.config['FILE_UPLOAD_FOLDER'], filename))
        return redirect(url_for('.home'))