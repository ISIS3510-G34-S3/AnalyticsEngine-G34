# presentation/device_distribution_monthly.py
import os, sys
# Safe import when not using venv / PYTHONPATH
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

from computation.device_distribution import list_available_months, get_device_distribution

st.set_page_config(page_title="Device installation distribution", page_icon="📱", layout="centered")
st.title("Device installation distribution by month")
st.caption("Select a year-month to see the device distribution (where the app is installed) at that time.")

months = list_available_months()
if not months:
    st.info("No device distribution data available yet.")
    st.stop()

selected_month = st.selectbox("Month (YYYY-MM)", months, index=0)
df = get_device_distribution(selected_month)

with st.expander("See raw data"):
    st.dataframe(df, use_container_width=True)

if df.empty:
    st.warning("No rows for the selected month.")
else:
    # Bar chart (devices by count)
    fig, ax = plt.subplots()
    ax.bar(df["device"], df["count"])
    ax.set_title(f"Device installations — {selected_month}")
    ax.set_xlabel("Device")
    ax.set_ylabel("Install count")
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

    # Optional: a small table with shares
    st.caption("Shares by device (% of month total)")
    st.dataframe(df[["device", "share"]].round(1), use_container_width=True)
