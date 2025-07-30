import streamlit as st

st.title("Select entry")
st.caption("This page allows you to see a travel.")

if "travel_entries" in st.session_state and st.session_state.travel_entries:
    entry_names = [entry.get_name() for entry in st.session_state.travel_entries]
    selected_entry = st.selectbox("Select a travel entry", entry_names)
else:
    st.write("No travel entries found.")
