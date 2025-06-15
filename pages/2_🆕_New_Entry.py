import streamlit as st
import pycountry

st.title("Add new entry")

travel_name = st.text_input("Travel Name")
travel_country = st.text_input("Travel Country")
travel_date = st.date_input("Travel Start Date")
travel_end_date = st.date_input("Travel End Date")


countries = [country.name for country in pycountry.countries]
selected_country = st.selectbox("Select a country", countries)

