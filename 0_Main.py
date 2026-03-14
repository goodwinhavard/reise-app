import streamlit as st
import json

st.set_page_config(
    page_title="Håvard's Travel App",
    page_icon=":airplane:"
)

st.title("Håvard's Travel App")

filename = "travel_data.json"

if 'travel_entries' not in st.session_state:
    st.session_state.travel_entries = []

if st.sidebar.button("Load from file"):
    st.write("Reading from file: ", filename)

    try:
        with open(filename, "r", encoding="utf-8") as f:
            st.session_state.travel_entries = json.load(f)
        st.sidebar.success(f"Loaded {len(st.session_state.travel_entries)} entries from {filename}")
    except FileNotFoundError:
        st.sidebar.error(f"File {filename} not found.")

if st.sidebar.button("Save to file"):
    st.write("Saving to file: ", filename)

    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump([entry.__dict__ if hasattr(entry, '__dict__') else entry for entry in st.session_state.travel_entries], f, ensure_ascii=False, indent=2)
        st.sidebar.success(f"Saved {len(st.session_state.travel_entries)} entries to {filename}")
    except Exception as e:
        st.sidebar.error(f"Failed to save: {e}")

    