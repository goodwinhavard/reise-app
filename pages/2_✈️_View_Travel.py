import streamlit as st
import os
from data.sidebar import render_sidebar

render_sidebar()
st.title("View Travel")

if "travel_entries" not in st.session_state or not st.session_state.travel_entries:
    st.info("No travel entries found. Add one on the **New Entry** page.")
    st.stop()

entry_names = [entry.get_name() for entry in st.session_state.travel_entries]
selected_name = st.selectbox("Select a travel entry", entry_names)
entry = next((e for e in st.session_state.travel_entries if e.get_name() == selected_name), None)

if entry is None:
    st.stop()

st.divider()
st.header(entry.get_name())

col1, col2 = st.columns(2)
with col1:
    st.metric("Country", entry.get_country())
with col2:
    duration = (entry.get_end_date() - entry.get_start_date()).days
    st.metric("Duration", f"{duration} days")

col3, col4 = st.columns(2)
with col3:
    st.write("**Start Date**")
    st.write(entry.get_start_date())
with col4:
    st.write("**End Date**")
    st.write(entry.get_end_date())

if entry.get_text():
    st.divider()
    st.subheader("Personal Notes")
    st.write(entry.get_text())

locations = entry.get_locations() if hasattr(entry, "locations") else []
if locations:
    st.divider()
    st.subheader(f"Locations ({len(locations)})")
    for i, loc in enumerate(locations):
        st.write(f"**{i + 1}. {loc.cname}** — Lat: {loc.x_coord}, Lon: {loc.y_coord}")
else:
    st.write("No locations registered.")

photos = entry.get_photos() if hasattr(entry, "photos") else []

# Check if running locally (files exist) or on web server
if photos and os.path.exists(photos[0]):
    # Use local paths
    photo_paths = photos
else:
    # Use GitHub raw URLs for web hosting
    base_url = "https://raw.githubusercontent.com/goodwinhavard/reise-app/main/"
    photo_paths = [base_url + p.replace("\\", "/") for p in photos]

if photo_paths:
    st.divider()
    st.subheader(f"Photos ({len(photo_paths)})")
    cols = st.columns(3)
    for i, path in enumerate(photo_paths):
        with cols[i % 3]:
            st.image(path, use_container_width=True)
