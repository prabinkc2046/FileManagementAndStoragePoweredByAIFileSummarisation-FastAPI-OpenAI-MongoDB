from pymongo import MongoClient
from model import FileModel
from uuid import uuid4
from datetime import datetime

# Get mongo path and database name
from environment.get_env_variable import MONGODB_PATH, DB_NAME


# MongoDB setup
client = MongoClient(MONGODB_PATH)
db = client[DB_NAME]
users_collection = db["users"]
blacklist_collection = db["token_blacklist"]
files_collection = db["files"]
storage_collection = db["storage"]
secret_collection= db["secret"]

