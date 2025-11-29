import sys
import os

# Add project root to path so we can import ingestion_integration when running as a script
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from ingestion_integration.lib.pg import (
    get_conn,
    upsert_many
)
from ingestion_integration.lib.fs import get_fs

# We only have one row to update, so we can just delete and insert, or upsert with a lock.
# Since there's no primary key that is stable (it's a singleton), 
# we'll just clear the table and insert the new single row.
INSERT_SQL = """
TRUNCATE fact_messaging_global_usage;
INSERT INTO fact_messaging_global_usage (last_chat_started_at, total_chats_started)
VALUES (%(last_chat_started_at)s, %(total_chats_started)s);
"""

def run():
    db = get_fs()
    doc_ref = db.collection("analytics").document("messaging_global_usage")
    doc = doc_ref.get()

    if not doc.exists:
        print("[WARN] Document analytics/messaging_global_usage does not exist.")
        return

    data = doc.to_dict()
    
    # Extract fields
    # The timestamp in Firestore comes as a datetime object usually, 
    # but here we'll convert it to string or keep it as is depending on how we want to store it.
    # The user prompt showed a string representation, but Firestore SDK usually returns datetime.
    # We'll cast to string to match the schema TEXT.
    last_chat = data.get("last_chat_started_at")
    total_chats = data.get("total_chats_started", 0)

    row = {
        "last_chat_started_at": str(last_chat) if last_chat else None,
        "total_chats_started": int(total_chats)
    }

    with get_conn() as conn, conn.cursor() as cur:
        # Use separate execute calls to avoid "multiple commands" error
        cur.execute("TRUNCATE fact_messaging_global_usage;")
        cur.execute("""
            INSERT INTO fact_messaging_global_usage (last_chat_started_at, total_chats_started)
            VALUES (%(last_chat_started_at)s, %(total_chats_started)s);
        """, row)
        conn.commit()

    print(f"[OK] Updated messaging global usage: {row}")

if __name__ == "__main__":
    run()
