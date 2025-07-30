import streamlit as st
import pycountry

from data.entries import TravelEntry
from geopy.geocoders import Nominatim

import geonamescache

def get_coordinates(city, country):
    geolocator = Nominatim(user_agent="city_mapper")
    location = geolocator.geocode(f"{city}, {country}")
    if location:
        return (location.latitude, location.longitude)
    else:
        return None
    

st.title("Add new entry")

travel_name = st.text_input("Travel Name")
#travel_country = st.text_input("Travel Country")
travel_date = st.date_input("Travel Start Date")
travel_end_date = st.date_input("Travel End Date")


#countries = [country.name for country in pycountry.countries]
#travel_country = st.selectbox("Select a country", countries)

gc = geonamescache.GeonamesCache()
countries = gc.get_countries()
country_names = sorted([c['name'] for c in countries.values()])
travel_country = st.selectbox("Select a country", country_names)

# Get cities
cities = [city['name'] for city in gc.get_cities().values() if city['countrycode'] == [k for k,v in countries.items() if v['name'] == travel_country][0]]
cities = sorted(cities)


st.subheader("Add Locations (Sub-Entries)")

# Use session_state to persist sub_locations across reruns
if "sub_locations" not in st.session_state:
    st.session_state.sub_locations = []

with st.form(key="location_form", clear_on_submit=True):
    # Fetch cities for the selected country using the 'cities' package

    # Get country code from country name
    country_obj = pycountry.countries.get(name=travel_country)
    country_code = country_obj.alpha_2 if country_obj else None

    # Get list of cities for the selected country
    #city_list = []
    # if country_code:
    #     city_list = [city.name for city in Cities.get_cities(country_code=country_code)]
    # city = st.selectbox("City", city_list, key="city_input") if city_list else st.text_input("City", key="city_input")
    city = st.selectbox("Select a city", cities)
    #city = st.text_input("City", value=selected_city, key="city_input")


    fill_coords = st.form_submit_button("📍 Find Coordinates")
    if fill_coords:
        coords = get_coordinates(city, travel_country)
        if coords:
            #st.session_state["x_input"] = str(coords[0])
            #st.session_state["y_input"] = str(coords[1])
            st.write(f"Coordinates for {city}, {travel_country}: X: {coords[0]}, Y: {coords[1]}")
            #st.experimental_rerun()
            x_coord = st.text_input("X-coordinate", value=coords[0], key="x_input")
            y_coord = st.text_input("Y-coordinate", value=coords[1], key="y_input")

        else:
            st.warning("Could not find coordinates for this city.")
            x_coord = st.text_input("X-coordinate", value="999", key="x_input")
            y_coord = st.text_input("Y-coordinate", value="999", key="y_input")

    add_location = st.form_submit_button("➕ Add Location")
    if add_location:
        if city:
            st.session_state.sub_locations.append({
                "city": city,
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
