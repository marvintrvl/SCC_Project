#tokens.py
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models import User

def init_jwt(app):
    jwt = JWTManager(app)

def authenticate(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user

def identity(payload):
    user_id = payload['identity']
    return User.query.get(user_id)

def create_jwt_token(user):
    access_token = create_access_token(identity=user.id)
    return access_token
