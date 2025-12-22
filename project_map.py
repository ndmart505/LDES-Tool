import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def prepare_map_data(df):
    """
    Aggregate project data by state and convert to state codes.
    """
    state_abbrev = {
        'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
        'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA',
        'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA',
        'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
        'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS', 'Missouri': 'MO',
        'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ',
        'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH',
        'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
        'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT',
        'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'
    }

    # Clean data
    df_clean = df[df['State'].notna()].copy()
    df_clean = df_clean[df_clean['State'] != 'NA']

    # Count projects per state
    state_counts = df_clean.groupby('State').size().reset_index(name='project_count')

    # Cap project counts at 10 for color scaling
    state_counts['project_count_capped'] = state_counts['project_count'].clip(upper=10)

    # Map state abbreviations
    state_counts['state_code'] = state_counts['State'].map(state_abbrev)
    state_counts = state_counts[state_counts['state_code'].notna()]

    return state_counts, df_clean


def create_choropleth_map(state_counts):
    """
    Generate US choropleth map with capped 1–10+ color scale.
    """
    custom_blue_scale = [
        [0.0, '#6baed6'],
        [0.25, '#4292c6'],
        [0.5, '#2171b5'],
        [0.75, '#08519c'],
        [1.0, '#08306b']
    ]

    fig = go.Figure(data=go.Choropleth(
        locations=state_counts['state_code'],
        z=state_counts['project_count_capped'],
        zmin=1,
        zmax=10,
        locationmode='USA-states',
        colorscale=custom_blue_scale,
        customdata=state_counts[['State', 'project_count']],
        colorbar=dict(
            title=dict(
                text="Number of Projects<br>",
                font=dict(color='white')
            ),
            tickmode='array',
            tickvals=list(range(1, 11)),
            ticktext=[str(i) for i in range(1, 10)] + ["10+"],
            tickfont=dict(color='white'),
            bgcolor='rgba(0,0,0,0.5)'
        ),
        hovertemplate=(
            '<b>%{customdata[0]}</b><br>'
            'Projects: %{customdata[1]}<br>'
            '<i>Click to view projects</i><extra></extra>'
        ),
        marker_line_color='white',
        marker_line_width=1.5
    ))

    fig.update_layout(
        title=dict(
            text='LDES Projects by State',
            font=dict(color='white', size=20)
        ),
        geo=dict(
            scope='usa',
            bgcolor='rgba(0,0,0,0)',
            lakecolor='rgb(17,17,17)',
            landcolor='rgb(17,17,17)',
            coastlinecolor='white',
            coastlinewidth=1.5,
            showlakes=True,
            projection_type='albers usa',
            showland=True,
            showcountries=False,
            subunitcolor='white',
            subunitwidth=1.5,
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        margin=dict(l=0, r=0, t=60, b=0),
        height=550
    )

    return fig


def display_project_detail(project_row):
    """
    Display detailed information for a selected project in the side panel.
    """
    st.markdown("### Project Details")
    
    # Project Name
    project_name = project_row.get('Project name', 'Unnamed Project')
    if pd.isna(project_name) or str(project_name).strip() == '':
        project_name = "Unnamed Project"
    st.markdown(f"**{project_name}**")
    
    st.divider()
    
    # Location
    st.markdown("**Location**")
    state = project_row.get('State', 'N/A')
    st.write(f"State: {state if not pd.isna(state) else 'N/A'}")
    
    st.divider()
    
    # Technology
    st.markdown("**Technology**")
    tech_type = project_row.get('Technology Type', 'N/A')
    detailed_tech = project_row.get('Detailed Technology', 'N/A')
    st.write(f"Type: {tech_type if not pd.isna(tech_type) else 'N/A'}")
    st.write(f"Details: {detailed_tech if not pd.isna(detailed_tech) else 'N/A'}")
    
    st.divider()
    
    # Specifications
    st.markdown("**Specifications**")
    power = project_row.get('Power [MW]', None)
    energy = project_row.get('Energy  [MWh]', None)
    duration = project_row.get('Duration [h]', None)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Power", f"{power} MW" if not pd.isna(power) and power != '' else "N/A")
        st.metric("Duration", f"{duration} h" if not pd.isna(duration) and duration != '' else "N/A")
    with col2:
        st.metric("Energy", f"{energy} MWh" if not pd.isna(energy) and energy != '' else "N/A")
    
    st.divider()
    
    # Ownership & Status
    st.markdown("**Ownership & Status**")
    tech_provider = project_row.get('Tech provider ', 'N/A')
    customer = project_row.get('Customer/Owner', 'N/A')
    status = project_row.get('Status', 'N/A')
    
    st.write(f"Provider: {tech_provider if not pd.isna(tech_provider) and str(tech_provider).strip() != '' else 'N/A'}")
    st.write(f"Owner: {customer if not pd.isna(customer) and str(customer).strip() != '' and str(customer) != 'NA' else 'N/A'}")
    st.write(f"Status: {status if not pd.isna(status) else 'N/A'}")
    
    # Website link
    website = project_row.get('Website', '')
    if not pd.isna(website) and str(website).strip() != '':
        st.divider()
        st.markdown(f"[Visit Website]({website})")


def display_project_list(df_clean, selected_state=None):
    """
    Display interactive project list with side panel detail view.
    Shows first 10 projects by default with expand option.
    """
    # Initialize selected project in session state
    if 'selected_project_idx' not in st.session_state:
        st.session_state.selected_project_idx = None
    
    # Initialize show_all in session state
    if 'show_all_projects' not in st.session_state:
        st.session_state.show_all_projects = False
    
    # Filter by state if provided
    if selected_state:
        display_df = df_clean[df_clean['State'] == selected_state].copy()
    else:
        display_df = df_clean.copy()
    
    if len(display_df) == 0:
        st.info("No projects found matching the current filters.")
        return
    
    # Reset index for consistent indexing
    display_df = display_df.reset_index(drop=True)
    
    total_projects = len(display_df)
    
    # Determine how many projects to show
    if st.session_state.show_all_projects or total_projects <= 10:
        projects_to_show = total_projects
    else:
        projects_to_show = 10
    
    st.caption(f"Showing {projects_to_show} of {total_projects} project(s)")
    
    # Two-column layout: List on left, Detail on right
    list_col, detail_col = st.columns([1, 1])
    
    with list_col:
        st.markdown("### Projects")
        
        # Display project list items
        for idx in range(projects_to_show):
            row = display_df.iloc[idx]
            
            project_name = row.get('Project name', 'Unnamed Project')
            if pd.isna(project_name) or str(project_name).strip() == '':
                project_name = "Unnamed Project"
            
            state = row.get('State', 'N/A')
            tech_type = row.get('Detailed Technology', row.get('Technology Type', 'N/A'))
            power = row.get('Power [MW]', '')
            energy = row.get('Energy  [MWh]', '')
            
            # Build metadata line
            meta_parts = []
            meta_parts.append(str(state) if not pd.isna(state) else 'N/A')
            meta_parts.append(str(tech_type) if not pd.isna(tech_type) else 'N/A')
            
            specs = []
            if not pd.isna(power) and power != '':
                specs.append(f"{power} MW")
            if not pd.isna(energy) and energy != '':
                specs.append(f"{energy} MWh")
            if specs:
                meta_parts.append(" / ".join(specs))
            
            meta_line = " | ".join(meta_parts)
            
            # Create clickable button for each project
            if st.button(
                f"{project_name}\n\n{meta_line}",
                key=f"project_{idx}_{selected_state}",
                use_container_width=True,
                type="primary" if st.session_state.selected_project_idx == idx else "secondary"
            ):
                st.session_state.selected_project_idx = idx
                st.rerun()
        
        # Show expand/collapse button if more than 10 projects
        if total_projects > 10:
            if st.session_state.show_all_projects:
                if st.button("Show Less", use_container_width=True):
                    st.session_state.show_all_projects = False
                    st.rerun()
            else:
                if st.button(f"Show All {total_projects} Projects", use_container_width=True):
                    st.session_state.show_all_projects = True
                    st.rerun()
    
    with detail_col:
        if st.session_state.selected_project_idx is not None and st.session_state.selected_project_idx < len(display_df):
            selected_row = display_df.iloc[st.session_state.selected_project_idx]
            display_project_detail(selected_row)
        else:
            st.info("Select a project from the list to view details")


def render_project_map(projects_df):
    """
    Render interactive project map with click selection.
    """
    st.header("LDES Project Map")

    state_counts, df_clean = prepare_map_data(projects_df)

    if 'selected_state' not in st.session_state:
        st.session_state.selected_state = None

    fig = create_choropleth_map(state_counts)

    # Use selected_state as part of the key to force re-render when selection changes
    map_key = f"state_map_{st.session_state.selected_state}"

    selected_points = st.plotly_chart(
        fig,
        use_container_width=True,
        key=map_key,
        on_select="rerun",
        selection_mode="points"
    )

    # Check if user clicked on the map
    if selected_points and hasattr(selected_points, 'selection'):
        if selected_points.selection and 'points' in selected_points.selection and len(selected_points.selection['points']) > 0:
            clicked_point = selected_points.selection['points'][0]
            if 'customdata' in clicked_point:
                new_state = clicked_point['customdata'][0]
                # If clicking the same state, deselect it
                if st.session_state.selected_state == new_state:
                    st.session_state.selected_state = None
                    st.session_state.selected_project_idx = None
                    st.session_state.show_all_projects = False
                else:
                    st.session_state.selected_state = new_state
                    st.session_state.selected_project_idx = None
                    st.session_state.show_all_projects = False

    if st.session_state.selected_state:
        st.subheader(f"Projects in {st.session_state.selected_state}")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.info(f"Currently viewing: **{st.session_state.selected_state}**")
        with col2:
            if st.button("Clear Selection", key="clear_btn"):
                st.session_state.selected_state = None
                st.session_state.selected_project_idx = None
                st.session_state.show_all_projects = False
                st.rerun()

        display_project_list(df_clean, st.session_state.selected_state)

    else:
        st.info("Click on a state in the map above to view projects by state")

        with st.expander("Select a state manually"):
            selected_state = st.selectbox(
                "Select a state:",
                options=sorted(state_counts['State'].unique()),
                index=None,
                placeholder="Choose a state...",
                key="manual_state_select"
            )

            if selected_state:
                st.session_state.selected_state = selected_state
                st.session_state.selected_project_idx = None
                st.session_state.show_all_projects = False
                st.rerun()