"""
Script to seed the database with sample video data
Run this script after setting up your MongoDB instance
"""

from models.video import Video

def seed_videos():
    """Seed the database with sample videos"""
    
    sample_videos = [
        {
            'title': 'Introduction to React Native',
            'description': 'Learn the basics of building mobile apps with React Native',
            'youtube_id': '0-S5a0Be2F4',
            'thumbnail_url': 'https://img.youtube.com/vi/0-S5a0Be2F4/hqdefault.jpg'
        },
        {
            'title': 'Flask API Development',
            'description': 'Building RESTful APIs with Flask and Python',
            'youtube_id': 'FSPRvFdiB_c',
            'thumbnail_url': 'https://img.youtube.com/vi/FSPRvFdiB_c/hqdefault.jpg'
        },
        {
            'title': 'MongoDB Database Design',
            'description': 'Best practices for designing MongoDB schemas',
            'youtube_id': 'pWbMrx5rV9w',
            'thumbnail_url': 'https://img.youtube.com/vi/pWbMrx5rV9w/hqdefault.jpg'
        },
        {
            'title': 'JWT Authentication Explained',
            'description': 'Understanding JSON Web Tokens and secure authentication',
            'youtube_id': '926YEknB8O0',
            'thumbnail_url': 'https://img.youtube.com/vi/926YEknB8O0/hqdefault.jpg'
        },
        {
            'title': 'Mobile App Security',
            'description': 'Security best practices for mobile applications',
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
