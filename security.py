
from user import User
from werkzeug.security import safe_str_cmp # flask comes with a safe string compare

users = [
    User(1, 'ian', 'pw')
]

# uses set comprehension, look up if syntax is confusing 
username_mapping = {u.username : u for u in users} 
userid_mapping = {u.id : u for u in users}

def authenticate (username, password):
    user = username_mapping.get(username, None)
    if user and safe_str_cmp(user.password, password): 
        return user

# identity is specific to the flask-jwt library
def identity(payload):
    userid = payload['identity']
    return userid_mapping.get(userid, None)
