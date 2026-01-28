from models.user import User
from app import create_app

app = create_app()

with app.app_context():
    email = "john@example.com"
    password = "password123"
    
    user = User.find_by_email(email)
    if not user:
        print("User not found!")
    else:
        print(f"User found: {user['email']}")
        # Verify password manually
        is_valid = User.verify_password(password, user['password_hash'])
        print(f"Password 'password123' valid? {is_valid}")
        
        if not is_valid:
            # Let's try to reset it
            print("Resetting password...")
            # We need to manually update the hash in DB since we don't have an update method exposed in this way smoothly
            # But we can create a new User object to get the hash
            temp_user = User("temp", "temp", password)
            new_hash = temp_user.password_hash
            
            from database import db
            db.get_users_collection().update_one(
                {'email': email},
                {'$set': {'password_hash': new_hash}}
            )
            print("Password reset to 'password123'")
