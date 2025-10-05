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

def list_available_months():
    sql = "SELECT DISTINCT yyyymm FROM fact_feature_usage_monthly ORDER BY yyyymm DESC;"
    with psycopg.connect(_pg_dsn_from_env()) as conn:
        return [r[0] for r in conn.execute(sql).fetchall()]

def get_least_used_features(yyyymm: str) -> pd.DataFrame:
    """
    Returns a DataFrame with columns: feature_key, yyyymm, count
    Ordered by count ASC (least used first) for the given month.
    """
    sql = """
        SELECT feature_key, yyyymm, count
        FROM fact_feature_usage_monthly
        WHERE yyyymm = %s
        ORDER BY count ASC, feature_key ASC;
    """
    with psycopg.connect(_pg_dsn_from_env()) as conn:
        df = pd.read_sql(sql, conn, params=(yyyymm,))
    return df
