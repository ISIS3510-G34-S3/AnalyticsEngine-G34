from ingestion_integration.lib.pg import get_conn, upsert_many
from ingestion_integration.lib.fs import stream_subcollection_group
from ingestion_integration.lib.utils import to_utc

UPSERT_SQL = """
INSERT INTO fact_availability_slot (
  experience_id, start_utc, end_utc, capacity_total, capacity_remaining
) VALUES (
  %(experience_id)s, %(start_utc)s, %(end_utc)s, %(capacity_total)s, %(capacity_remaining)s
)
ON CONFLICT (experience_id, start_utc, end_utc) DO UPDATE SET
  capacity_total=EXCLUDED.capacity_total,
  capacity_remaining=EXCLUDED.capacity_remaining;
"""

def run():
    rows = []
    for snap in stream_subcollection_group("availability"):
        d = snap.to_dict() or {}
        exp_id = snap.reference.parent.parent.id  # experiences/{expId}/availability/{slotId}

        rows.append({
            "experience_id": exp_id,
            "start_utc": to_utc(d.get("start")),
            "end_utc": to_utc(d.get("end")),
            "capacity_total": int(d.get("capacityTotal", 0)),
            "capacity_remaining": int(d.get("capacityRemaining", 0)),
        })

    if not rows:
        print("[INFO] No availability slots found.")
        return

    with get_conn() as conn, conn.cursor() as cur:
        upsert_many(cur, UPSERT_SQL, rows)
        conn.commit()
    print(f"[OK] Upserted {len(rows)} availability slot(s).")

if __name__ == "__main__":
    run()
