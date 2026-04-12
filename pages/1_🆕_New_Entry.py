import datetime

import streamlit as st
import pycountry
import os
import re
from data.sidebar import render_sidebar

from data.entries import TravelEntry, Location
from geopy.geocoders import Nominatim

import geonamescache

st.set_page_config(layout="wide")

@st.cache_data
def get_coordinates(city, country):
    geolocator = Nominatim(user_agent="city_mapper")
    location = geolocator.geocode(f"{city}, {country}")
    if location:
        return (location.latitude, location.longitude)
    else:
        return None

@st.cache_data
def load_countries():
    gc = geonamescache.GeonamesCache()
    countries = gc.get_countries()
    country_names = sorted([c['name'] for c in countries.values()])
    return countries, country_names

@st.cache_data
def get_cities_for_country(country_name):
    gc = geonamescache.GeonamesCache()
    countries = gc.get_countries()
    code = next((k for k, v in countries.items() if v['name'] == country_name), None)
    if not code:
        return []
    return sorted([city['name'] for city in gc.get_cities().values() if city['countrycode'] == code])
    
if 'locations_list' not in st.session_state:
    st.session_state.locations_list = []

render_sidebar()
st.title("Add new travel entry")

st.session_state.travel_name = st.text_input("Travel Name")
st.session_state.travel_start_date = st.date_input("Travel Start Date", min_value=datetime.date(year=1984, month=1, day=1))
st.session_state.travel_end_date = st.date_input("Travel End Date", min_value=st.session_state.travel_start_date)
st.session_state.travel_text = st.text_area("Add your personal notes")

countries, country_names = load_countries()
st.session_state.travel_country = st.selectbox("Select a country", country_names)

st.write("Number of locations added:", len(st.session_state.locations_list))

cities = get_cities_for_country(st.session_state.travel_country)


st.divider()

cols = st.columns([1, 1])  # Three columns: left, divider, right
with cols[0]:
    st.write("🌇 Add City")

    country_obj = pycountry.countries.get(name=st.session_state.travel_country)
    country_code = country_obj.alpha_2 if country_obj else None

    city = st.selectbox("Select a city", cities)
    coords = get_coordinates(city, st.session_state.travel_country)

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
            #st.experimental_rerun()

if len(st.session_state.locations_list) > 0:
    if st.button("Clear Locations"):
        st.session_state.locations_list = []
    st.divider()

st.subheader("Photos")
uploaded_photos = st.file_uploader(
    "Add photos for this trip",
    type=["jpg", "jpeg", "png", "webp", "heic"],
    accept_multiple_files=True,
)

if st.button("Add Entry"):

    err_txt = ""
    if st.session_state.travel_name is None or st.session_state.travel_name.strip() == "":
        err_txt = err_txt + "Please provide a travel name.\n"

    if len(st.session_state.locations_list) == 0:
        err_txt = err_txt + "Please add at least one location.\n"

    if err_txt != "":
        st.write("Not all required fields are filled:")
        st.error(err_txt)

    else:
        # Save photos to photos/<sanitized_travel_name>/
        safe_name = re.sub(r"[^\w\-]", "_", st.session_state.travel_name.strip())
        photo_dir = os.path.join("photos", safe_name)
        photo_paths = []

        if uploaded_photos:
            os.makedirs(photo_dir, exist_ok=True)
            for photo in uploaded_photos:
                dest = os.path.join(photo_dir, photo.name)
                with open(dest, "wb") as f:
                    f.write(photo.getbuffer())
                photo_paths.append(dest)

        new_entry = TravelEntry(
            name=st.session_state.travel_name,
            country=st.session_state.travel_country,
            start_date=st.session_state.travel_start_date,
            end_date=st.session_state.travel_end_date,
            locations=st.session_state.locations_list,
            text=st.session_state.travel_text,
            photos=photo_paths,
        )

        st.session_state.travel_entries.append(new_entry)
        st.success(f"Travel entry added successfully! ({len(photo_paths)} photo(s) saved)")

if st.button("Clear All"):
    st.session_state.locations_list = []
    st.session_state.travel_name = ""
    st.session_state.travel_start_date = None
    st.session_state.travel_end_date = None
    st.session_state.travel_text = ""
