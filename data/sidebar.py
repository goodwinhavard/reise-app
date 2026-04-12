import json
import streamlit as st
from datetime import date
from data.entries import TravelEntry, Location

FILENAME = "travel_data.json"


def entry_to_dict(entry):
    return {
        "name": entry.name,
        "country": entry.country,
        "start_date": entry.start_date.isoformat(),
        "end_date": entry.end_date.isoformat(),
        "text": entry.text,
        "locations": [{"cname": loc.cname, "x_coord": loc.x_coord, "y_coord": loc.y_coord} for loc in entry.locations],
        "photos": entry.photos,
    }


def dict_to_entry(d):
    locations = [Location(loc["cname"], loc["x_coord"], loc["y_coord"]) for loc in d.get("locations", [])]
    return TravelEntry(
        name=d["name"],
        country=d["country"],
        start_date=date.fromisoformat(d["start_date"]),
        end_date=date.fromisoformat(d["end_date"]),
        locations=locations,
        text=d.get("text"),
        photos=d.get("photos", []),
    )


def render_sidebar():
    if "travel_entries" not in st.session_state:
        st.session_state.travel_entries = []
        # Load data automatically if file exists
        try:
            with open(FILENAME, "r", encoding="utf-8") as f:
                st.session_state.travel_entries = [dict_to_entry(d) for d in json.load(f)]
        except FileNotFoundError:
            pass  # File doesn't exist, start with empty list

    if st.sidebar.button("Load from file"):
        try:
            with open(FILENAME, "r", encoding="utf-8") as f:
                st.session_state.travel_entries = [dict_to_entry(d) for d in json.load(f)]
            st.sidebar.success(f"Loaded {len(st.session_state.travel_entries)} entries")
        except FileNotFoundError:
            st.sidebar.error(f"File {FILENAME} not found.")

    if st.sidebar.button("Save to file"):
        try:
            with open(FILENAME, "w", encoding="utf-8") as f:
                json.dump([entry_to_dict(e) for e in st.session_state.travel_entries], f, ensure_ascii=False, indent=2)
            st.sidebar.success(f"Saved {len(st.session_state.travel_entries)} entries")
        except Exception as e:
            st.sidebar.error(f"Failed to save: {e}")
