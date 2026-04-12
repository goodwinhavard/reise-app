import streamlit as st
import os
import re
from data.sidebar import render_sidebar

render_sidebar()
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