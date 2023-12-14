# user-service/models.py
from database import db
from passlib.hash import sha256_crypt  # Import the sha256_crypt hashing algorithm

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    street = db.Column(db.String(255))
    city = db.Column(db.String(255))
    postal_code = db.Column(db.String(20))
    country = db.Column(db.String(255))

    def set_password(self, password):
        # Use passlib to hash the password using sha256_crypt
        self.password_hash = sha256_crypt.hash(password)

    def check_password(self, password):
        # Use passlib to verify the hashed password
        return sha256_crypt.verify(password, self.password_hash)
