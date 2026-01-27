import jwt
from datetime import datetime, timedelta
from database import db
from config import Config
from bson.objectid import ObjectId

class Video:
    def __init__(self, title, description, youtube_id, thumbnail_url):
        self.title = title
        self.description = description
        self.youtube_id = youtube_id
        self.thumbnail_url = thumbnail_url
        self.is_active = True
        self.created_at = datetime.utcnow()
        
    def to_dict(self):
        return {
            'title': self.title,
            'description': self.description,
            'youtube_id': self.youtube_id,
            'thumbnail_url': self.thumbnail_url,
            'is_active': self.is_active,
            'created_at': self.created_at
        }
        
    @classmethod
    def create(cls, title, description, youtube_id, thumbnail_url):
        video = cls(title, description, youtube_id, thumbnail_url)
        videos_collection = db.get_videos_collection()
        result = videos_collection.insert_one(video.to_dict())
        return str(result.inserted_id)
        
    @classmethod
    def get_active_videos(cls, limit=2):
        videos_collection = db.get_videos_collection()
        videos = list(videos_collection.find({'is_active': True}).limit(limit))
        
        # Convert ObjectId to string and remove youtube_id for security
        for video in videos:
            video['_id'] = str(video['_id'])
            video.pop('youtube_id', None)  # Never expose YouTube ID to client
            
        return videos
        
    @classmethod
    def find_by_id(cls, video_id):
        videos_collection = db.get_videos_collection()
        video_data = videos_collection.find_one({'_id': ObjectId(video_id)})
        return video_data
        
    @classmethod
    def generate_playback_token(cls, video_id, user_id):
        """Generate a signed token for video playback"""
        payload = {
            'video_id': video_id,
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(hours=1),  # Token expires in 1 hour
            'purpose': 'video_playback'
        }
        return jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm='HS256')
        
    @classmethod
    def verify_playback_token(cls, token):
        """Verify and decode playback token"""
        try:
            payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
            if payload.get('purpose') != 'video_playback':
                return None
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
