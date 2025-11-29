# presentation/skills_top5_departments.py
import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

from computation.skills_top_departments import (
    get_top_departments,
    get_overall_skill_counts_in_top_departments,
    get_skill_counts_by_department,
)

st.set_page_config(page_title="Most common skills in top departments", page_icon="📊", layout="centered")
st.title("Most common “skills to learn” in the experiences of the top departments")
st.caption("Ranks skills from experiences in the departments with the highest number of active experiences.")

with st.sidebar:
    st.header("Controls")
    n_depts = st.number_input("Top N departments", min_value=1, max_value=20, value=5, step=1)
    k_skills = st.number_input("Show top K skills", min_value=5, max_value=100, value=15, step=5)

# Determine top departments
top_depts = get_top_departments(limit=n_depts)
if not top_depts:
    st.info("No departments found.")
    st.stop()

st.write(f"Top departments by active experiences: {', '.join(top_depts)}")

# Overall skill counts across those departments
overall_df = get_overall_skill_counts_in_top_departments(limit_depts=n_depts)
if overall_df.empty:
    st.warning("No skills found for the selected departments.")
    st.stop()

overall_top = overall_df.head(k_skills)

# Overall bar chart
fig = plt.figure()
plt.bar(overall_top["skill"], overall_top["total_count"])
plt.title("Most common skills across the selected top departments")
plt.xlabel("Skill")
plt.ylabel("Count")
plt.xticks(rotation=45, ha="right")
st.pyplot(fig)

with st.expander("See overall data"):
    st.dataframe(overall_df, use_container_width=True)

# Per-department bar charts
per_dept_df = get_skill_counts_by_department(limit_depts=n_depts)
st.subheader("Per-department breakdown")

if per_dept_df.empty:
    st.info("No per-department skill data available.")
else:
    # Ensure only selected top_depts are shown and in the same order
    per_dept_df = per_dept_df[per_dept_df["department"].isin(top_depts)]

    for dept in top_depts:
        ddf = per_dept_df[per_dept_df["department"] == dept]
        if ddf.empty:
            continue

        ddf_sorted = ddf.sort_values(["count", "skill"], ascending=[False, True]).head(k_skills)

        st.markdown(f"**{dept}**")
        fig = plt.figure()
        plt.bar(ddf_sorted["skill"], ddf_sorted["count"])
        plt.title(f"Top skills in {dept}")
        plt.xlabel("Skill")
        plt.ylabel("Count")
        plt.xticks(rotation=45, ha="right")
        st.pyplot(fig)