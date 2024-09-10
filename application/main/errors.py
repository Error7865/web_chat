from flask import jsonify

def forbidden(msg):
    response=jsonify({'error': 'forbidden', "message": msg})
    response.status_code=403
    return response

def unauthorize(msg):
    response=jsonify({
        'error': 'unauthorize user',
        'msg': msg
    })
    response.status_code=401
    return response

def no_content(msg):
    response=jsonify({
        'error': 'No content',
        'msg': msg
    })
    response.status_code=204
    return response