from ingestion_integration.lib.fs import stream_collection
from ingestion_integration.lib.pg import get_conn, upsert_many
import re

COLLECTION = "device_distribution"  # adjust if your collection has a different name

UPSERT_SQL = """
INSERT INTO fact_device_usage_monthly (yyyymm, count)
VALUES (%s, %s)
ON CONFLICT (yyyymm) DO UPDATE SET
  count = EXCLUDED.count;
"""

def extract_yyyymm(doc_id: str, fallback: str | None) -> str | None:
    """
    Accepts doc id like 'device_YYYY-MM'. If not matched, tries fallback 'YYYY-MM'.
    Returns 'YYYY-MM' or None.
    """
    m = re.match(r"device_(\d{4}-\d{2})$", doc_id or "")
    if m:
        return m.group(1)
    if fallback and re.match(r"^\d{4}-\d{2}$", fallback):
        return fallback
    return None

def run():
    rows = []
    for snap in stream_collection(COLLECTION):
        d = snap.to_dict() or {}
        doc_id = snap.id
        yyyymm = extract_yyyymm(doc_id, d.get("date"))
        cnt = d.get("count")

        if yyyymm is None or cnt is None:
            print(f"[WARN] Skipping doc {doc_id}: yyyymm={yyyymm}, count={cnt}")
            continue

        rows.append((yyyymm, int(cnt)))

    if not rows:
        print("[OK] No device usage rows to upsert.")
        return

    with get_conn() as conn:
        with conn.cursor() as cur:
            upsert_many(cur, UPSERT_SQL, rows)
    print(f"[OK] Upserted {len(rows)} device usage row(s).")

if __name__ == "__main__":
    run()
