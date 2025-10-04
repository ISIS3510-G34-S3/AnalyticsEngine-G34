import psycopg2
import psycopg2.extras
from .env import PG_DSN

def get_conn():
    return psycopg2.connect(PG_DSN)

def upsert_many(cur, sql, rows):
    psycopg2.extras.execute_batch(cur, sql, rows, page_size=1000)

def get_highwater(cur, source_key):
    cur.execute("SELECT highwater FROM ingestion_state WHERE source_key=%s", (source_key,))
    r = cur.fetchone()
    return r[0] if r else None

def set_highwater(cur, source_key, ts):
    cur.execute("""
        INSERT INTO ingestion_state (source_key, highwater)
        VALUES (%s, %s)
        ON CONFLICT (source_key) DO UPDATE SET highwater=EXCLUDED.highwater
    """, (source_key, ts))
