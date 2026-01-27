from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    jwt = JWTManager(app)
    CORS(app)
    
    # Register blueprints
    from routes.auth import auth_bp
    from routes.video import video_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(video_bp)
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'message': 'API is running'}
    
    return app
