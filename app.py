import streamlit as st
import pandas as pd
import pycountry
import plotly.express as px
from data.sidebar import render_sidebar

st.set_page_config(
    page_title="Goodwins Travel App",
    page_icon=":airplane:"
)

st.title("Goodwins Travel App")

render_sidebar()

# Display summary of loaded data
if "travel_entries" in st.session_state and st.session_state.travel_entries:
    num_entries = len(st.session_state.travel_entries)
    total_locations = sum(len(entry.get_locations()) for entry in st.session_state.travel_entries)
    total_photos = sum(len(entry.get_photos()) for entry in st.session_state.travel_entries)
    st.write(f"**Loaded Data:** {num_entries} travel entries, {total_locations} locations, {total_photos} photos")

    # --- Build per-country summary ---
    country_data = {}
    for entry in st.session_state.travel_entries:
        country_name = entry.get_country()
        if country_name not in country_data:
            country_data[country_name] = {
                "trips": [],
            }
        country_data[country_name]["trips"].append(entry)

    rows = []
    for country_name, data in country_data.items():
        # Resolve ISO alpha-3 code (required by Plotly choropleth)
        country_obj = pycountry.countries.get(name=country_name)
        if country_obj is None:
            # Fuzzy fallback
            results = pycountry.countries.search_fuzzy(country_name)
            country_obj = results[0] if results else None

        if country_obj is None:
            continue  # skip countries we can't resolve

        trips = data["trips"]

        rows.append({
            "country": country_name,
            "iso_alpha": country_obj.alpha_3,
            "trips": len(trips),
        })

    if rows:
        df = pd.DataFrame(rows)

        # --- Choropleth map ---
        fig = px.choropleth(
            df,
            locations="iso_alpha",
            color="trips",
            hover_name="country",
            color_continuous_scale=[(0, "#2ecc71"), (1, "#1a6b3a")],
            range_color=(1, max(df["trips"].max(), 2)),
        )

        fig.update_layout(
            geo=dict(
                showframe=False,
                showcoastlines=True,
                projection_type="natural earth",
                landcolor="#d3d3d3",
                showland=True,
                showcountries=True,
                countrycolor="#ffffff",
                bgcolor="rgba(0,0,0,0)",
            ),
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            paper_bgcolor="rgba(0,0,0,0)",
            coloraxis_showscale=False,  # Hide colorbar for cleaner look
            dragmode=False,  # Disable dragging
        )

        st.subheader("Visited Countries")
        st.plotly_chart(
            fig,
            use_container_width=True,
            config={
                'displayModeBar': False,
                'modeBarButtonsToRemove': ['pan2d', 'select2d', 'lasso2d', 'zoom2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d'],
                'scrollZoom': False
            }
        )
else:
    st.write("No travel data loaded.")
