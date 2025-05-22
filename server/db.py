from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
client = MongoClient(os.getenv("MONGODB_URI"))
db = client["optiresume"]
users_collection = db["users"]
print("Connected to MongoDB:", os.getenv("MONGODB_URI"))