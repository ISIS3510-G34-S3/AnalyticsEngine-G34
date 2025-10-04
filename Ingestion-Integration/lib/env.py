import os
from dotenv import load_dotenv

load_dotenv()

PG_DSN = (
    f"host={os.getenv('PGHOST')} port={os.getenv('PGPORT')} "
    f"dbname={os.getenv('PGDATABASE')} user={os.getenv('PGUSER')} password={os.getenv('PGPASSWORD')}"
)

GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
INGESTION_WATERMARK_DAYS = int(os.getenv("INGESTION_WATERMARK_DAYS", "90"))
