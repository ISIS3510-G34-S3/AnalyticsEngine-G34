import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from computation.regional_offers_analysis import (
    get_experience_offers_by_region,
    get_category_distribution_by_region,
    get_public_entity_insights,
    get_market_opportunity_analysis
)

st.set_page_config(
    page_title="Q12 - Regional Experience Offers", 
    page_icon="🌎", 
    layout="wide"
)

st.title("Q12: Regional Experience Offers Analysis for Public Entities")
st.markdown("""
**Business Question**: Which regions in Colombia have the greatest concentrations of experience offers, what are most of these offers typically like, and how could this information be useful to public entities?

**Analysis Type**: Type 4 - External Data Sharing  
**Purpose**: Analyze aggregated data for sharing with public entities to support regional development and policy making.
""")

# Load data
with st.spinner("Loading regional experience offers data..."):
    regional_offers = get_experience_offers_by_region()
    category_distribution = get_category_distribution_by_region()
    public_insights = get_public_entity_insights()
    market_analysis = get_market_opportunity_analysis()

# Executive Summary for Public Entities
st.header("🏛️ Executive Summary for Public Entities")

col1, col2, col3, col4 = st.columns(4)

total_experiences = regional_offers['total_experiences'].sum()
total_economic_impact = public_insights['economic_impact'].sum()
total_entrepreneurs = regional_offers['active_hosts'].sum()
avg_verification_rate = regional_offers['verification_rate'].mean()

with col1:
    st.metric(
        "Total Experience Supply", 
        f"{total_experiences:,}",
        delta="Across all regions"
    )

with col2:
    st.metric(
        "Economic Impact", 
        f"${total_economic_impact:,.0f} COP",
        delta="Annual tourism revenue"
    )

with col3:
    st.metric(
        "Tourism Entrepreneurs", 
        f"{total_entrepreneurs:,}",
        delta="Active hosts/businesses"
    )

with col4:
    st.metric(
        "Avg Verification Rate", 
        f"{avg_verification_rate:.1f}%",
        delta="Quality indicator"
    )

# Regional concentration analysis
st.header("🗺️ Regional Experience Offer Concentration")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Experience Supply by Department")
    
    # Create supply concentration chart
    fig_supply = px.bar(
        regional_offers.head(10),
        x='total_experiences',
        y='department',
        color='avg_price',
        title='Number of Experience Offers by Colombian Department',
        labels={
            'total_experiences': 'Number of Experience Offers',
            'department': 'Department',
            'avg_price': 'Average Price (COP)'
        },
        color_continuous_scale='Plasma',
        orientation='h'
    )
    fig_supply.update_layout(height=500)
    st.plotly_chart(fig_supply, use_container_width=True)

with col2:
    st.subheader("Top 5 Supply Regions")
    top_5_supply = regional_offers.head(5)
    for _, row in top_5_supply.iterrows():
        st.metric(
            row['department'],
            f"{row['total_experiences']:,} offers",
            delta=f"{row['active_hosts']:,} hosts"
        )

# Experience characteristics analysis
st.header("🔍 Experience Offer Characteristics")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Price Distribution by Region")
    fig_price = px.box(
        regional_offers.head(8),
        x='department',
        y='avg_price',
        title='Average Experience Prices by Department',
        labels={
            'avg_price': 'Average Price (COP)',
            'department': 'Department'
        }
    )
    fig_price.update_xaxis(tickangle=45)
    st.plotly_chart(fig_price, use_container_width=True)

with col2:
    st.subheader("Group Size Capacity")
    fig_capacity = px.scatter(
        regional_offers,
        x='total_experiences',
        y='avg_group_size',
        size='active_hosts',
        color='verification_rate',
        hover_data=['department'],
        title='Experience Capacity vs Supply',
        labels={
            'total_experiences': 'Number of Offers',
            'avg_group_size': 'Average Group Size',
            'verification_rate': 'Verification Rate %'
        }
    )
    st.plotly_chart(fig_capacity, use_container_width=True)

# Category analysis
st.header("🏷️ Experience Categories by Region")

