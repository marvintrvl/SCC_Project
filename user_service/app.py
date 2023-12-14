# user-service/app.py

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies
from datetime import timedelta
from models import User
from database import db
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5003"}}, supports_credentials=True)

db_name = 'users.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'uewqriughbrepighrrupqeghrtoubq34t'
app.config['JWT_SECRET_KEY'] = 'uewqriughbrepighrrupqeghrtoubq34t'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)

db.init_app(app)

def create_db():
    with app.app_context():
        db.create_all()
 
if __name__ == "__main__":
    from models import User
    create_db()

# Initialize extensions
jwt = JWTManager(app)

# User loader function 
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.get(identity)

# Routes
@app.route('/')
def index():
    return jsonify(message='Welcome to the User Service!')

@app.route('/register', methods=['POST'])
@cross_origin()
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    street = data.get('street')
    city = data.get('city')
    postal_code = data.get('postal_code')
    country = data.get('country')

    if username and password:
        new_user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            street=street,
            city=city,
            postal_code=postal_code,
            country=country
        )
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify(message='User registered successfully'), 201
    else:
        return jsonify(message='Username and password are required'), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify(message='Invalid credentials'), 401

@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    response = jsonify(message='Logged out successfully')
    unset_jwt_cookies(response)
    return response, 200

@app.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    user = User.query.get(current_user)
    if user:
        return jsonify({
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'street': user.street,
            'city': user.city,
            'postal_code': user.postal_code,
            'country': user.country,
        }), 200
    else:
        return jsonify(message='User not found'), 404

# Flask route for changing name
@app.route('/change-name', methods=['POST'])
@jwt_required()
def change_name():
    current_user = get_jwt_identity()
    user = User.query.get(current_user)
    if user:
        data = request.get_json()
        # Update user's name details
        user.first_name = data.get('newFirstName')
        user.last_name = data.get('newLastName')
        db.session.commit()
        return jsonify(message='Name changed successfully'), 200
    else:
        return jsonify(message='User not found'), 404

@app.route('/change-email', methods=['POST'])
@jwt_required()
def change_email():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if user:
        data = request.get_json()
        
        # Update user's username (which is used as an email)
        user.username = data.get('new_email')
        db.session.commit()
        
        return jsonify(message='Email changed successfully'), 200
    else:
        return jsonify(message='User not found'), 404

# Flask route for changing password
@app.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    current_user = get_jwt_identity()
    user = User.query.get(current_user)
    if user:
        data = request.get_json()
        current_password = data.get('currentPassword')
        new_password = data.get('newPassword')
        repeat_password = data.get('repeatPassword')

        # Check if current password is correct
        if not user.check_password(current_password):
            return jsonify(message='Current password is incorrect'), 400

        # Check if new password and repeat password match
        if new_password != repeat_password:
            return jsonify(message='New password and repeat password do not match'), 400

        # Update user's password
        user.set_password(new_password)
        db.session.commit()
        return jsonify(message='Password changed successfully'), 200
    else:
        return jsonify(message='User not found'), 404

# Flask route for changing address
@app.route('/change-address', methods=['POST'])
@jwt_required()
def change_address():
    current_user = get_jwt_identity()
    user = User.query.get(current_user)
    if user:
        data = request.get_json()
        # Update user's address details
        user.street = data.get('newStreet')
        user.city = data.get('newCity')
        user.postal_code = data.get('newPostalCode')
        user.country = data.get('newCountry')
        db.session.commit()
        return jsonify(message='Address changed successfully'), 200
    else:
        return jsonify(message='User not found'), 404

    
@app.after_request
def after_request(response):
    if request.method == 'DELETE':
        response.headers['Access-Control-Allow-Origin'] = 'http://127.0.0.1:5003'
    response.headers['Access-Control-Allow-Origin'] = 'http://127.0.0.1:5003'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, HEAD, PUT, DELETE, OPTIONS'
    return response

if __name__ == '__main__':
    app.run(debug=True)
