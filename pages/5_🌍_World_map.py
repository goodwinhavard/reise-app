import streamlit as st
import pandas as pd
import pycountry
import plotly.express as px

st.set_page_config(layout="wide")
st.title("World Map")

if "travel_entries" not in st.session_state or not st.session_state.travel_entries:
    st.info("No travel entries found. Add one on the **New Entry** page.")
    st.stop()

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
    trips_summary = "<br>".join(
        f"• {t.get_name()} ({t.get_start_date().year})" for t in trips
    )
    cities = []
    for t in trips:
        cities += [loc.cname for loc in t.get_locations()]

    rows.append({
        "country": country_name,
        "iso_alpha": country_obj.alpha_3,
        "trips": len(trips),
        "years": ", ".join(sorted(set(str(t.get_start_date().year) for t in trips))),
        "cities": ", ".join(sorted(set(cities))),
        "trips_summary": trips_summary,
    })

df = pd.DataFrame(rows)

# --- Choropleth map ---
fig = px.choropleth(
    df,
    locations="iso_alpha",
    color="trips",
    hover_name="country",
    hover_data={
        "iso_alpha": False,
        "trips": True,
        "years": True,
        "cities": True,
    },
    color_continuous_scale=[(0, "#2ecc71"), (1, "#1a6b3a")],
    range_color=(1, max(df["trips"].max(), 2)),
    labels={"trips": "Trips", "years": "Year(s)", "cities": "Cities"},
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
    coloraxis_colorbar=dict(title="Trips"),
)

st.plotly_chart(fig, use_container_width=True)

# --- Summary table below the map ---
st.divider()
st.subheader(f"Visited countries ({len(df)})")
display_df = df[["country", "trips", "years", "cities"]].rename(columns={
    "country": "Country",
    "trips": "Trips",
    "years": "Year(s)",
    "cities": "Cities",
})
st.dataframe(display_df.sort_values("Country"), use_container_width=True, hide_index=True)