if len(category_distribution) > 0:
    # Create category heatmap
    category_pivot = category_distribution.pivot_table(
        index='department', 
        columns='category', 
        values='category_count', 
        fill_value=0
    )
    
    fig_categories = px.imshow(
        category_pivot.head(8),
        title='Experience Category Distribution by Department',
        labels={'x': 'Experience Category', 'y': 'Department', 'color': 'Number of Offers'},
        color_continuous_scale='Blues'
    )
    st.plotly_chart(fig_categories, use_container_width=True)
    
    # Category insights
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Most Popular Categories")
        category_totals = category_distribution.groupby('category')['category_count'].sum().sort_values(ascending=False)
        st.bar_chart(category_totals.head(6))
    
    with col2:
        st.subheader("Category Price Analysis")
        category_prices = category_distribution.groupby('category')['avg_price_for_category'].mean().sort_values(ascending=False)
        st.bar_chart(category_prices.head(6))

# Public entity insights
st.header("🏛️ Strategic Insights for Public Entities")

st.markdown("""
### 📊 Policy Development & Economic Planning Data

This section provides actionable insights for public entities including tourism ministries, 
regional development agencies, and municipal governments.
""")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Economic Development Indicators")
    
    # Economic impact table
    economic_df = public_insights[['department', 'entrepreneurship_count', 'economic_impact', 
                                 'tourism_demand', 'infrastructure_capacity_needed']].copy()
    economic_df['economic_impact_millions'] = (economic_df['economic_impact'] / 1000000).round(1)
    
    st.dataframe(
        economic_df[['department', 'entrepreneurship_count', 'economic_impact_millions', 
                    'tourism_demand', 'infrastructure_capacity_needed']],
        use_container_width=True,
        column_config={
            'economic_impact_millions': 'Economic Impact (Millions COP)',
            'entrepreneurship_count': 'Entrepreneurs',
            'tourism_demand': 'Annual Visitors',
            'infrastructure_capacity_needed': 'Avg Group Size Need'
        }
    )

with col2:
    st.subheader("Market Development Opportunities")
    
    # Market opportunity analysis
    opportunity_df = market_analysis[['department', 'demand_supply_ratio', 
                                    'unverified_hosts_count', 'avg_unverified_price']].copy()
    opportunity_df['price_gap'] = (opportunity_df['avg_verified_price'] - opportunity_df['avg_unverified_price']).round(0)
    
    st.dataframe(
        opportunity_df[['department', 'demand_supply_ratio', 'unverified_hosts_count', 'price_gap']],
        use_container_width=True,
        column_config={
            'demand_supply_ratio': 'Demand/Supply Ratio',
            'unverified_hosts_count': 'Unverified Hosts',
            'price_gap': 'Verification Price Premium (COP)'
        }
    )

