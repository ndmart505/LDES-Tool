import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Set default view to wide
st.set_page_config(layout="wide", page_title="LDES Energy Storage")

csv_url = "ldes_real_data_v0.csv"
projects_url = "LDES project tracking list v3.csv"

# Header with logo (appears on all pages)
st.markdown(
    """
    <div style="text-align: center;">
        <img src="https://www.sandia.gov/app/uploads/sites/256/2025/07/LDES-Logo-blackBG.png" width="653" height="115">
    </div>
    """, 
    unsafe_allow_html=True
)

st.divider()

# Sidebar navigation
st.sidebar.header("Navigation")
page_options = ["Documentation", "Visualization", "Project Tracking"]
st.session_state.page = st.sidebar.selectbox(
    "Select Page",
    options=page_options,
    index=page_options.index(st.session_state.get('page', 'Documentation'))
)

st.sidebar.divider()

# ==================== DOCUMENTATION PAGE ====================
if st.session_state.page == "Documentation":
    # Hide sidebar for Documentation page
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] {
            display: none;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
if st.session_state.page == "Documentation":
    st.title("Energy Storage Technologies Visualization App")
    
    st.markdown("""
        Welcome to the LDES Energy Storage Technologies Visualization App.""")

    # Navigation buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Visualization", use_container_width=True, type="primary"):
            st.session_state.page = "Visualization"
            st.rerun()
    with col2:
        if st.button("Project Tracking", use_container_width=True, type="primary"):
            st.session_state.page = "Project Tracking"
            st.rerun()
    with col3:
        st.markdown("")  # Empty column for spacing 


    st.markdown("""
        the buttons above to navigate between different sections:
        - **Documentation**: Learn about the data definitions, assumptions, and methodology
        - **Visualization**: Explore interactive charts and filter energy storage technology data
        - **Project Tracking**: View and analyze LDES project locations and status
    """)

    st.header("Documentation")
    st.markdown("""
    **Definitions:**
    - **Technology Type:** Broad category of energy storage technologies (e.g., Electrochemical, Thermal).
    - **Detailed Technology:** Specific energy storage technologies within a category (e.g., Lithium-ion, Sodium-ion).
    - **TRL (Technology Readiness Level):** A measure of technology maturity (scale: 1–9).
    - **ARL (Application Readiness Level):** A measure of application maturity (scale: 1–9).

    **Assumptions:**
    - Data is provided in a cleaned `.csv` file format.
    - Numerical columns contain valid numeric data (e.g., no strings or missing values).

    **Methodology:**
    - Data is loaded from a `.csv` file.
    - Users can filter the data using sidebar controls (checkboxes, sliders, dropdowns).
    - Visualizations are generated dynamically based on filtered data.
    """)

# ==================== VISUALIZATION PAGE ====================
elif st.session_state.page == "Visualization":
    st.title("Energy Storage Technologies Visualization")
    
    try:
        df = pd.read_csv(csv_url)
        
        # Sidebar filters
        st.sidebar.header("Visualization Filters")

        # Filter by "Technology Type"
        if "Technology Type" in df.columns:
            technology_types = df["Technology Type"].unique()
            selected_technology_types = []
            for tech_type in technology_types:
                if st.sidebar.checkbox(tech_type, value=True):
                    selected_technology_types.append(tech_type)
            df = df[df["Technology Type"].isin(selected_technology_types)]

        # Filter by "Detailed Technology" using pills
        if "Detailed Technology" in df.columns:
            detailed_technologies = sorted(df["Detailed Technology"].unique())

            selected_detailed_technologies = st.sidebar.pills(
                "Detailed Technologies",
                options=detailed_technologies,
                default=detailed_technologies,
                selection_mode="multi"
            )

            df = df[df["Detailed Technology"].isin(selected_detailed_technologies)]

        # Define the mapping of combined metrics to their low/high column names
        range_metrics = {
            "Duration (hr)": ("Duration - Low (hr)", "Duration - High (hr)"),
            "RTE (%)": ("RTE - Low (%)", "RTE - High (%)"),
            "Degradation (%/cycle)": ("Degradation - Low (%/cycle)", "Degradation - High (%/cycle)"),
            "Cycle Life (#)": ("Cycle Life - Low (#)", "Cycle Life - High (#)"),
            "Ramp Rate (% rated power/min)": ("Ramp Rate - Low (% rated power/min)", "Ramp Rate - High (% rated power/min)"),
            "Response Time (s)": ("Response Time - Low (s)", "Response Time - High (s)"),
            "Energy Density (acre/MWhe)": ("Energy Density - Low (acre/MWhe)", "Energy Density - High (acre/MWhe)"),
            "Power Density (acre/MW)": ("Power Density - Low (acre/MW)", "Power Density - High (acre/MW)"),
            "CAPEX Energy Basis ($/kWhe)": ("CAPEX Energy Basis - Low ($/kWhe)", "CAPEX Energy Basis - High ($/kWhe)"),
            "CAPEX Power Basis ($/kWe)": ("CAPEX Power Basis - Low ($/kWe)", "CAPEX Power Basis - High ($/kWe)"),
            "OPEX ($/kW-year)": ("OPEX - Low ($/kW-year)", "OPEX - High ($/kW-year)")
        }

        # Create list of available filter options (excluding Detailed Technology)
        available_filters = []
        
        for metric_name, (low_col, high_col) in range_metrics.items():
            if low_col in df.columns and high_col in df.columns:
                available_filters.append(metric_name)
        
        single_value_columns = ["TRL", "ARL", "MRL"]
        for col in single_value_columns:
            if col in df.columns:
                available_filters.append(col)
        
        filter_columns = st.sidebar.multiselect("Select columns to filter by", options=available_filters)

        active_filter_ranges = {}

        # Create sliders for selected filter columns
        filtered_df = df.copy()
        
        for filter_col in filter_columns:
            if filter_col in range_metrics:
                low_col, high_col = range_metrics[filter_col]
                
                all_low_values = df[low_col].dropna()
                all_high_values = df[high_col].dropna()
                
                if len(all_low_values) > 0 and len(all_high_values) > 0:
                    overall_min = min(all_low_values.min(), all_high_values.min())
                    overall_max = max(all_low_values.max(), all_high_values.max())
                    
                    selected_range = st.sidebar.slider(
                        f"Filter by {filter_col}", 
                        min_value=float(overall_min), 
                        max_value=float(overall_max), 
                        value=(float(overall_min), float(overall_max)),
                        key=f"slider_{filter_col}"
                    )
                    
                    active_filter_ranges[filter_col] = selected_range
                    
                    mask = (
                        (filtered_df[low_col] <= selected_range[1]) & 
                        (filtered_df[high_col] >= selected_range[0])
                    )
                    filtered_df = filtered_df[mask]
                    
            elif filter_col in ["TRL", "ARL", "MRL"] and filter_col in df.columns:
                if df[filter_col].dtype in [int, float]:
                    min_val = df[filter_col].min()
                    max_val = df[filter_col].max()
                    selected_range = st.sidebar.slider(
                        f"Filter by {filter_col}", 
                        min_value=float(min_val), 
                        max_value=float(max_val), 
                        value=(float(min_val), float(max_val)),
                        key=f"slider_{filter_col}"
                    )
                    filtered_df = filtered_df[
                        (filtered_df[filter_col] >= selected_range[0]) & 
                        (filtered_df[filter_col] <= selected_range[1])
                    ]

        # Function to create range bars with clipping
        def create_range_bar(df, x_col, y_low_col, y_high_col, title):
            fig = go.Figure()
            
            clip_range = None
            metric_name = None
            
            for metric, (low_col, high_col) in range_metrics.items():
                if low_col == y_low_col and high_col == y_high_col:
                    metric_name = metric
                    if metric in active_filter_ranges:
                        clip_range = active_filter_ranges[metric]
                    break
            
            for i, row in df.iterrows():
                low_val = row[y_low_col]
                high_val = row[y_high_col]
                
                rte_low = row.get("RTE - Low (%)", "N/A")
                rte_high = row.get("RTE - High (%)", "N/A")
                trl = row.get("TRL", "N/A")
                capex_low = row.get("CAPEX Energy Basis - Low ($/kWhe)", "N/A")
                capex_high = row.get("CAPEX Energy Basis - High ($/kWhe)", "N/A")
                
                hover_text = f"<b>{row[x_col]}</b><br><br>"
                hover_text += f"RTE: {rte_low} - {rte_high}%<br>" if rte_low != "N/A" else "RTE: N/A<br>"
                hover_text += f"TRL: {trl}<br>"
                hover_text += f"CAPEX: ${capex_low} - ${capex_high}/kWhe<br>" if capex_low != "N/A" else "CAPEX: N/A<br>"
                hover_text += "<extra></extra>"
                
                if clip_range:
                    clipped_low = max(low_val, clip_range[0])
                    clipped_high = min(high_val, clip_range[1])
                    
                    if clipped_low <= clipped_high:
                        fig.add_trace(go.Bar(
                            x=[row[x_col]],
                            y=[clipped_high - clipped_low],
                            base=[clipped_low],
                            name=row[x_col],
                            hovertemplate=hover_text
                        ))
                else:
                    fig.add_trace(go.Bar(
                        x=[row[x_col]],
                        y=[high_val - low_val],
                        base=[low_val],
                        name=row[x_col],
                        hovertemplate=hover_text
                    ))
            
            fig.update_layout(title=title, barmode='group')
            return fig

        # Sidebar for custom graph
        st.sidebar.header("Custom Graph")

        y_axis_value = st.sidebar.selectbox(
            "Select the y-axis value for the custom graph",
            options=[
                "Duration (hr)",
                "RTE (%)",
                "Degradation (%/cycle)",
                "Cycle Life (#)",
                "Ramp Rate (% rated power/min)",
                "Response Time (s)",
                "Energy Density (acre/MWhe)",
                "Power Density (acre/MW)",
                "CAPEX Energy Basis ($/kWhe)",
                "CAPEX Power Basis ($/kWe)",
                "OPEX ($/kW-year)",
                "TRL", "ARL", "MRL"
            ]
        )

        def set_figure_size(fig):
            fig.update_layout(
                margin=dict(l=50, r=50, t=80, b=50),
                font=dict(size=12),
                autosize=True
            )
            return fig

        def create_custom_graph(df, metric_type):        
            if metric_type in range_metrics:
                low_col, high_col = range_metrics[metric_type]
                return create_range_bar(df, "Detailed Technology", low_col, high_col, f"{metric_type} Range")
            else:
                return px.bar(df, x="Detailed Technology", y=metric_type, 
                             title=f"Custom Graph: {metric_type}", 
                             color="Detailed Technology")

        # Dictionary to hold all figures
        figures = {
            "Custom Graph": set_figure_size(create_custom_graph(filtered_df, y_axis_value)),
            "Duration Range (hr)": set_figure_size(create_range_bar(filtered_df, "Detailed Technology", "Duration - Low (hr)", "Duration - High (hr)", "Duration Range (hr)")),
            "Round-Trip Efficiency (RTE) Range (%)": set_figure_size(create_range_bar(filtered_df, "Detailed Technology", "RTE - Low (%)", "RTE - High (%)", "Round-Trip Efficiency (RTE) Range (%)")),
            "Degradation Rate Range (%/cycle)": set_figure_size(create_range_bar(filtered_df, "Detailed Technology", "Degradation - Low (%/cycle)", "Degradation - High (%/cycle)", "Degradation Rate Range (%/cycle)")),
            "Cycle Life Range (#)": set_figure_size(create_range_bar(filtered_df, "Detailed Technology", "Cycle Life - Low (#)", "Cycle Life - High (#)", "Cycle Life Range (#)")),
            "Ramp Rate Range (% rated power/min)": set_figure_size(create_range_bar(filtered_df, "Detailed Technology", "Ramp Rate - Low (% rated power/min)", "Ramp Rate - High (% rated power/min)", "Ramp Rate Range (% rated power/min)")),
            "Response Time Range (s)": set_figure_size(create_range_bar(filtered_df, "Detailed Technology", "Response Time - Low (s)", "Response Time - High (s)", "Response Time Range (s)")),
            "Energy Density Range (acre/MWhe)": set_figure_size(create_range_bar(filtered_df, "Detailed Technology", "Energy Density - Low (acre/MWhe)", "Energy Density - High (acre/MWhe)", "Energy Density Range (acre/MWhe)")),
            "Power Density Range (acre/MW)": set_figure_size(create_range_bar(filtered_df, "Detailed Technology", "Power Density - Low (acre/MW)", "Power Density - High (acre/MW)", "Power Density Range (acre/MW)")),
            "CAPEX Energy Basis Range ($/kWhe)": set_figure_size(create_range_bar(filtered_df, "Detailed Technology", "CAPEX Energy Basis - Low ($/kWhe)", "CAPEX Energy Basis - High ($/kWhe)", "CAPEX Energy Basis Range ($/kWhe)")),
            "CAPEX Power Basis Range ($/kWe)": set_figure_size(create_range_bar(filtered_df, "Detailed Technology", "CAPEX Power Basis - Low ($/kWe)", "CAPEX Power Basis - High ($/kWe)", "CAPEX Power Basis Range ($/kWe)")),
            "OPEX Range ($/kW-year)": set_figure_size(create_range_bar(filtered_df, "Detailed Technology", "OPEX - Low ($/kW-year)", "OPEX - High ($/kW-year)", "OPEX Range ($/kW-year)")),
            "Technology Readiness Level (TRL)": set_figure_size(px.bar(filtered_df, x="Detailed Technology", y="TRL", title="Technology Readiness Level (TRL)", color="Detailed Technology")),
            "Application Readiness Level (ARL)": set_figure_size(px.bar(filtered_df, x="Detailed Technology", y="ARL", title="Application Readiness Level (ARL)", color="Detailed Technology")),
            "Manufacturing Readiness Level (MRL)": set_figure_size(px.bar(filtered_df, x="Detailed Technology", y="MRL", title="Manufacturing Readiness Level (MRL)", color="Detailed Technology")),
            "Expected Downtime": set_figure_size(px.bar(filtered_df, x="Detailed Technology", color="Expected Downtime", title="Expected Downtime")),
            "Geological Feature Requirement": set_figure_size(px.bar(filtered_df, x="Detailed Technology", color="Geological Req.", title="Geological Feature Requirement")),
            "Historical Fire Events": set_figure_size(px.bar(filtered_df, x="Detailed Technology", color="Fire Incidents", title="Historical Fire Events")),
            "Environmental Impact": set_figure_size(px.bar(filtered_df, x="Detailed Technology", color="Environmental Impact", title="Environmental Impact")),
            "Separate Power & Energy": set_figure_size(px.bar(filtered_df, x="Detailed Technology", color="Separate Power & Energy ", title="Separate Power & Energy")),
            "Off-Gassing": set_figure_size(px.bar(filtered_df, x="Detailed Technology", color="Off-Gassing ", title="Off-Gassing")),
        }

        selected_chart = st.selectbox("Select Graph to View:", list(figures.keys()))
        st.plotly_chart(figures[selected_chart], use_container_width=True, config={'displayModeBar': True, 'responsive': True})

        # Display the filtered data
        st.header("Filtered Data")

        column_config = {}

        if "Technology Type" in filtered_df.columns:
            column_config["Technology Type"] = st.column_config.TextColumn(
                "Technology Type",
                width=115,
                pinned="left" 
            )
            
        if "Detailed Technology" in filtered_df.columns:
            column_config["Detailed Technology"] = st.column_config.TextColumn(
                "Detailed Technology", 
                width=260,
                pinned="left"
            )
            
        st.data_editor(
            filtered_df,
            column_config=column_config,
            use_container_width=True,
            height=400,
            disabled=True,
            hide_index=True
        )

    except Exception as e:
        st.error(f"Error loading the CSV file: {e}")

# ==================== PROJECT TRACKING PAGE ====================
elif st.session_state.page == "Project Tracking":
    st.title("LDES Project Tracking")
    
    st.markdown("""
    This page displays the LDES Project Tracking Spreadsheet with information about 
    various energy storage projects and their current status.
    """)
    
    try:
        import project_map
        
        # Load the CSV file
        projects_df = pd.read_csv(projects_url)
        
        # Sidebar filters for Project Tracking
        st.sidebar.header("Project Tracking Filters")
        
        # Filter by "Technology Type"
        if "Technology Type" in projects_df.columns:
            technology_types = projects_df["Technology Type"].unique()
            selected_technology_types = []
            for tech_type in technology_types:
                if st.sidebar.checkbox(f"{tech_type}", value=True, key=f"project_tech_{tech_type}"):
                    selected_technology_types.append(tech_type)
            filtered_projects_df = projects_df[projects_df["Technology Type"].isin(selected_technology_types)]
        else:
            filtered_projects_df = projects_df

        # Filter by "Detailed Technology"
        if "Detailed Technology" in projects_df.columns:
            detailed_technologies = sorted(projects_df["Detailed Technology"].unique())

            selected_detailed_technologies = st.sidebar.pills(
                "Detailed Technologies",
                options=detailed_technologies,
                default=detailed_technologies,
                selection_mode="multi"
            )

            filtered_projects_df = filtered_projects_df[
                filtered_projects_df["Detailed Technology"].isin(selected_detailed_technologies)
            ]

        # Display basic statistics
        st.subheader("Project Overview")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Projects", len(projects_df))
        with col2:
            st.metric("Filtered Projects", len(filtered_projects_df))

        # Render the project map
        project_map.render_project_map(filtered_projects_df)    
        
        # Display the full dataframe
        st.subheader("Project Data")
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
        
        # Option to download the data
        st.download_button(
            label="Download Project Data as CSV",
            data=filtered_projects_df.to_csv(index=False).encode('utf-8'),
            file_name='ldes_project_tracking.csv',
            mime='text/csv',
        )

    except Exception as e:
        st.error(f"Error loading the project tracking file: {e}")
        st.info("Please ensure the file exists at the specified URL and is accessible.")