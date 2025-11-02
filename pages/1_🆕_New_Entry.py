import streamlit as st
import pycountry

from data.entries import TravelEntry, Location
from geopy.geocoders import Nominatim

import geonamescache

st.set_page_config(layout="wide")
def get_coordinates(city, country):
    geolocator = Nominatim(user_agent="city_mapper")
    location = geolocator.geocode(f"{city}, {country}")
    if location:
        return (location.latitude, location.longitude)
    else:
        return None
    
if 'locations_list' not in st.session_state:
    st.session_state.locations_list = []

st.session_state.locations_list = []

st.title("Add new travel entry")

travel_name = st.text_input("Travel Name")
travel_date = st.date_input("Travel Start Date")
travel_end_date = st.date_input("Travel End Date")

travel_text = st.text_area("Add your personal notes")


gc = geonamescache.GeonamesCache()
countries = gc.get_countries()
country_names = sorted([c['name'] for c in countries.values()])
travel_country = st.selectbox("Select a country", country_names)

# Get cities
cities = [city['name'] for city in gc.get_cities().values() if city['countrycode'] == [k for k,v in countries.items() if v['name'] == travel_country][0]]
cities = sorted(cities)


st.divider()

cols = st.columns([1, 1])  # Three columns: left, divider, right
with cols[0]:
    st.write("🌇 Add City")

    country_obj = pycountry.countries.get(name=travel_country)
    country_code = country_obj.alpha_2 if country_obj else None

    city = st.selectbox("Select a city", cities)
    coords = get_coordinates(city, travel_country)

    x_coord = st.number_input("X-coordinate", value=float(coords[0]), key="x_input_city", format="%.6f")
    y_coord = st.number_input("Y-coordinate", value=float(coords[1]), key="y_input_city", format="%.6f")

    if st.button("➕ Add City"):
        # text_input returns strings — convert if you need floats
        st.write(city, x_coord, y_coord)
        new_location = Location(city, x_coord, y_coord)
        st.session_state.locations_list.append(new_location)
        st.write("Locations added so far:", len(st.session_state.locations_list))

with cols[1]:
    #st.divider()
    st.write("🏞️ Add Location")
    name = st.text_input("Location Name")
    x_coord = st.number_input("X-coordinate", value=999.0, key="x_input_location", format="%.6f")
    y_coord = st.number_input("Y-coordinate", value=999.0, key="y_input_location", format="%.6f")

    if st.button("➕ Add Location"):
        st.write(name, x_coord, y_coord)
        new_location = Location(name, x_coord, y_coord)
        st.session_state.locations_list.append(new_location)
        st.write("Locations added so far:", len(st.session_state.locations_list))

st.divider()

for loc in st.session_state.locations_list:
    idx = st.session_state.locations_list.index(loc)
    cols = st.columns([9, 1])
    with cols[0]:
        st.write(f"Location Name: {loc.cname}, X: {loc.x_coord}, Y: {loc.y_coord}")
    with cols[1]:
        if st.button("X", key=f"remove_location_{idx}"):
            st.session_state.locations_list.pop(idx)
            st.experimental_rerun()

if len(st.session_state.locations_list) > 0:
    if st.button("Clear Locations"):
        st.session_state.locations_list = []

    st.divider()
if st.button("Add Entry"):

    err_txt = ""
    # Undersøke at alt er lagt ved
    if travel_name is None or travel_name.strip() == "":
        err_txt = err_txt + "Please provide a travel name.\n"



    if err_txt != "":
        st.write("Not all required fields are filled:")
        st.error(err_txt)

    else:
        st.write("Not implemented yet.")
    # if travel_name and travel_country and travel_date and travel_end_date:
    #     entry = TravelEntry(travel_name, travel_country, travel_date, travel_end_date)
    #     if "travel_entries" not in st.session_state:
    #         st.session_state.travel_entries = []
    #     st.session_state.travel_entries.append(entry)
    #     st.success(f"Entry '{travel_name}' added successfully!")
    # else:
    #     st.error("Please fill in all fields before adding an entry.")
