from ingestion_integration.lib.pg import get_conn, upsert_many
from ingestion_integration.lib.fs import stream_collection
from ingestion_integration.lib.utils import to_utc, to_text_array

UPSERT_SQL = """
INSERT INTO fact_feature_usage_monthly (
  feature_key, yyyymm, count
) VALUES (
  %(feature_key)s, %(yyyymm)s, %(count)s
)
ON CONFLICT (feature_key, yyyymm) DO UPDATE SET
  count=EXCLUDED.count;
"""

def run():
    rows = []
    for doc in stream_collection("feature_usage_monthly"):
        d = doc.to_dict()
        rows.append({
            "feature_key": d.get("featureKey"),
            "yyyymm": d.get("date"),   # stored as 'YYYY-MM'
            "count": int(d.get("count", 0))
        })
    if not rows:
        return
    with get_conn() as conn, conn.cursor() as cur:
        upsert_many(cur, UPSERT_SQL, rows)
        conn.commit()

if __name__ == "__main__":
    run()
