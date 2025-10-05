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

def get_authentic_experience_bookings_by_region() -> pd.DataFrame:
    """
    Q11: Which regions in Colombia show the highest concentration of authentic 
    experience bookings and how could this aggregated data be shared with 
    regional tourism boards?
    
    Returns a DataFrame with columns: department, authentic_bookings, total_bookings, 
    authentic_percentage, total_revenue, avg_booking_value
    """
    # Always return mock data for demo purposes
    return pd.DataFrame({
        'department': ['Cundinamarca', 'Antioquia', 'Valle del Cauca', 'Bolívar', 'Magdalena', 
                      'Santander', 'Quindío', 'Risaralda', 'Caldas', 'Nariño'],
        'authentic_bookings': [485, 392, 278, 215, 198, 175, 145, 132, 118, 95],
        'total_bookings': [1250, 980, 750, 520, 445, 380, 295, 265, 240, 180],
        'authentic_percentage': [38.8, 40.0, 37.1, 41.3, 44.5, 46.1, 49.2, 49.8, 49.2, 52.8],
        'authentic_revenue': [89250000, 72440000, 51060000, 39925000, 36630000, 
                            31325000, 26100000, 23760000, 21240000, 17100000],
        'avg_authentic_booking_value': [184000, 184900, 183700, 185700, 185000, 
                                      179000, 180000, 180000, 180000, 180000]
    })

def get_tourism_board_report_data() -> pd.DataFrame:
    """
    Get detailed data for sharing with regional tourism boards
    """
    # Always return mock data for demo purposes
    return pd.DataFrame({
        'department': ['Cundinamarca', 'Antioquia', 'Valle del Cauca', 'Bolívar', 'Magdalena'],
        'category_focus': ['authentic'] * 5,
        'unique_experiences': [125, 98, 75, 55, 48],
        'total_bookings': [485, 392, 278, 215, 198],
        'avg_booking_value': [184000, 184900, 183700, 185700, 185000],
        'total_revenue': [89250000, 72440000, 51060000, 39925000, 36630000],
        'unique_hosts': [95, 78, 62, 45, 40],
        'avg_group_size': [6, 7, 6, 8, 7],
        'active_months': [12, 11, 10, 9, 8]
    })

def get_seasonal_authentic_trends() -> pd.DataFrame:
    """
    Get seasonal trends for authentic experiences by region
    """
    # Always return mock data for demo purposes
    import random
    mock_data = []
    departments = ['Cundinamarca', 'Antioquia', 'Valle del Cauca', 'Bolívar', 'Magdalena']
    for dept in departments:
        base_bookings = {'Cundinamarca': 40, 'Antioquia': 33, 'Valle del Cauca': 23, 
                       'Bolívar': 18, 'Magdalena': 16}[dept]
        for month in range(1, 13):
            # Simulate seasonal variations
            seasonal_factor = 1.0
            if month in [12, 1, 6, 7]:  # High season
                seasonal_factor = 1.4
            elif month in [2, 3, 9, 10]:  # Medium season
                seasonal_factor = 1.1
            
            bookings = int(base_bookings * seasonal_factor * random.uniform(0.8, 1.2))
            revenue = bookings * 184000  # Average booking value
            
            mock_data.append({
                'department': dept,
                'month': month,
                'bookings': bookings,
                'revenue': revenue
            })
    return pd.DataFrame(mock_data)