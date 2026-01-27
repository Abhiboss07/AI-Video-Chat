import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    JWT_SECRET_KEY = os.getenv('JWT_SECRET', 'fallback_secret_key_change_in_production')
    JWT_ACCESS_TOKEN_EXPIRES = 86400  # 24 hours in seconds
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/videoapp')
    DB_NAME = 'videoapp'
