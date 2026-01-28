from database import db
from seed_data import seed_videos

def clean_and_seed():
    print("Cleaning old videos...")
    db.get_videos_collection().delete_many({})
    print("Old videos deleted.")
    
    print("re-seeding with valid videos...")
    seed_videos()
    print("Done!")

if __name__ == "__main__":
    clean_and_seed()
