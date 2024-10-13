import pyrebase
import os

# Initialize Firebase connection
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
db = firebase.database()

def get_user_data(user_id):
    """Fetch user data from Firebase by user ID."""
    user_data = db.child("users").child(user_id).get()
    return user_data.val() if user_data.val() else None

def save_user_data(user_id, user_data):
    """Save or update user data in Firebase."""
    db.child("users").child(user_id).set(user_data)
