# computation/skills_top_departments.py
import os
import psycopg
import pandas as pd
from typing import List
from dotenv import load_dotenv, find_dotenv

def _pg_dsn_from_env() -> str:
    load_dotenv(find_dotenv(filename=".env", usecwd=True))
    host = os.getenv("PGHOST", "localhost")
    port = os.getenv("PGPORT", "5432")
    db   = os.getenv("PGDATABASE", "analytics")
    user = os.getenv("PGUSER", "analytics_user")
    pwd  = os.getenv("PGPASSWORD", "supersecret")
    return f"host={host} port={port} dbname={db} user={user} password={pwd}"

def get_top_departments(limit: int = 5) -> List[str]:
    sql = """
        SELECT department
        FROM (
            SELECT department, COUNT(*) AS cnt
            FROM dim_experience
            WHERE is_active = TRUE AND department IS NOT NULL AND department <> ''
            GROUP BY department
            ORDER BY cnt DESC
            LIMIT %s
        ) t;
    """
    with psycopg.connect(_pg_dsn_from_env()) as conn:
        rows = conn.execute(sql, (limit,)).fetchall()
    return [r[0] for r in rows]

def get_overall_skill_counts_in_top_departments(limit_depts: int = 5) -> pd.DataFrame:
    """
    Counts skills across experiences in the top-N departments.
    Columns: skill, total_count
    """
    sql = """
    WITH top_depts AS (
        SELECT department
        FROM (
            SELECT department, COUNT(*) AS cnt
            FROM dim_experience
            WHERE is_active = TRUE AND department IS NOT NULL AND department <> ''
            GROUP BY department
            ORDER BY cnt DESC
            LIMIT %s
        ) t
    )
    SELECT s.skill, COUNT(*)::BIGINT AS total_count
    FROM dim_experience e
    JOIN top_depts d ON e.department = d.department
    JOIN dim_experience_skill s ON s.experience_id = e.experience_id
    WHERE e.is_active = TRUE
      AND s.skill IS NOT NULL AND s.skill <> ''
    GROUP BY s.skill
    ORDER BY total_count DESC, s.skill ASC;
    """
    with psycopg.connect(_pg_dsn_from_env()) as conn:
        df = pd.read_sql(sql, conn, params=(limit_depts,))
    return df

def get_skill_counts_by_department(limit_depts: int = 5) -> pd.DataFrame:
    """
    Counts skills per department for the top-N departments.
    Columns: department, skill, count
    """
    sql = """
    WITH top_depts AS (
        SELECT department
        FROM (
            SELECT department, COUNT(*) AS cnt
            FROM dim_experience
            WHERE is_active = TRUE AND department IS NOT NULL AND department <> ''
            GROUP BY department
            ORDER BY cnt DESC
            LIMIT %s
        ) t
    )
    SELECT e.department, s.skill, COUNT(*)::BIGINT AS count
    FROM dim_experience e
    JOIN top_depts d ON e.department = d.department
    JOIN dim_experience_skill s ON s.experience_id = e.experience_id
    WHERE e.is_active = TRUE
      AND s.skill IS NOT NULL AND s.skill <> ''
    GROUP BY e.department, s.skill
    ORDER BY e.department ASC, count DESC, s.skill ASC;
    """
    with psycopg.connect(_pg_dsn_from_env()) as conn:
        df = pd.read_sql(sql, conn, params=(limit_depts,))
    return df