# ingestion_integration/jobs/load_experiences.py
from datetime import datetime, timezone
from ingestion_integration.lib.pg import get_conn, upsert_many
from ingestion_integration.lib.fs import stream_collection
from ingestion_integration.lib.utils import to_utc, to_text_array

UPSERT_SQL = """
INSERT INTO dim_experience (
  experience_id, host_id, department, host_verified, is_active,
  categories, price_cop, group_size_max, created_at_utc, updated_at_utc
) VALUES (
  %(experience_id)s, %(host_id)s, %(department)s, %(host_verified)s, %(is_active)s,
  %(categories)s, %(price_cop)s, %(group_size_max)s, %(created_at_utc)s, %(updated_at_utc)s
)
ON CONFLICT (experience_id) DO UPDATE SET
  host_id=EXCLUDED.host_id,
  department=EXCLUDED.department,
  host_verified=EXCLUDED.host_verified,
  is_active=EXCLUDED.is_active,
  categories=EXCLUDED.categories,
  price_cop=EXCLUDED.price_cop,
  group_size_max=EXCLUDED.group_size_max,
  created_at_utc=EXCLUDED.created_at_utc,
  updated_at_utc=EXCLUDED.updated_at_utc;
"""

def _coerce_int(v):
    if v is None or v == "":
        return None
    try:
        return int(v)
    except Exception:
        return None

def run():
    rows = []
    skipped = 0

    for doc in stream_collection("experiences"):
        d = doc.to_dict() or {}

        host_id = d.get("hostId")
        department = d.get("department")
        host_verified = bool(d.get("hostVerified", False))
        is_active = bool(d.get("isActive", False))
        categories = to_text_array(d.get("categories", []))

        # price/group size are optional
        price_cop = _coerce_int(d.get("priceCOP"))
        group_size_max = _coerce_int(d.get("groupSizeMax"))

        # timestamps: require created_at_utc; fallback to updatedAt; finally now()
        created_at = to_utc(d.get("createdAt")) or to_utc(d.get("updatedAt")) or datetime.now(timezone.utc)
        updated_at = to_utc(d.get("updatedAt"))

        # Validate required fields for NOT NULL columns
        # Required by schema: host_id, department, host_verified, is_active, categories, created_at_utc
        if not host_id or not department or created_at is None:
            skipped += 1
            print(f"[WARN] Skipping experience {doc.id}: "
                  f"hostId={host_id!r}, department={department!r}, createdAt={created_at!r}")
            continue

        rows.append({
            "experience_id": doc.id,
            "host_id": host_id,
            "department": department,
            "host_verified": host_verified,
            "is_active": is_active,
            "categories": categories,
            "price_cop": price_cop,
            "group_size_max": group_size_max,
            "created_at_utc": created_at,
            "updated_at_utc": updated_at
        })

    if not rows:
        print("[INFO] No valid experiences to upsert.")
        if skipped:
            print(f"[INFO] Skipped {skipped} experience(s) due to missing required fields.")
        return

    with get_conn() as conn, conn.cursor() as cur:
        upsert_many(cur, UPSERT_SQL, rows)
        conn.commit()

    print(f"[OK] Upserted {len(rows)} experience(s). Skipped {skipped}.")
    
if __name__ == "__main__":
    run()
