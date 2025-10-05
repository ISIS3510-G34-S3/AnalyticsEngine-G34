import os
from dotenv import load_dotenv, find_dotenv

# find nearest .env starting from current working dir
load_dotenv(find_dotenv(filename=".env", usecwd=True))

PG_DSN = (
    f"host={os.getenv('PGHOST')} port={os.getenv('PGPORT')} "
    f"dbname={os.getenv('PGDATABASE')} user={os.getenv('PGUSER')} password={os.getenv('PGPASSWORD')}"
)

GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
INGESTION_WATERMARK_DAYS = int(os.getenv("INGESTION_WATERMARK_DAYS", "90"))
