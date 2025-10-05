import psycopg
from .env import PG_DSN

def get_conn():
    return psycopg.connect(PG_DSN)

def upsert_many(cur, sql, rows):
    cur.executemany(sql, rows)

def get_highwater(cur, source_key):
    cur.execute("SELECT highwater FROM ingestion_state WHERE source_key=%(k)s", {"k": source_key})
    r = cur.fetchone()
    return r[0] if r else None

def set_highwater(cur, source_key, ts):
    cur.execute("""
        INSERT INTO ingestion_state (source_key, highwater)
        VALUES (%(k)s, %(ts)s)
        ON CONFLICT (source_key) DO UPDATE SET highwater=EXCLUDED.highwater
    """, {"k": source_key, "ts": ts})
