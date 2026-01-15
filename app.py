import streamlit as st
from components.header import render_header
from pages import documentation, visualization, project_tracking

st.set_page_config(layout="wide", page_title="LDES Energy Storage")

render_header()

st.sidebar.header("Navigation")
page_options = ["Documentation", "Visualization", "Project Tracking"]
st.session_state.page = st.sidebar.selectbox(
    "Select Page",
    options=page_options,
    index=page_options.index(st.session_state.get('page', 'Documentation'))
)

st.sidebar.divider()

if st.session_state.page == "Documentation":
    documentation.render()
elif st.session_state.page == "Visualization":
    visualization.render()
elif st.session_state.page == "Project Tracking":
    project_tracking.render()