from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
MONGODB_URI = "mongodb+srv://admin:admin123@optiresume.loocmvt.mongodb.net/?retryWrites=true&w=majority&appName=optiresume"
client = MongoClient(MONGODB_URI)
db = client["optiresume"]
users_collection = db["users"]
print("Connected to MongoDB:", os.getenv("MONGODB_URI"))
