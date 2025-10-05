from ingestion_integration.lib.pg import (
    get_conn,
    upsert_many,
    get_highwater,
    set_highwater,  # <-- make sure this is imported
)
from ingestion_integration.lib.fs import stream_collection
from ingestion_integration.lib.utils import to_utc

UPSERT_SQL = """
INSERT INTO fact_booking (
  booking_id, experience_id, host_id, traveler_id, people_count, amount_cop, created_at_utc
) VALUES (
  %(booking_id)s, %(experience_id)s, %(host_id)s, %(traveler_id)s, %(people_count)s, %(amount_cop)s, %(created_at_utc)s
)
ON CONFLICT (booking_id) DO UPDATE SET
  experience_id=EXCLUDED.experience_id,
  host_id=EXCLUDED.host_id,
  traveler_id=EXCLUDED.traveler_id,
  people_count=EXCLUDED.people_count,
  amount_cop=EXCLUDED.amount_cop,
  created_at_utc=EXCLUDED.created_at_utc;
"""

SOURCE_KEY = "bookings"

def _coerce_int(v):
    if v is None or v == "":
        return None
    try:
        return int(v)
    except Exception:
        return None

def run():
    docs = list(stream_collection("bookings"))
    rows = []
    skipped = 0
    new_highwater = None

    for doc in docs:
        d = doc.to_dict() or {}
        created = to_utc(d.get("createdAt"))
        exp_id = d.get("expId")
        host_id = d.get("hostId")

        # Minimal validation: we need exp_id, host_id, created
        if not exp_id or not host_id or created is None:
            skipped += 1
            print(f"[WARN] Skipping booking {doc.id}: "
                  f"expId={exp_id!r}, hostId={host_id!r}, createdAt={created!r}")
            continue

        rows.append({
            "booking_id": doc.id,
            "experience_id": exp_id,
            "host_id": host_id,
            "traveler_id": d.get("travelerId"),
            "people_count": _coerce_int(d.get("peopleCount")) or 0,
            "amount_cop": _coerce_int(d.get("amountCOP")),
            "created_at_utc": created
        })

        if (new_highwater is None) or (created > new_highwater):
            new_highwater = created

    if not rows:
        print("[INFO] No valid bookings to upsert.")
        if skipped:
            print(f"[INFO] Skipped {skipped} booking(s) due to missing required fields.")
        return

    with get_conn() as conn, conn.cursor() as cur:
        upsert_many(cur, UPSERT_SQL, rows)
        if new_highwater is not None:
            set_highwater(cur, SOURCE_KEY, new_highwater)
        conn.commit()

    print(f"[OK] Upserted {len(rows)} booking(s). Skipped {skipped}.")

if __name__ == "__main__":
    run()
