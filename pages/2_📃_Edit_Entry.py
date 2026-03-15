import streamlit as st

st.title("Edit entry")

st.write("There are ", len(st.session_state.travel_entries), " travel entries stored.")

travel_names = [entry.get_name() for entry in st.session_state.travel_entries]

if len(travel_names) >0:


    seleted_entry = st.selectbox("Select a travel entry to edit", travel_names)

    entry = next((e for e in st.session_state.travel_entries if e.get_name() == seleted_entry), None)

    st.write(f"Editing travel entry: **{entry.get_name()}**")
    
    new_name = st.text_input("Travel Name", value=entry.name)
    new_start_date = st.date_input("Travel Start Date", value=entry.start_date)
    new_end_date = st.date_input("Travel End Date", value=entry.end_date)
    new_text = st.text_area("Personal Notes", value=entry.text)

    # Edit locations list (select one to edit or remove)
    locations = entry.locations if hasattr(entry, "locations") else []

    st.write("Number of locations:", len(locations))

    if len(locations) > 0:
        # find entry index to create unique keys
        entry_index = next(i for i, e in enumerate(st.session_state.travel_entries) if e is entry)

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
                st.experimental_rerun()
        with c2:
            if st.button("Remove Location", key=f"remove_loc_{entry_index}_{sel_idx}"):
                entry.locations.pop(sel_idx)
                st.success("Location removed.")
                st.experimental_rerun()
    else:
        st.write("No locations to edit.")
    
    if st.button("Save Changes"):
        entry.name = new_name
        entry.start_date = new_start_date
        entry.end_date = new_end_date
        entry.text = new_text
        
        st.success("Travel entry updated successfully!")

else:
    st.write("No travel entry selected for editing.")