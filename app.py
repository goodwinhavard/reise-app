import streamlit as st
from data.sidebar import render_sidebar

st.set_page_config(
    page_title="Goodwins Travel App",
    page_icon=":airplane:"
)

st.title("Goodwins Travel App")

render_sidebar()
