from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models.user import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or not all(k in data for k in ('name', 'email', 'password')):
            return jsonify({'error': 'Missing required fields'}), 400
            
        name = data['name'].strip()
        email = data['email'].strip().lower()
        password = data['password']
        
        # Basic validation
        if len(name) < 2:
            return jsonify({'error': 'Name must be at least 2 characters'}), 400
            
        if len(password) < 6:
            return jsonify({'error': 'Password must be at least 6 characters'}), 400
            
        # Check if user already exists
        existing_user = User.find_by_email(email)
        if existing_user:
            return jsonify({'error': 'Email already registered'}), 409
            
        # Create new user
        user_id = User.create(name, email, password)
        
        # Create access token
        access_token = create_access_token(identity=user_id)
        
        return jsonify({
            'message': 'User created successfully',
            'user_id': user_id,
            'access_token': access_token
        }), 201
        
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data or not all(k in data for k in ('email', 'password')):
            return jsonify({'error': 'Missing email or password'}), 400
            
        email = data['email'].strip().lower()
        password = data['password']
        
        # Find user
        user_data = User.find_by_email(email)
        if not user_data:
            return jsonify({'error': 'Invalid credentials'}), 401
            
        # Verify password
        if not User.verify_password(password, user_data['password_hash']):
            return jsonify({'error': 'Invalid credentials'}), 401
            
        # Create access token
        access_token = create_access_token(identity=str(user_data['_id']))
        
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user': {
                'id': str(user_data['_id']),
                'name': user_data['name'],
                'email': user_data['email']
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    try:
        current_user_id = get_jwt_identity()
        user_data = User.find_by_id(current_user_id)
        
        if not user_data:
            return jsonify({'error': 'User not found'}), 404
            
        return jsonify({
            'user': user_data
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    # In a production app, you might want to implement token blacklisting
    # For now, we'll just return success - client should discard the token
    return jsonify({'message': 'Logout successful'}), 200
