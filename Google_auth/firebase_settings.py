# firebase_auth_project/firebase.py

import firebase_admin
from firebase_admin import credentials, auth

# Path to your Firebase service account key file
cred = credentials.Certificate('C:/Users/rakes/PycharmProjects/Google_auth/firebase-token.json')

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred)