# Infrastructure planning
st.header("🏗️ Infrastructure & Development Planning")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 🚧 Infrastructure Needs
    **Based on Current Demand:**
    - Average group sizes require facilities for 6-8 people
    - High-demand regions need transportation infrastructure
    - Tourism service facilities (restrooms, parking, etc.)
    """)

with col2:
    st.markdown("""
    ### 📈 Economic Development
    **Tourism Industry Growth:**
    - Support for small tourism entrepreneurs
    - Quality certification programs
    - Marketing and promotion support
    """)

with col3:
    st.markdown("""
    ### 🔧 Regulatory Framework
    **Policy Recommendations:**
    - Host verification incentive programs
    - Tourism business registration streamlining
    - Safety and quality standards development
    """)

# Regional development priorities
st.header("🎯 Regional Development Priorities")

# Create priority matrix
priority_df = public_insights.copy()
priority_df['development_priority_score'] = (
    priority_df['economic_impact'] / priority_df['economic_impact'].max() * 0.4 +
    priority_df['entrepreneurship_count'] / priority_df['entrepreneurship_count'].max() * 0.3 +
    priority_df['tourism_demand'] / priority_df['tourism_demand'].max() * 0.3
) * 100

priority_df = priority_df.sort_values('development_priority_score', ascending=False)

fig_priority = px.scatter(
    priority_df.head(10),
    x='entrepreneurship_count',
    y='economic_impact',
    size='tourism_demand',
    color='development_priority_score',
    hover_data=['department'],
    title='Regional Development Priority Matrix',
    labels={
        'entrepreneurship_count': 'Number of Tourism Entrepreneurs',
        'economic_impact': 'Economic Impact (COP)',
        'tourism_demand': 'Tourism Demand',
        'development_priority_score': 'Development Priority Score'
    },
    color_continuous_scale='Reds'
)
st.plotly_chart(fig_priority, use_container_width=True)

# Public entity action items
st.header("📋 Action Items for Public Entities")

tab1, tab2, tab3 = st.tabs(["Tourism Ministries", "Regional Governments", "Municipal Authorities"])

with tab1:
    st.markdown("""
    ### 🏛️ National Tourism Ministry Actions
    
    **Policy Development:**
    - Create national tourism entrepreneur support programs
    - Develop quality certification standards for experience providers
    - Establish data sharing frameworks with private platforms
    
    **Investment Priorities:**
    - Focus on top 5 regions with highest economic impact
    - Develop infrastructure in high-demand, low-supply areas
    - Support verification and quality improvement programs
    
    **International Marketing:**
    - Promote regions with high authentic experience concentrations
    - Develop regional tourism brand strategies
    - Create international partnership opportunities
    """)

with tab2:
    st.markdown("""
    ### 🏢 Regional Government Actions
    
    **Economic Development:**
    - Support local tourism entrepreneur training programs
    - Develop regional tourism infrastructure
    - Create regional tourism promotion campaigns
    
    **Regulatory Framework:**
    - Streamline business registration for tourism providers
    - Develop regional safety and quality standards
    - Create incentive programs for host verification
    
    **Collaboration:**
    - Partner with private platforms for data sharing
    - Coordinate with national tourism policies
    - Develop inter-regional tourism circuits
    """)

with tab3:
    st.markdown("""
    ### 🏛️ Municipal Authority Actions
    
    **Local Infrastructure:**
    - Ensure adequate facilities for average group sizes (6-8 people)
    - Develop parking and transportation access
    - Maintain tourism sites and facilities
    
    **Business Support:**
    - Provide local business registration services
    - Offer municipal grants for tourism entrepreneurs
    - Create local tourism information services
    
    **Community Development:**
    - Engage local communities in tourism planning
    - Develop community-based tourism initiatives
    - Ensure sustainable tourism practices
    """)

# Data export for public entities
st.header("📊 Data Export for Public Entities")

col1, col2 = st.columns(2)

with col1:
    # Create comprehensive public entity report
    public_report = regional_offers.merge(
        public_insights[['department', 'economic_impact', 'entrepreneurship_count']], 
        on='department', 
        how='left'
    )
    
    csv_public = public_report.to_csv(index=False)
    st.download_button(
        label="Download Public Entity Report (CSV)",
        data=csv_public,
        file_name=f"colombia_tourism_regional_analysis_public_entities.csv",
        mime="text/csv"
    )

with col2:
    st.info("""
    **For Public Entity Partnerships:**
    
    📧 government.relations@travelapp.co
    📞 +57 (1) 123-4567 ext. 200
    🌐 www.travelapp.co/public-partnerships
    
    *Contact us for detailed regional reports and collaboration opportunities.*
    """)

# Raw data section
with st.expander("📊 View Raw Data"):
    tab1, tab2, tab3, tab4 = st.tabs(["Regional Offers", "Category Distribution", "Public Insights", "Market Analysis"])
    
    with tab1:
        st.dataframe(regional_offers, use_container_width=True)
    
    with tab2:
        st.dataframe(category_distribution, use_container_width=True)
    
    with tab3:
        st.dataframe(public_insights, use_container_width=True)
    
    with tab4:
        st.dataframe(market_analysis, use_container_width=True)

st.markdown("---")
st.markdown("**Data Source**: Analytics Pipeline | **Last Updated**: Real-time | **Question Owner**: Santiago Arenas")