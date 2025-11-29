import sys
import os

# Add the project root directory to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
import plotly.express as px
from ingestion_integration.lib.pg import get_conn

def load_data():
    query = """
    SELECT last_chat_started_at, total_chats_started
    FROM fact_messaging_global_usage
    LIMIT 1;
    """
    with get_conn() as conn:
        return pd.read_sql(query, conn)

def main():
    st.title("Messaging Global Usage")
    st.write("Tracking global chat initiation metrics.")

    try:
        df = load_data()
        if df.empty:
            st.warning("No data available yet. Please run the ingestion pipeline.")
        else:
            row = df.iloc[0]
            total_chats = row["total_chats_started"]
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Total Chats Started", value=total_chats)
            with col2:
                st.metric(label="Last Chat Started At", value=row["last_chat_started_at"])

            # Create data for the bar chart
            # Currently only "Messaging" feature is tracked here, but structure allows more.
            features_data = pd.DataFrame({
                "Feature": ["Messaging"],
                "Usage Count": [total_chats]
            })
            
            st.subheader("Usage of App Features")
            fig = px.bar(
                features_data, 
                x="Feature", 
                y="Usage Count", 
                title="Feature Usage Overview",
                text="Usage Count"
            )
            st.plotly_chart(fig)
                
    except Exception as e:
        st.error(f"Error loading data: {e}")

if __name__ == "__main__":
    main()
