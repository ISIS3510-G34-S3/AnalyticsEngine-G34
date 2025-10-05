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

def get_experience_offers_by_region() -> pd.DataFrame:
    """
    Q12: Which regions in Colombia have the greatest concentrations of experience 
    offers, what are most of these offers typically like, and how could this 
    information be useful to public entities?
    
    Returns a DataFrame with columns: department, total_experiences, avg_price, 
    most_common_category, avg_group_size, active_hosts
    """
    # Always return mock data for demo purposes
    return pd.DataFrame({
        'department': ['Cundinamarca', 'Antioquia', 'Valle del Cauca', 'Bolívar', 'Atlántico', 
                      'Santander', 'Quindío', 'Risaralda', 'Caldas', 'Magdalena'],
        'total_experiences': [342, 285, 198, 156, 134, 125, 89, 78, 67, 54],
        'avg_price': [165000, 158000, 172000, 145000, 155000, 162000, 148000, 151000, 159000, 142000],
        'avg_group_size': [6.5, 7.2, 6.8, 8.1, 6.9, 6.4, 5.8, 6.2, 6.6, 7.5],
        'active_hosts': [245, 198, 145, 112, 98, 89, 67, 58, 52, 41],
        'verified_experiences': [189, 142, 108, 78, 67, 62, 45, 39, 33, 27],
        'verification_rate': [55.3, 49.8, 54.5, 50.0, 50.0, 49.6, 50.6, 50.0, 49.3, 50.0]
    })

def get_category_distribution_by_region() -> pd.DataFrame:
    """
    Get the distribution of experience categories by region
    """
    # Always return mock data for demo purposes
    departments = ['Cundinamarca', 'Antioquia', 'Valle del Cauca', 'Bolívar', 'Atlántico']
    categories = ['cultural', 'adventure', 'gastronomic', 'authentic', 'nature', 'historical']
    mock_data = []
    
    for dept in departments:
        base_count = {'Cundinamarca': 60, 'Antioquia': 50, 'Valle del Cauca': 40, 
                     'Bolívar': 30, 'Atlántico': 25}[dept]
        
        for i, category in enumerate(categories):
            # Simulate different popularity for different categories
            popularity_factor = [1.0, 0.8, 0.9, 0.6, 0.7, 0.5][i]
            count = int(base_count * popularity_factor)
            price = 150000 + (i * 10000) + (hash(dept + category) % 30000)
            
            mock_data.append({
                'department': dept,
                'category': category,
                'category_count': count,
                'avg_price_for_category': price
            })
    
    return pd.DataFrame(mock_data)

def get_public_entity_insights() -> pd.DataFrame:
    """
    Get insights specifically useful for public entities (tourism development, 
    economic planning, infrastructure needs)
    """
    # Always return mock data for demo purposes
    return pd.DataFrame({
        'department': ['Cundinamarca', 'Antioquia', 'Valle del Cauca', 'Bolívar', 'Atlántico'],
        'supply_density': [342, 285, 198, 156, 134],
        'avg_experience_price': [165000, 158000, 172000, 145000, 155000],
        'entrepreneurship_count': [245, 198, 145, 112, 98],
        'economic_impact': [564300000, 450300000, 340560000, 226080000, 207700000],
        'tourism_demand': [3420, 2850, 1980, 1560, 1340],
        'infrastructure_capacity_needed': [7, 7, 7, 8, 7]
    })

def get_market_opportunity_analysis() -> pd.DataFrame:
    """
    Analyze market opportunities and gaps for public policy development
    """
    # Always return mock data for demo purposes
    return pd.DataFrame({
        'department': ['Cundinamarca', 'Antioquia', 'Valle del Cauca', 'Bolívar', 'Atlántico'],
        'current_supply': [342, 285, 198, 156, 134],
        'current_demand': [3420, 2850, 1980, 1560, 1340],
        'demand_supply_ratio': [10.0, 10.0, 10.0, 10.0, 10.0],
        'unverified_hosts_count': [153, 143, 90, 78, 67],
        'avg_unverified_price': [155000, 148000, 162000, 135000, 145000],
        'avg_verified_price': [175000, 168000, 182000, 155000, 165000]
    })