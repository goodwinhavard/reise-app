import streamlit as st
import pycountry

from data.entries import TravelEntry

st.title("Add new entry")

travel_name = st.text_input("Travel Name")
#travel_country = st.text_input("Travel Country")
travel_date = st.date_input("Travel Start Date")
travel_end_date = st.date_input("Travel End Date")


countries = [country.name for country in pycountry.countries]
travel_country = st.selectbox("Select a country", countries)


st.subheader("Add Locations (Sub-Entries)")

# Use session_state to persist sub_locations across reruns
if "sub_locations" not in st.session_state:
    st.session_state.sub_locations = []

with st.form(key="location_form", clear_on_submit=True):
    place = st.text_input("Place", key="place_input")
    x_coord = st.text_input("X-coordinate", value="999", key="x_input")
    y_coord = st.text_input("Y-coordinate", value="999", key="y_input")
    add_location = st.form_submit_button("➕ Add Location")
    if add_location:
        if place:
            st.session_state.sub_locations.append({
                "place": place,
                "x": x_coord,
                "y": y_coord
            })
        else:
            st.warning("Please add a place before submitting.")

if len(st.session_state.sub_locations) > 0:
    st.markdown("**Added Locations:**")
    for idx, loc in enumerate(st.session_state.sub_locations):
        cols = st.columns([6, 1])
        with cols[0]:
            st.write(f"{idx + 1}. {loc['place']} (X: {loc['x']}, Y: {loc['y']})")
        with cols[1]:
            if st.button("Remove", key=f"remove_{idx}"):
                st.session_state.sub_locations.pop(idx)
                break


if st.button("Add Entry"):
    if travel_name and travel_country and travel_date and travel_end_date:
        entry = TravelEntry(travel_name, travel_country, travel_date, travel_end_date)
        if "travel_entries" not in st.session_state:
            st.session_state.travel_entries = []
        st.session_state.travel_entries.append(entry)
        st.success(f"Entry '{travel_name}' added successfully!")
    else:
        st.error("Please fill in all fields before adding an entry.")