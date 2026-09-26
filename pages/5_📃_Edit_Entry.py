import datetime

import os
import re

import pycountry
import streamlit as st
from geopy.geocoders import Nominatim
import geonamescache

from data.entries import TravelEntry, Location
from data.sidebar import render_sidebar


@st.cache_data
def get_coordinates(city, country):
    geolocator = Nominatim(user_agent="city_mapper")
    location = geolocator.geocode(f"{city}, {country}")
    if location:
        return (location.latitude, location.longitude)
    return None


@st.cache_data
def load_countries():
    gc = geonamescache.GeonamesCache()
    countries = gc.get_countries()
    country_names = sorted([c["name"] for c in countries.values()])
    return countries, country_names


@st.cache_data
def get_cities_for_country(country_name):
    gc = geonamescache.GeonamesCache()
    countries = gc.get_countries()
    code = next((k for k, v in countries.items() if v["name"] == country_name), None)
    if not code:
        return []
    return sorted([city["name"] for city in gc.get_cities().values() if city["countrycode"] == code])


render_sidebar()
st.title("Edit entry")

st.write("There are ", len(st.session_state.travel_entries), " travel entries stored.")

travel_names = [entry.get_name() for entry in st.session_state.travel_entries]

if len(travel_names) >0:


    seleted_entry = st.selectbox("Select a travel entry to edit", travel_names)

    entry = next((e for e in st.session_state.travel_entries if e.get_name() == seleted_entry), None)

    # find entry index to create unique keys
    entry_index = next(i for i, e in enumerate(st.session_state.travel_entries) if e is entry)

    st.write(f"Editing travel entry: **{entry.get_name()}**")

    new_name = st.text_input("Travel Name", value=entry.name)
    new_start_date = st.date_input("Travel Start Date", value=entry.start_date)

    end_date_mode = st.radio(
        "Set end date by", ["Calendar", "Number of days"], horizontal=True, key=f"end_mode_{entry_index}"
    )
    if end_date_mode == "Number of days":
        default_days = max((entry.end_date - entry.start_date).days, 1)
        num_days = st.number_input(
            "Trip length (days)", min_value=1, value=default_days, step=1, key=f"end_days_{entry_index}"
        )
        new_end_date = new_start_date + datetime.timedelta(days=int(num_days))
        st.caption(f"Travel End Date: {new_end_date}")
    else:
        new_end_date = st.date_input(
            "Travel End Date", value=entry.end_date, min_value=new_start_date, key=f"end_date_{entry_index}"
        )

    new_text = st.text_area("Personal Notes", value=entry.text)

    st.subheader("Add a new location")
    countries, country_names = load_countries()
    new_location_country = st.selectbox(
        "Select a country for the new location",
        country_names,
        key=f"new_loc_country_{entry_index}",
    )
    available_cities = get_cities_for_country(new_location_country)

    if available_cities:
        new_location_city = st.selectbox(
            "Select a city",
            available_cities,
            key=f"new_loc_city_{entry_index}",
        )
        city_coords = get_coordinates(new_location_city, new_location_country)
    else:
        new_location_city = ""
        city_coords = None

    cols = st.columns([1, 1])
    with cols[0]:
        st.write("🌇 Add City")
        if city_coords:
            city_x = st.number_input(
                "X-coordinate",
                value=float(city_coords[0]),
                key=f"new_loc_city_x_{entry_index}",
                format="%.6f",
            )
            city_y = st.number_input(
                "Y-coordinate",
                value=float(city_coords[1]),
                key=f"new_loc_city_y_{entry_index}",
                format="%.6f",
            )
        else:
            city_x = st.number_input("X-coordinate", value=0.0, key=f"new_loc_city_x_{entry_index}", format="%.6f")
            city_y = st.number_input("Y-coordinate", value=0.0, key=f"new_loc_city_y_{entry_index}", format="%.6f")

        if st.button("➕ Add City", key=f"add_city_{entry_index}"):
            if new_location_city:
                entry.add_location(Location(new_location_city, city_x, city_y))
                st.success("Location added.")
                st.rerun()
            else:
                st.warning("Please select a city first.")

    with cols[1]:
        st.write("🏞️ Add Custom Location")
        custom_name = st.text_input("Location Name", key=f"custom_loc_name_{entry_index}")
        custom_x = st.number_input("X-coordinate", value=999.0, key=f"custom_loc_x_{entry_index}", format="%.6f")
        custom_y = st.number_input("Y-coordinate", value=999.0, key=f"custom_loc_y_{entry_index}", format="%.6f")

        if st.button("➕ Add Location", key=f"add_custom_loc_{entry_index}"):
            if custom_name.strip():
                entry.add_location(Location(custom_name.strip(), custom_x, custom_y))
                st.success("Custom location added.")
                st.rerun()
            else:
                st.warning("Please enter a location name.")

    st.divider()

    # Edit locations list (select one to edit or remove)
    locations = entry.locations if hasattr(entry, "locations") else []

    st.write("Number of locations:", len(locations))

    if len(locations) > 0:
        display_items = [f"{i+1}: {loc.cname} ({loc.x_coord}, {loc.y_coord})" for i, loc in enumerate(locations)]
        selected_display = st.selectbox("Select a location to edit/remove", display_items, key=f"sel_loc_{entry_index}")
        sel_idx = display_items.index(selected_display)
        sel_loc = locations[sel_idx]

        new_loc_name = st.text_input("Location Name", value=sel_loc.cname, key=f"loc_name_{entry_index}_{sel_idx}")
        new_loc_x = st.number_input("X-coordinate", value=float(sel_loc.x_coord), key=f"loc_x_{entry_index}_{sel_idx}", format="%.6f")
        new_loc_y = st.number_input("Y-coordinate", value=float(sel_loc.y_coord), key=f"loc_y_{entry_index}_{sel_idx}", format="%.6f")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("Update Location", key=f"update_loc_{entry_index}_{sel_idx}"):
                sel_loc.cname = new_loc_name
                sel_loc.x_coord = new_loc_x
                sel_loc.y_coord = new_loc_y
                st.success("Location updated.")
                st.rerun()
        with c2:
            if st.button("Remove Location", key=f"remove_loc_{entry_index}_{sel_idx}"):
                entry.locations.pop(sel_idx)
                st.success("Location removed.")
                st.rerun()
    else:
        st.write("No locations to edit.")
    
    # Photos
    st.divider()
    st.subheader("Photos")

    existing_photos = entry.get_photos() if hasattr(entry, "photos") else []
    existing_photos = [p for p in existing_photos if os.path.exists(p)]

    if existing_photos:
        st.write(f"{len(existing_photos)} photo(s) saved")
        cols = st.columns(3)
        for i, path in enumerate(existing_photos):
            with cols[i % 3]:
                st.image(path, use_container_width=True)
                if st.button("Remove", key=f"rm_photo_{i}"):
                    entry.photos.remove(path)
                    os.remove(path)
                    st.rerun()
    else:
        st.write("No photos yet.")

    new_photos = st.file_uploader(
        "Add more photos",
        type=["jpg", "jpeg", "png", "webp", "heic"],
        accept_multiple_files=True,
        key=f"photo_upload_{entry_index}",
    )

    if st.button("Save Changes"):
        entry.name = new_name
        entry.start_date = new_start_date
        entry.end_date = new_end_date
        entry.text = new_text

        if new_photos:
            safe_name = re.sub(r"[^\w\-]", "_", new_name.strip())
            photo_dir = os.path.join("photos", safe_name)
            os.makedirs(photo_dir, exist_ok=True)
            for photo in new_photos:
                dest = os.path.join(photo_dir, photo.name)
                with open(dest, "wb") as f:
                    f.write(photo.getbuffer())
                if dest not in entry.photos:
                    entry.photos.append(dest)

        st.success("Travel entry updated successfully!")

    # Delete button
    if st.button("Delete Travel Entry", type="secondary"):
        st.session_state.travel_entries.remove(entry)
        st.success("Travel entry deleted successfully!")
        st.rerun()