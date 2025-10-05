import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


from computation.least_used_features import list_available_months, get_least_used_features

st.set_page_config(page_title="Least-used Features", page_icon="📉", layout="centered")
st.title("Least-used Features (Monthly)")

months = list_available_months()
if not months:
    st.info("No feature-usage data available yet.")
    st.stop()

# default to most recent month
default_idx = 0
selected_month = st.selectbox("Month", months, index=default_idx)

df = get_least_used_features(selected_month)

# optional: show raw table
with st.expander("See raw data"):
    st.dataframe(df, use_container_width=True)

# bar chart: least → most
fig, ax = plt.subplots()
ax.bar(df["feature_key"], df["count"])
ax.set_title(f"Feature usage counts — {selected_month}")
ax.set_xlabel("Feature")
ax.set_ylabel("Monthly accesses")
ax.tick_params(axis='x', rotation=45)

st.pyplot(fig)

# quick insights
total = int(df["count"].sum())
least_row = df.iloc[0] if len(df) else None
if least_row is not None and total > 0:
    share = 100.0 * least_row["count"] / total
    st.caption(
        f"Least used: **{least_row['feature_key']}** with **{least_row['count']}** accesses "
        f"({share:.1f}% of total this month)."
    )
