import streamlit as st
import pandas as pd
from data.sidebar import render_sidebar

render_sidebar()
st.title("Travel Overview")

if "travel_entries" not in st.session_state or not st.session_state.travel_entries:
    st.info("No travel entries found. Add one on the **New Entry** page.")
    st.stop()

entries = st.session_state.travel_entries

rows = []
for entry in entries:
    duration = (entry.get_end_date() - entry.get_start_date()).days
    rows.append({
        "Travel": entry.get_name(),
        "Country": entry.get_country(),
        "Year": entry.get_start_date().year,
        "Start": entry.get_start_date(),
        "End": entry.get_end_date(),
        "Days": duration,
        "Locations": len(entry.get_locations()),
    })

df = pd.DataFrame(rows)

# Summary metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Trips", len(entries))
col2.metric("Countries Visited", df["Country"].nunique())
col3.metric("Total Days Travelled", df["Days"].sum())
col4.metric("Total Locations", df["Locations"].sum())

st.divider()

# Full table
st.subheader("All Trips")
st.dataframe(df, use_container_width=True, hide_index=True)

st.divider()

# Trips per country
st.subheader("Trips per Country")
country_counts = df.groupby("Country").agg(Trips=("Travel", "count"), Days=("Days", "sum")).reset_index().sort_values("Trips", ascending=False)
st.dataframe(country_counts, use_container_width=True, hide_index=True)

st.divider()

# Trips per year
st.subheader("Trips per Year")
year_counts = df.groupby("Year").agg(Trips=("Travel", "count"), Days=("Days", "sum")).reset_index().sort_values("Year", ascending=False)
st.dataframe(year_counts, use_container_width=True, hide_index=True)
