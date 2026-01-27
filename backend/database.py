from pymongo import MongoClient
from config import Config

class Database:
    def __init__(self):
        self.client = MongoClient(Config.MONGO_URI)
        self.db = self.client[Config.DB_NAME]
        
    def get_users_collection(self):
        return self.db.users
        
    def get_videos_collection(self):
        return self.db.videos
        
    def close_connection(self):
        self.client.close()

# Global database instance
db = Database()
