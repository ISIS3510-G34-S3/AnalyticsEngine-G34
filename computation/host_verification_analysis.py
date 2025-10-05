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

def get_host_verification_analysis() -> pd.DataFrame:
    """
    Q9: How does the host verification feature affect the number of bookings 
    compared to unverified hosts?
    
    Returns a DataFrame with columns: host_verified, total_bookings, avg_booking_amount, booking_count
    """
    # Always return mock data for demo purposes
    return pd.DataFrame({
        'host_verified': [True, False],
        'total_bookings': [1250, 890],
        'avg_booking_amount': [185000, 145000],
        'unique_hosts': [85, 120],
        'total_revenue': [231250000, 129050000]
    })

def get_detailed_host_verification_metrics() -> pd.DataFrame:
    """
    Get more detailed metrics for host verification analysis
    """
    # Always return mock data for demo purposes
    departments = ['Cundinamarca', 'Antioquia', 'Valle del Cauca', 'Atlántico', 'Santander']
    mock_data = []
    for verified in [True, False]:
        for dept in departments:
            base_bookings = 200 if verified else 150
            variation = hash(dept) % 100
            mock_data.append({
                'host_verified': verified,
                'department': dept,
                'bookings_count': base_bookings + variation,
                'avg_amount': (180000 if verified else 140000) + (variation * 1000),
                'experiences_count': (25 if verified else 35) + (variation % 20)
            })
    return pd.DataFrame(mock_data)