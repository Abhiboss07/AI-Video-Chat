import bcrypt
from datetime import datetime
from database import db
from bson.objectid import ObjectId

class User:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password_hash = self._hash_password(password)
        self.created_at = datetime.utcnow()
        
    def _hash_password(self, password):
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt)
        
    @staticmethod
    def verify_password(password, hashed):
        return bcrypt.checkpw(password.encode('utf-8'), hashed)
        
    def to_dict(self):
        return {
            'name': self.name,
            'email': self.email,
            'password_hash': self.password_hash,
            'created_at': self.created_at
        }
        
    @classmethod
    def create(cls, name, email, password):
        user = cls(name, email, password)
        users_collection = db.get_users_collection()
        result = users_collection.insert_one(user.to_dict())
        return str(result.inserted_id)
        
    @classmethod
    def find_by_email(cls, email):
        users_collection = db.get_users_collection()
        user_data = users_collection.find_one({'email': email})
        return user_data
        
    @classmethod
    def find_by_id(cls, user_id):
        users_collection = db.get_users_collection()
        user_data = users_collection.find_one({'_id': ObjectId(user_id)})
        if user_data:
            user_data['_id'] = str(user_data['_id'])
            # Remove password hash from response
            user_data.pop('password_hash', None)
        return user_data
