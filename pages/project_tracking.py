import streamlit as st
import pandas as pd
from components import project_map
from utils.config import PROJECTS_URL, TECH_CATEGORIES_PROJECT

def render():
    st.title("LDES Project Tracking")
    
    st.markdown("""
    This page displays the LDES Project Tracking Spreadsheet with information about 
    various energy storage projects and their current status.
    """)
    
    try:
        projects_df = pd.read_csv(PROJECTS_URL)
        
        st.sidebar.header("Project Tracking Filters")
        
        if "Technology Type" in projects_df.columns:
            technology_types = projects_df["Technology Type"].unique()
            selected_technology_types = []
            for tech_type in technology_types:
                if st.sidebar.checkbox(f"{tech_type}", value=True, key=f"project_tech_{tech_type}"):
                    selected_technology_types.append(tech_type)
            filtered_projects_df = projects_df[projects_df["Technology Type"].isin(selected_technology_types)]
        else:
            filtered_projects_df = projects_df

        if "Detailed Technology" in projects_df.columns:
            all_selected_project_detailed = []
            
            for tech_type in selected_technology_types:
                if tech_type in TECH_CATEGORIES_PROJECT:
                    st.sidebar.markdown(f"**{tech_type}**")
                    
                    available_techs = [t for t in TECH_CATEGORIES_PROJECT[tech_type] if t in projects_df["Detailed Technology"].unique()]
                    
                    if available_techs:
                        selected_techs = st.sidebar.pills(
                            f"project_{tech_type}_detailed",
                            options=available_techs,
                            default=available_techs,
                            selection_mode="multi",
                            label_visibility="collapsed"
                        )
                        all_selected_project_detailed.extend(selected_techs)
            
            if all_selected_project_detailed:
                filtered_projects_df = filtered_projects_df[
                    filtered_projects_df["Detailed Technology"].isin(all_selected_project_detailed)
                ]
            else:
                filtered_projects_df = filtered_projects_df[
                    filtered_projects_df["Detailed Technology"].isin([])
                ]

        st.subheader("Project Overview")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Projects", len(projects_df))
        with col2:
            st.metric("Filtered Projects", len(filtered_projects_df))

        project_map.render_project_map(filtered_projects_df)    
        
        st.subheader("All Projects")
        st.caption("Double-click on any cell to see its full content")

        project_column_config = {}
        
        st.data_editor(
            filtered_projects_df,
            column_config=project_column_config,
            use_container_width=True,
            height=600,
            disabled=True,
            hide_index=True
        )
        
        st.download_button(
            label="Download Project Data as CSV",
            data=filtered_projects_df.to_csv(index=False).encode('utf-8'),
            file_name='ldes_project_tracking.csv',
            mime='text/csv',
        )

    except Exception as e:
        st.error(f"Error loading the project tracking file: {e}")
        import traceback
        st.code(traceback.format_exc())