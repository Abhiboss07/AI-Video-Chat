from models.user import User
from app import create_app

app = create_app()

with app.app_context():
    # Check if user exists
    email = "john@example.com"
    existing = User.find_by_email(email)
    
    if existing:
        print(f"User {email} already exists")
    else:
        try:
            user_id = User.create("John Doe", email, "password123")
            print(f"Successfully created user: {email} / password123")
            print(f"User ID: {user_id}")
        except Exception as e:
            print(f"Error creating user: {e}")
