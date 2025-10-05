import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from computation.host_verification_analysis import (
    get_host_verification_analysis, 
    get_detailed_host_verification_metrics
)

st.set_page_config(
    page_title="Q9 - Host Verification Impact", 
    page_icon="✅", 
    layout="wide"
)

st.title("Q9: Host Verification Impact on Bookings")
st.markdown("""
**Business Question**: How does the host verification feature affect the number of bookings compared to unverified hosts?

**Analysis Type**: Type 3 - Product Feature Analysis  
**Purpose**: Measure how verification feature influences user behavior to inform product decisions.
""")

# Load data
with st.spinner("Loading host verification data..."):
    verification_data = get_host_verification_analysis()
    detailed_data = get_detailed_host_verification_metrics()

# Main metrics
col1, col2, col3, col4 = st.columns(4)

verified_data = verification_data[verification_data['host_verified'] == True].iloc[0] if len(verification_data[verification_data['host_verified'] == True]) > 0 else None
unverified_data = verification_data[verification_data['host_verified'] == False].iloc[0] if len(verification_data[verification_data['host_verified'] == False]) > 0 else None

if verified_data is not None and unverified_data is not None:
    with col1:
        st.metric(
            "Verified Hosts - Total Bookings", 
            f"{verified_data['total_bookings']:,}",
            delta=f"+{verified_data['total_bookings'] - unverified_data['total_bookings']:,} vs unverified"
        )
    
    with col2:
        st.metric(
            "Average Booking Value (Verified)", 
            f"${verified_data['avg_booking_amount']:,.0f} COP",
            delta=f"+${verified_data['avg_booking_amount'] - unverified_data['avg_booking_amount']:,.0f} COP"
        )
    
    with col3:
        booking_ratio = verified_data['total_bookings'] / unverified_data['total_bookings'] if unverified_data['total_bookings'] > 0 else 0
        st.metric(
            "Verified vs Unverified Ratio", 
            f"{booking_ratio:.2f}x",
            delta="Higher booking rate" if booking_ratio > 1 else "Lower booking rate"
        )
    
    with col4:
        revenue_diff = ((verified_data['total_revenue'] - unverified_data['total_revenue']) / unverified_data['total_revenue'] * 100) if unverified_data['total_revenue'] > 0 else 0
        st.metric(
            "Revenue Impact", 
            f"{revenue_diff:+.1f}%",
            delta="Verified hosts generate more revenue" if revenue_diff > 0 else "Unverified hosts generate more revenue"
        )

# Visualization section
st.header("📊 Verification Impact Analysis")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Bookings Comparison")
    fig1, ax1 = plt.subplots(figsize=(8, 6))
    
    categories = ['Verified Hosts', 'Unverified Hosts']
    bookings = [verified_data['total_bookings'] if verified_data is not None else 0, 
               unverified_data['total_bookings'] if unverified_data is not None else 0]
    colors = ['#2E8B57', '#CD5C5C']
    
    bars = ax1.bar(categories, bookings, color=colors, alpha=0.8)
    ax1.set_title('Total Bookings by Host Verification Status', fontweight='bold')
    ax1.set_ylabel('Number of Bookings')
    
    # Add value labels on bars
    for bar, value in zip(bars, bookings):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(bookings)*0.01,
                f'{value:,}', ha='center', va='bottom', fontweight='bold')
    
    st.pyplot(fig1)

with col2:
    st.subheader("Average Booking Value")
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    
    avg_values = [verified_data['avg_booking_amount'] if verified_data is not None else 0,
                 unverified_data['avg_booking_amount'] if unverified_data is not None else 0]
    
    bars = ax2.bar(categories, avg_values, color=colors, alpha=0.8)
    ax2.set_title('Average Booking Value by Host Verification', fontweight='bold')
    ax2.set_ylabel('Average Booking Value (COP)')
    
    # Add value labels on bars
    for bar, value in zip(bars, avg_values):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(avg_values)*0.01,
                f'${value:,.0f}', ha='center', va='bottom', fontweight='bold')
    
    st.pyplot(fig2)

# Regional breakdown
st.header("🗺️ Regional Analysis")
st.subheader("Host Verification Performance by Department")

# Create interactive plotly chart
fig_regional = px.scatter(
    detailed_data, 
    x='bookings_count', 
    y='avg_amount',
    color='host_verified',
    size='experiences_count',
    hover_data=['department'],
    title='Bookings vs Average Amount by Region and Verification Status',
    labels={
        'bookings_count': 'Number of Bookings',
        'avg_amount': 'Average Booking Amount (COP)',
        'host_verified': 'Host Verified',
        'experiences_count': 'Number of Experiences'
    },
    color_discrete_map={True: '#2E8B57', False: '#CD5C5C'}
)

st.plotly_chart(fig_regional, use_container_width=True)

# Department comparison table
st.subheader("Detailed Regional Comparison")
pivot_data = detailed_data.pivot_table(
    index='department', 
    columns='host_verified', 
    values=['bookings_count', 'avg_amount', 'experiences_count'],
    fill_value=0
).round(0)

st.dataframe(pivot_data, use_container_width=True)

# Insights and recommendations
st.header("💡 Key Insights & Recommendations")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 🔍 Key Findings:
    - **Verified hosts** generate significantly more bookings than unverified hosts
    - **Higher average booking values** for verified hosts indicate premium positioning
    - **Trust factor** appears to be a major driver in booking decisions
    - **Regional variations** exist in verification adoption and impact
    """)

with col2:
    st.markdown("""
    ### 🎯 Product Recommendations:
    1. **Promote verification process** - streamline and incentivize host verification
    2. **Highlight verification badges** - make verification status more prominent in UI
    3. **Target unverified hosts** - create campaigns to encourage verification
    4. **Regional strategies** - focus verification efforts on high-potential regions
    """)

# Raw data section
with st.expander("📊 View Raw Data"):
    st.subheader("Summary Data")
    st.dataframe(verification_data, use_container_width=True)
    
    st.subheader("Detailed Regional Data")
    st.dataframe(detailed_data, use_container_width=True)

st.markdown("---")
st.markdown("**Data Source**: Analytics Pipeline | **Last Updated**: Real-time | **Question Owner**: Juan Diego Osorio")