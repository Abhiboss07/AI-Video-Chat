from functools import wraps
from flask import jsonify, request
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from models.user import User

def jwt_required_custom(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request()
            current_user_id = get_jwt_identity()
            
            # Verify user still exists
            user_data = User.find_by_id(current_user_id)
            if not user_data:
                return jsonify({'error': 'User not found'}), 401
                
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'error': 'Invalid token'}), 401
    return decorated_function
