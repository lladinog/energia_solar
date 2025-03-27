import streamlit as st

# Config default settings of the page
st.set_page_config(
    page_title=None,
    page_icon=None,
    layout='centered',
    initial_sidebar_state='auto',
    menu_items={
        'Help': None,
        'Report a bug': None,
        'About': None
    }
)


st.title("Hello World")
