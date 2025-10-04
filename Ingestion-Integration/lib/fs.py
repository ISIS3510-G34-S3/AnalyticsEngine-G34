import os
from google.cloud import firestore

def get_fs():
    # Service account path is read from GOOGLE_APPLICATION_CREDENTIALS
    return firestore.Client()

def stream_collection(col_name):
    db = get_fs()
    return db.collection(col_name).stream()

def stream_subcollection_group(name):  # e.g., 'availability'
    db = get_fs()
    return db.collection_group(name).stream()
