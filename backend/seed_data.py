"""
Script to seed the database with sample video data
Run this script after setting up your MongoDB instance
"""

from models.video import Video

def seed_videos():
    """Seed the database with sample videos"""
    
    sample_videos = [
        {
            'title': 'React Native in 100 Seconds',
            'description': 'Quick introduction to React Native by Fireship.',
            'youtube_id': 'gvkqT_Uoahw',
            'thumbnail_url': 'https://img.youtube.com/vi/gvkqT_Uoahw/hqdefault.jpg'
        },
        {
            'title': 'Big Buck Bunny (Test)',
            'description': 'Reliable test video to verify playback.',
            'youtube_id': 'aqz-KE-bpKQ',
            'thumbnail_url': 'https://img.youtube.com/vi/aqz-KE-bpKQ/hqdefault.jpg'
        },
        {
            'title': 'Big Buck Bunny',
            'description': 'The classic open source test video.',
            'youtube_id': 'aqz-KE-bpKQ',
            'thumbnail_url': 'https://img.youtube.com/vi/aqz-KE-bpKQ/hqdefault.jpg'
        },
        {
            'title': 'MongoDB Explained',
            'description': 'What is MongoDB? (Official Video)',
            'youtube_id': 'pWbMrx5rV9w',
            'thumbnail_url': 'https://img.youtube.com/vi/pWbMrx5rV9w/hqdefault.jpg'
        },
        {
            'title': 'Mobile App Architecture',
            'description': 'Designing mobile apps for scale.',
            'youtube_id': 'inWWhr5tnEA',
            'thumbnail_url': 'https://img.youtube.com/vi/inWWhr5tnEA/hqdefault.jpg'
        }
    ]
    
    print("Seeding videos...")
    
    for video_data in sample_videos:
        try:
            video_id = Video.create(
                video_data['title'],
                video_data['description'],
                video_data['youtube_id'],
                video_data['thumbnail_url']
            )
            print(f"Created video: {video_data['title']} (ID: {video_id})")
        except Exception as e:
            print(f"Error creating video {video_data['title']}: {e}")
    
    print("Video seeding completed!")

if __name__ == "__main__":
    seed_videos()
