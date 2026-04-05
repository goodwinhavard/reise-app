import streamlit as st
from data.sidebar import render_sidebar

st.set_page_config(
    page_title="Håvard's Travel App",
    page_icon=":airplane:"
)

st.title("Håvard's Travel App")

render_sidebar()
