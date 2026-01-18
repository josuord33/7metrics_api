import pymongo
import sys
import certifi
from src.infrastructure.config.settings import settings

def test_connection():
    ca = certifi.where()
    uri = settings.MONGODB_URL
    client = pymongo.MongoClient(uri, serverSelectionTimeoutMS=5000, tlsCAFile=ca)

    try:
        print(f"Connecting to MongoDB ({settings.DATABASE_NAME}) using certifi...")
        client.admin.command('ping')
        print("✅ Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    finally:
        client.close()

if __name__ == "__main__":
    test_connection()
