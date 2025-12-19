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


def display_state_projects(df_clean, selected_state):
    """
    Display projects for a selected state.
    """
    state_projects = df_clean[df_clean['State'] == selected_state]

    if len(state_projects) > 0:
        st.subheader(f"Projects in {selected_state}")
        st.metric("Total Projects", len(state_projects))

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
    Render interactive project map with click selection.
    """
    st.header("LDES Project Map")

    state_counts, df_clean = prepare_map_data(projects_df)

    if 'selected_state' not in st.session_state:
        st.session_state.selected_state = None

    fig = create_choropleth_map(state_counts)

    selected_points = st.plotly_chart(
        fig,
        use_container_width=True,
        key="state_map",
        on_select="rerun"
    )

    if selected_points and hasattr(selected_points, 'selection') and selected_points.selection:
        if 'points' in selected_points.selection and len(selected_points.selection['points']) > 0:
            clicked_point = selected_points.selection['points'][0]
            if 'customdata' in clicked_point:
                st.session_state.selected_state = clicked_point['customdata'][0]

    st.subheader("View Projects by State")

    if st.session_state.selected_state:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.info(f"Currently viewing: **{st.session_state.selected_state}**")
        with col2:
            if st.button("Clear Selection"):
                st.session_state.selected_state = None
                st.rerun()

        display_state_projects(df_clean, st.session_state.selected_state)

    else:
        st.info("Click on a state to view its projects")

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
                st.rerun()