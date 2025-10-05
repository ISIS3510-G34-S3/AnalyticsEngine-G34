import streamlit as st

st.set_page_config(page_title="Analytics Dashboard", page_icon="📊", layout="wide")
st.title("Travel App Analytics Dashboard")

st.markdown("""
Welcome to the comprehensive Analytics Dashboard for our Travel App Analytics Pipeline.

This dashboard provides insights across different types of business analytics to support product decisions, 
strategic partnerships, and external stakeholder engagement.
""")

# Create dashboard sections
col1, col2 = st.columns(2)

with col1:
    st.header("🔍 Product Analytics")
    st.markdown("""
    **Type 3 Analytics - Product Feature Analysis**
    
    These dashboards help inform product and design decisions by measuring how specific features influence user behavior.
    """)
    
    with st.container():
        st.subheader("Q7: Feature Usage Analysis")
        st.markdown("**Monthly feature usage analysis to identify least-used features**")
        if st.button("📉 View Least-Used Features Dashboard"):
            st.markdown("**Command to run:**")
            st.code("streamlit run presentation/feature_usage_least_often.py")
    
    with st.container():
        st.subheader("Q9: Host Verification Impact")
        st.markdown("**How host verification affects booking behavior compared to unverified hosts**")
        st.markdown("*Owner: Juan Diego Osorio*")
        if st.button("✅ View Host Verification Analysis"):
            st.markdown("**Command to run:**")
            st.code("streamlit run presentation/q9_host_verification_impact.py")

with col2:
    st.header("🌎 Strategic Analytics")
    st.markdown("""
    **Type 4 Analytics - External Data Sharing**
    
    These dashboards analyze aggregated data for sharing with external stakeholders to support strategic partnerships and public policy.
    """)
    
    with st.container():
        st.subheader("Q11: Authentic Experience Regions")
        st.markdown("**Regional concentration of authentic experiences for tourism board partnerships**")
        st.markdown("*Owner: Ignacio Chaparro*")
        if st.button("🏛️ View Tourism Board Analysis"):
            st.markdown("**Command to run:**")
            st.code("streamlit run presentation/q11_authentic_experiences_regions.py")
    
    with st.container():
        st.subheader("Q12: Regional Offers for Public Entities")
        st.markdown("**Experience offer concentrations and characteristics for public entity partnerships**")
        st.markdown("*Owner: Santiago Arenas*")
        if st.button("🌎 View Public Entity Analysis"):
            st.markdown("**Command to run:**")
            st.code("streamlit run presentation/q12_regional_offers_public_entities.py")

st.markdown("---")

st.header("🚀 Quick Start Guide")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 📋 Prerequisites
    1. **PostgreSQL Database** running with analytics schema
    2. **Python Environment** with required packages
    3. **Firebase Credentials** in `Llaves/analytics-ingestion.json`
    4. **Environment Variables** configured in `.env` file
    """)

with col2:
    st.markdown("""
    ### 🔧 Setup Commands
    ```bash
    # Activate virtual environment
    .venv/Scripts/Activate.ps1
    
    # Run data ingestion
    python ingestion_integration/run_all.py
    
    # Launch specific dashboard
    streamlit run presentation/[dashboard].py
    ```
    """)

with col3:
    st.markdown("""
    ### 📊 Available Dashboards
    - **Feature Usage** (Q7) - Product optimization
    - **Host Verification** (Q9) - Feature impact analysis  
    - **Regional Authentic** (Q11) - Tourism board data
    - **Regional Offers** (Q12) - Public entity insights
    """)

st.header("📈 Business Question Overview")

# Create a table with all business questions
questions_data = {
    "Question": ["Q7", "Q9", "Q11", "Q12"],
    "Title": [
        "Feature Usage Analysis", 
        "Host Verification Impact",
        "Authentic Experience Regions",
        "Regional Offers Analysis"
    ],
    "Type": ["Type 3", "Type 3", "Type 4", "Type 4"],
    "Purpose": [
        "Identify least-used features for product optimization",
        "Measure verification feature impact on booking behavior", 
        "Share regional data with tourism boards for partnerships",
        "Provide aggregated data to public entities for policy development"
    ],
    "Owner": [
        "Analytics Team",
        "Juan Diego Osorio", 
        "Ignacio Chaparro",
        "Santiago Arenas"
    ],
    "Dashboard": [
        "feature_usage_least_often.py",
        "q9_host_verification_impact.py",
        "q11_authentic_experiences_regions.py", 
        "q12_regional_offers_public_entities.py"
    ]
}

st.dataframe(questions_data, use_container_width=True)

st.markdown("---")

st.markdown("""
### 🔗 Additional Resources

- **Project Repository**: AnalyticsEngine-G34
- **Current Branch**: implement/bq9-11-12  
- **Data Pipeline**: Ingestion → Integration → Computation → Presentation
- **Technology Stack**: Python, PostgreSQL, Firebase, Streamlit, Plotly

For technical support or questions about the analytics pipeline, please refer to the project documentation or contact the development team.
""")

# Add system status indicators
st.header("🔧 System Status")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Database", "🟡 Mock Mode", delta="Using sample data")

with col2:
    st.metric("Firebase", "🟡 Mock Mode", delta="Credentials needed")

with col3:
    st.metric("Dashboards", "🟢 Active", delta="4 available")

with col4:
    st.metric("Data Pipeline", "🔄 Ready", delta="Awaiting real data")
