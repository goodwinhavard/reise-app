import streamlit as st
import json
from datetime import date
from data.entries import TravelEntry, Location

st.set_page_config(
    page_title="Håvard's Travel App",
    page_icon=":airplane:"
)

st.title("Håvard's Travel App")

filename = "travel_data.json"

if 'travel_entries' not in st.session_state:
    st.session_state.travel_entries = []

def entry_to_dict(entry):
    return {
        "name": entry.name,
        "country": entry.country,
        "start_date": entry.start_date.isoformat(),
        "end_date": entry.end_date.isoformat(),
        "text": entry.text,
        "locations": [{"cname": loc.cname, "x_coord": loc.x_coord, "y_coord": loc.y_coord} for loc in entry.locations],
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
    )

if st.sidebar.button("Load from file"):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            st.session_state.travel_entries = [dict_to_entry(d) for d in json.load(f)]
        st.sidebar.success(f"Loaded {len(st.session_state.travel_entries)} entries from {filename}")
    except FileNotFoundError:
        st.sidebar.error(f"File {filename} not found.")

if st.sidebar.button("Save to file"):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump([entry_to_dict(e) for e in st.session_state.travel_entries], f, ensure_ascii=False, indent=2)
        st.sidebar.success(f"Saved {len(st.session_state.travel_entries)} entries to {filename}")
    except Exception as e:
        st.sidebar.error(f"Failed to save: {e}")

    