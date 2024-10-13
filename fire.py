import pyrebase
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Firebase configuration
config = {
    "apiKey": os.getenv("FIREBASE_API_KEY"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
    "databaseURL": os.getenv("FIREBASE_DATABASE_URL"),
    "projectId": os.getenv("FIREBASE_PROJECT_ID"),
    "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
    "appId": os.getenv("FIREBASE_APP_ID"),
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

def create_user(user_id, user_data):
    """Create a new user in Firebase."""
    db.child("users").child(user_id).set(user_data)

def get_user(user_id):
    """Retrieve user data from Firebase."""
    return db.child("users").child(user_id).get().val()

def update_user(user_id, user_data):
    """Update existing user data in Firebase."""
    db.child("users").child(user_id).update(user_data)

def save_user_coins(user_id, coins):
    """Save user coins to Firebase."""
    db.child("users").child(user_id).update({"coins": coins})
