import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def prepare_map_data(df):
    """
    Aggregate project data by state and convert to state codes.
    
    Parameters:
    - df: DataFrame with project data including 'State' column
    
    Returns:
    - state_counts: DataFrame with state names, codes, and project counts
    - df_clean: Cleaned DataFrame
    """
    # State name to abbreviation mapping
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
    
    # Remove rows with missing or 'NA' states
    df_clean = df[df['State'].notna()].copy()
    df_clean = df_clean[df_clean['State'] != 'NA']
    
    # Count projects per state
    state_counts = df_clean.groupby('State').size().reset_index(name='project_count')
    
    # Add state abbreviations for the map
    state_counts['state_code'] = state_counts['State'].map(state_abbrev)
    
    # Remove any states that didn't map (shouldn't happen with clean data)
    state_counts = state_counts[state_counts['state_code'].notna()]
    
    return state_counts, df_clean


def create_choropleth_map(state_counts):
    """
    Generate an interactive US choropleth map with dark theme.
    
    Parameters:
    - state_counts: DataFrame with 'State', 'state_code', and 'project_count' columns
    
    Returns:
    - fig: Plotly figure object
    """
    # Custom dark blue color scale - reversed so more projects = darker
    custom_blue_scale = [
        [0.0, '#6baed6'],   # Lightest blue (fewer projects)
        [0.25, '#4292c6'],
        [0.5, '#2171b5'],
        [0.75, '#08519c'],
        [1.0, '#08306b']    # Darkest blue (more projects)
    ]
    
    fig = go.Figure(data=go.Choropleth(
        locations=state_counts['state_code'],
        z=state_counts['project_count'],
        locationmode='USA-states',
        colorscale=custom_blue_scale,
        text=state_counts['State'],
        colorbar=dict(
            title=dict(
                text="Number of<br>Projects",
                font=dict(color='white')
            ),
            tickfont=dict(color='white'),
            bgcolor='rgba(0,0,0,0.5)'
        ),
        hovertemplate='<b>%{text}</b><br>Projects: %{z}<extra></extra>',
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
            # Add state borders for all states
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


def display_state_projects(df_clean, selected_state):
    """
    Display projects for a selected state.
    
    Parameters:
    - df_clean: Cleaned DataFrame with project data
    - selected_state: State full name (e.g., 'California', 'Texas')
    """
    state_projects = df_clean[df_clean['State'] == selected_state]
    
    if len(state_projects) > 0:
        st.subheader(f"Projects in {selected_state}")
        st.metric("Total Projects", len(state_projects))
        
        # Display project table
        st.dataframe(
            state_projects,
            use_container_width=True,
            height=400,
            hide_index=True
        )
    else:
        st.info(f"No projects found for {selected_state}")


def render_project_map(projects_df):
    """
    Main function to render the project map interface.
    
    Parameters:
    - projects_df: DataFrame with all project data
    """
    st.header("LDES Project Map")
    st.markdown("Click on a state to view projects in that location.")
    
    # Prepare data
    state_counts, df_clean = prepare_map_data(projects_df)
    
    # Create and display map
    fig = create_choropleth_map(state_counts)
    st.plotly_chart(fig, use_container_width=True)
    
    # State selection dropdown (temporary - will be replaced with click events)
    st.subheader("View Projects by State")
    selected_state = st.selectbox(
        "Select a state:",
        options=sorted(state_counts['State'].unique()),
        index=None,
        placeholder="Choose a state..."
    )
    
    if selected_state:
        display_state_projects(df_clean, selected_state)