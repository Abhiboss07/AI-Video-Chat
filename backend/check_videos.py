from models.video import Video
from app import create_app
from bson.objectid import ObjectId

app = create_app()

with app.app_context():
    video_id = "697912c4ea20cb0038adf2ac"
    # Note: The log showed this ID. It might vary if the user re-seeded, but let's try to look it up or list all.
    
    videos = Video.get_active_videos(limit=100)
    print("Listing all videos in DB:")
    for v in videos:
        # We need to dig deeper to see the hidden youtube_id, so we'll use find_by_id logic or raw collection
        from database import db
        raw = db.get_videos_collection().find_one({'_id': ObjectId(v['_id'])})
        print(f"Title: {raw['title']}")
        print(f"YouTube ID: {raw['youtube_id']}")
        print(f"Watch URL: https://www.youtube.com/watch?v={raw['youtube_id']}")
        print("-" * 20)
