from google.cloud import firestore
from google.oauth2 import service_account
from .env import GOOGLE_APPLICATION_CREDENTIALS, GCP_PROJECT_ID

def get_fs():
    creds = service_account.Credentials.from_service_account_file(GOOGLE_APPLICATION_CREDENTIALS)
    return firestore.Client(project=GCP_PROJECT_ID, credentials=creds)

def stream_collection(col_name):
    return get_fs().collection(col_name).stream()

def stream_subcollection_group(name):
    return get_fs().collection_group(name).stream()
