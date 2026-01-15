import streamlit as st
from utils.config import LOGO_URL

def render_header():
    st.markdown(
        f"""
        <div style="text-align: center;">
            <img src="{LOGO_URL}" width="653" height="115">
        </div>
        """, 
        unsafe_allow_html=True
    )
    st.divider()