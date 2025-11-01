# computation/device_distribution.py
import os
import psycopg
import pandas as pd
from dotenv import load_dotenv, find_dotenv

def _pg_dsn_from_env() -> str:
    load_dotenv(find_dotenv(filename=".env", usecwd=True))
    host = os.getenv("PGHOST", "localhost")
    port = os.getenv("PGPORT", "5432")
    db   = os.getenv("PGDATABASE", "analytics")
    user = os.getenv("PGUSER", "analytics_user")
    pwd  = os.getenv("PGPASSWORD", "supersecret")
    return f"host={host} port={port} dbname={db} user={user} password={pwd}"

def list_available_months() -> list[str]:
    sql = "SELECT DISTINCT yyyymm FROM fact_device_distribution_monthly ORDER BY yyyymm DESC;"
    with psycopg.connect(_pg_dsn_from_env()) as conn:
        return [r[0] for r in conn.execute(sql).fetchall()]

def get_device_distribution(yyyymm: str) -> pd.DataFrame:
    """
    Returns columns: device, yyyymm, count, share (share in % for the selected month)
    Ordered by count DESC (most prevalent first).
    """
    sql = """
        SELECT device, yyyymm, count
        FROM fact_device_distribution_monthly
        WHERE yyyymm = %s
        ORDER BY count DESC, device ASC;
    """
    with psycopg.connect(_pg_dsn_from_env()) as conn:
        df = pd.read_sql(sql, conn, params=(yyyymm,))
    if not df.empty:
        total = df["count"].sum()
        df["share"] = (df["count"] / total) * 100.0 if total else 0.0
    else:
        df["share"] = []
    return df
