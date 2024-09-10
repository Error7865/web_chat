from flask import request, jsonify
from . import api
from .errors import unauthorize, no_content
from ..models import User

@api.route('/search-user', methods=['GET','POST'])
def search_user():
    data=request.get_json()
    print(data)
    user=User.query.filter_by(user_key=data['user_key']).first()
    if user is None:        #user_key does not exits
        return unauthorize('Unvalid userkey.')
    #Now we find user so just return user with given email
    looking_for=User.query.filter_by(email=data['email']).first()
    if looking_for is None or looking_for.email==user.email:     #There haven't any user with provided email
        return no_content('Ther haven\'t any user with this email')
    # print('Here data ', looking_for.email)
    return jsonify({
        'email': looking_for.email,
        'picture': looking_for.profile_image()
    })