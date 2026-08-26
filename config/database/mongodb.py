from pymongo import MongoClient
from django.conf import settings

client = MongoClient(
    settings.MONGODB_URI,
    serverSelectionTimeoutMS=5000,
)

def get_database():
    return client[settings.MONGODB_NAME]

db = get_database()