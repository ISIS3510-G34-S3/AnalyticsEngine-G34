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

from computation.authentic_experiences_analysis import (
    get_authentic_experience_bookings_by_region,
    get_tourism_board_report_data,
    get_seasonal_authentic_trends
)

st.set_page_config(
    page_title="Q11 - Authentic Experience Regions", 
    page_icon="🏛️", 
    layout="wide"
)

st.title("Q11: Authentic Experience Bookings by Colombian Regions")
st.markdown("""
**Business Question**: Which regions in Colombia show the highest concentration of authentic experience bookings and how could this aggregated data be shared with regional tourism boards?

**Analysis Type**: Type 4 - External Data Sharing  
**Purpose**: Analyze geospatial data to identify market trends for strategic partnerships with Colombian tourism boards.
""")

# Load data
with st.spinner("Loading authentic experience data..."):
    regional_data = get_authentic_experience_bookings_by_region()
    tourism_board_data = get_tourism_board_report_data()
    seasonal_data = get_seasonal_authentic_trends()

# Key metrics
st.header("📈 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

total_authentic_bookings = regional_data['authentic_bookings'].sum()
total_revenue = regional_data['authentic_revenue'].sum()
avg_authentic_percentage = regional_data['authentic_percentage'].mean()
top_region = regional_data.iloc[0]['department'] if len(regional_data) > 0 else "N/A"

with col1:
    st.metric(
        "Total Authentic Bookings", 
        f"{total_authentic_bookings:,}",
        delta="Across all regions"
    )

with col2:
    st.metric(
        "Total Authentic Revenue", 
        f"${total_revenue:,.0f} COP",
        delta="Economic impact"
    )

with col3:
    st.metric(
        "Average Authentic %", 
        f"{avg_authentic_percentage:.1f}%",
        delta="Of total bookings"
    )

with col4:
    st.metric(
        "Leading Region", 
        top_region,
        delta=f"{regional_data.iloc[0]['authentic_bookings']:,} bookings" if len(regional_data) > 0 else "0 bookings"
    )

# Main visualization
st.header("🗺️ Regional Distribution of Authentic Experience Bookings")

col1, col2 = st.columns([2, 1])

with col1:
    # Interactive map-style visualization
    fig_map = px.bar(
        regional_data.head(10), 
        x='authentic_bookings', 
        y='department',
        color='authentic_percentage',
        title='Authentic Experience Bookings by Colombian Department',
        labels={
            'authentic_bookings': 'Number of Authentic Bookings',
            'department': 'Department',
            'authentic_percentage': 'Authentic %'
        },
        color_continuous_scale='Viridis',
        orientation='h'
    )
    fig_map.update_layout(height=500)
    st.plotly_chart(fig_map, use_container_width=True)

with col2:
    st.subheader("Top 5 Regions")
    top_5 = regional_data.head(5)
    for _, row in top_5.iterrows():
        st.metric(
            row['department'],
            f"{row['authentic_bookings']:,} bookings",
            delta=f"{row['authentic_percentage']:.1f}% authentic"
        )

# Revenue analysis
st.header("💰 Economic Impact Analysis")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Revenue by Region")
    fig_revenue = px.pie(
        regional_data.head(8), 
        values='authentic_revenue', 
        names='department',
        title='Authentic Experience Revenue Distribution'
    )
    st.plotly_chart(fig_revenue, use_container_width=True)

with col2:
    st.subheader("Booking Value Analysis")
    fig_value = px.scatter(
        regional_data,
        x='authentic_bookings',
        y='avg_authentic_booking_value',
        size='authentic_revenue',
        color='authentic_percentage',
        hover_data=['department'],
        title='Bookings vs Average Value',
        labels={
            'authentic_bookings': 'Number of Bookings',
            'avg_authentic_booking_value': 'Average Booking Value (COP)',
            'authentic_percentage': 'Authentic %'
        }
    )
    st.plotly_chart(fig_value, use_container_width=True)

# Seasonal trends
st.header("📅 Seasonal Trends Analysis")

if len(seasonal_data) > 0:
    # Create monthly trends chart
    fig_seasonal = px.line(
        seasonal_data[seasonal_data['department'].isin(regional_data.head(5)['department'])],
        x='month',
        y='bookings',
        color='department',
        title='Monthly Authentic Experience Bookings - Top 5 Regions',
        labels={
            'month': 'Month',
            'bookings': 'Number of Bookings',
            'department': 'Department'
        }
    )
    fig_seasonal.update_xaxis(
        tickmode='array',
        tickvals=list(range(1, 13)),
        ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    )
    st.plotly_chart(fig_seasonal, use_container_width=True)
else:
    st.info("Seasonal data not available. Using aggregated yearly data.")

# Tourism Board Report Section
st.header("🏛️ Tourism Board Partnership Report")

st.markdown("""
### 📋 Executive Summary for Regional Tourism Boards

This section provides aggregated insights specifically designed for sharing with Colombian regional tourism boards to support strategic planning and tourism development initiatives.
""")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Market Opportunity Analysis")
    
    # Create a comprehensive report dataframe
    if len(tourism_board_data) > 0:
        report_df = tourism_board_data.copy()
        report_df['market_potential_score'] = (
            report_df['total_revenue'] / report_df['total_revenue'].max() * 0.4 +
            report_df['total_bookings'] / report_df['total_bookings'].max() * 0.3 +
            report_df['unique_hosts'] / report_df['unique_hosts'].max() * 0.3
        ) * 100
        
        st.dataframe(
            report_df[['department', 'unique_experiences', 'total_bookings', 
                      'total_revenue', 'unique_hosts', 'market_potential_score']].round(1),
            use_container_width=True
        )

with col2:
    st.subheader("Infrastructure & Development Needs")
    
    if len(tourism_board_data) > 0:
        infrastructure_df = tourism_board_data[['department', 'avg_group_size', 
                                              'unique_hosts', 'active_months']].copy()
        infrastructure_df['capacity_utilization'] = (
            infrastructure_df['active_months'] / 12 * 100
        ).round(1)
        
        st.dataframe(infrastructure_df, use_container_width=True)

# Actionable insights for tourism boards
st.header("🎯 Strategic Recommendations for Tourism Boards")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 🚀 High-Priority Regions
    **Immediate Investment Opportunities:**
    - Focus on top 3 regions with highest authentic booking concentration
    - Develop infrastructure to support average group sizes of 6-8 people
    - Create authentic experience certification programs
    """)

with col2:
    st.markdown("""
    ### 🔧 Development Areas
    **Capacity Building Needs:**
    - Host training programs for authentic experience delivery
    - Marketing support for regional authentic experiences
    - Seasonal demand management strategies
    """)

with col3:
    st.markdown("""
    ### 🤝 Partnership Opportunities
    **Collaboration Framework:**
    - Data sharing agreements for market intelligence
    - Joint marketing campaigns for authentic experiences
    - Quality assurance and certification programs
    """)

# Export functionality for tourism boards
st.header("📊 Data Export for Tourism Boards")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Download Regional Report")
    
    # Create downloadable CSV
    export_data = regional_data.merge(
        tourism_board_data[['department', 'unique_experiences', 'unique_hosts']], 
        on='department', 
        how='left'
    )
    
    csv_data = export_data.to_csv(index=False)
    st.download_button(
        label="Download Regional Analysis (CSV)",
        data=csv_data,
        file_name=f"authentic_experiences_regional_analysis.csv",
        mime="text/csv"
    )

with col2:
    st.subheader("Partnership Contact")
    st.info("""
    **For Tourism Board Partnerships:**
    
    📧 partnerships@travelapp.co
    📞 +57 (1) 123-4567
    🌐 www.travelapp.co/partnerships
    
    *Contact us to establish data sharing agreements and collaborative tourism development programs.*
    """)

# Raw data section
with st.expander("📊 View Raw Data"):
    tab1, tab2, tab3 = st.tabs(["Regional Data", "Tourism Board Data", "Seasonal Trends"])
    
    with tab1:
        st.dataframe(regional_data, use_container_width=True)
    
    with tab2:
        st.dataframe(tourism_board_data, use_container_width=True)
    
    with tab3:
        st.dataframe(seasonal_data, use_container_width=True)

st.markdown("---")
st.markdown("**Data Source**: Analytics Pipeline | **Last Updated**: Real-time | **Question Owner**: Ignacio Chaparro")