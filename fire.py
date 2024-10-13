import pyrebase
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

firebase_config = {
    "apiKey": os.getenv("API_KEY"),
    "authDomain": os.getenv("AUTH_DOMAIN"),
    "databaseURL": os.getenv("DATABASE_URL"),
    "projectId": os.getenv("PROJECT_ID"),
    "storageBucket": os.getenv("STORAGE_BUCKET"),
    "messagingSenderId": os.getenv("MESSAGING_SENDER_ID"),
    "appId": os.getenv("APP_ID")
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
db = firebase.database()

def get_user_data(user_id):
    """Fetch user data from Firebase Realtime Database."""
    return db.child("users").child(user_id).get().val()

def save_coin_data(user_id, coin_data):
    """Save user's coin data to Firebase."""
    db.child("users").child(user_id).child("coins").set(coin_data)

def update_boost_data(user_id, boost_data):
    """Update boost information."""
    db.child("users").child(user_id).child("boost").set(boost_data)
