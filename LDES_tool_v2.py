import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# Set default view to wide
st.set_page_config(layout="wide", page_title="LDES Energy Storage")

csv_url = "ldes_real_data_v1.csv"
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
        Welcome to the LDES Energy Storage Technologies Visualization App! This innovative tool is 
        designed to facilitate dynamic visualization of long-duration energy storage metrics and projects.  

        By leveraging data sourced from industry reports, academic literature, and expert insights, 
        the app empowers users to effectively filter and down-select options based on high-priority metrics. 
        Our goal is to enhance your decision-making process and provide a comprehensive understanding of 
        energy storage technologies.
    """)

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
        Use the buttons above to navigate between different sections:
        - **Documentation**: Learn about the data definitions, assumptions, and methodology
        - **Visualization**: Explore interactive charts and filter energy storage technology data
        - **Project Tracking**: View and analyze LDES project locations and status
    """)

    st.header("Documentation")
    st.subheader("Definitions:")
    left_col, right_col = st.columns(2)
    with left_col:
        st.markdown("""
        - **Technology Type:** Broad category of energy storage technologies.

        - **Detailed Technology:** Specific energy storage technologies within a category.

        - **Round Trip Efficiency AC-AC (%):** Ratio of energy discharged from the system (AC) from a 
        starting state of charge to the energy received (AC) to bring the system to the same starting charge. 
        Clearly provide system boundary encompassed for provided RTE.

        - **Discharge Duration (hrs):** Sweet spot of discharge duration in hours. The duration at which 
        the system discharges the rated power.

        - **Degradation Rate (% Energy Capacity Change/Cycle):** Rate at which the energy capacity of the ESS degrades. 
        Rate is dependent on ambient conditions, depth of discharge, charge rate, and discharge rate. 
        Provide nominal values and relevant conditions.

        - **Cycle Life (# of cycles):** Number of cycles expected within the life of the energy storage system. 
        Cycles until retirement is required.

        - **Ramp Rate (% rated power/s):** The speed at which storage can increase or decrease input/output.

        - **Expected Downtime**

        - **Response Time from off state (s):** Time required for a system to output (or input) energy at full 
        rated power from shutdown state.
                    
        - **Energy Density (acre/MWhe):** Amount of land required to deploy 1 unit energy (electrical equivalent) 
        capacity of the ESS storage block. This metric should correspond to the storage block of the ESS.<br>  
        If the system has separate power and storage blocks (e.g., thermal energy storage), this value should 
        represent the storage block only footprint. If the ESS power and energy components are consolidated 
        in one package (e.g., battery container), this value should still represent the storage block footprint, 
        which consequently is the combined footprint. Note if the value is for a combined or separate power 
        and energy footprint.
        """,unsafe_allow_html=True)

    with right_col:
        st.markdown("""
        - **Power Density (acre/MWe):** Amount of land required to deploy 1 unit of power (electrical equivalent) 
        capacity of the ESS power equipment. If the storage and power blocks are separate (e.g., thermal energy storage), 
        this value only should correspond to the footprint of the power-related equipment. If the power and energy 
        equipment are consolidated in one package (e.g., battery container), this value should still represent 
        the power equipment footprint, which consequently is the combined footprint. Note if the value is for a 
        combined or separate power and energy footprint.
                    
        - **Geological Feature Requirement (Yes or No):** Does the technology require a natural geological feature? 
        Yes or No? If yes, describe the feature.

        - **Historical Fire Events (≥5 = high, 1–5 = medium, 0 = low):** Number of fire events associated with LDES 
        technologies as a result of the LDES system itself.

        - **Off-gassing (Yes or No):** Does the system produce gases as a byproduct of the system operations? 
        If yes, describe the gases produced and quantity of gases yielded per kWh of energy discharged or charged (m³/kWh).

        - **Environmental Impact (Qualitative Low, Medium, High):** Will the system be negatively intrusive in the 
        natural environment in which it is situated (water consumption, soil erosion, form-factor, etc.). 
        Describe impact.

        - **Technology Readiness Level (#):** Level of technology maturity and readiness for commercialization (1–9 scale).

        - **Adoption Readiness Level (#):** Readiness of users, processes, and organization needed to commercially deploy 
        the system (1–9).

        - **Manufacturing Readiness Level (#):** Readiness of technology to be commercially manufactured at intended 
        commercial deployment scale (1–9).

        - **CAPEX Energy Basis ($/kWhe):** Total capital cost of the Energy Storage System on an electrical energy basis 
        (four-hour basis).

        - **CAPEX Power Basis ($/kWe):** Total capital cost of the Energy Storage System on an electrical power unit basis.

        - **OPEX ($/kW-year):** Annual operational and maintenance expenditure associated with the Energy Storage System.
        """)


    st.markdown("""
        - Data is provided by technology experts associated with Department of Energy National Laboratories.
        - Technology experts sourced data from industry, literature, and expert judgement where applicable.
        - Data is time-stamped to June 2025.
        - **Disclaimer:** The quantitative metrics provided are not guaranteed to match the most up-to-date metrics 
        offered by technology providers. The data provided herein is the best data available at the time of this release.
    """)

    st.subheader("Methodology:")

    st.markdown("""
        - Data is loaded from the baseline `.csv` file.
        - Users can filter the data using sidebar controls (checkboxes, sliders, dropdowns).
        - Visualizations are generated dynamically based on filtered data.
    """)

# ==================== VISUALIZATION PAGE ====================
elif st.session_state.page == "Visualization":
    st.title("Energy Storage Technologies Visualization")
    
    try:
        df = pd.read_csv(csv_url)
        
        # Debug: Check actual column names
        # st.write("Column names in CSV:", df.columns.tolist())
        
        # Sidebar filters
        st.sidebar.header("Visualization Filters")
        
        # Define the mapping of combined metrics to their low/high column names
        range_metrics = {
            "Duration (hr)": ("Duration - Low (hr)", "Duration - High (hr)"),
            "RTE (%)": ("RTE - Low (%)", "RTE - High (%)"),
            "Degradation (%/cycle)": ("Degradation - Low (%/cycle)", "Degradation - High (%/cycle)"),
            "Cycle Life (#)": ("Cycle Life - Low (#)", "Cycle Life - High (#)"),
            "Ramp Rate (% rated power/sec)": ("Ramp Rate - Low (% rated power/sec)", "Ramp Rate - High (% rated power/sec)"),
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
        
        # Add categorical filters to available options
        categorical_filters = {
            "Geological Req.": "Geological Feature Requirement",
            "Fire Incidents": "Historical Fire Events",
            "Environmental Impact": "Environmental Impact",
            "Off-Gassing ": "Off-Gassing"
        }
        
        for col, display_name in categorical_filters.items():
            if col in df.columns:
                available_filters.append(display_name)
        
        # Move "Select columns to filter by" to top (after available_filters is defined)
        filter_columns = st.sidebar.multiselect("Select columns to filter by", options=available_filters)

        active_filter_ranges = {}

        # Create sliders/pills for selected filter columns immediately after the multiselect
        filtered_df = df.copy()
        
        # Extract boolean from Off-Gassing strings (Yes/No at start)
        def extract_offgassing_bool(value):
            if pd.isna(value):
                return None
            value_str = str(value).strip()
            if value_str.startswith("Yes"):
                return "Yes"
            elif value_str.startswith("No"):
                return "No"
            return None
        
        # Mapping of display names to actual column names for categorical filters
        categorical_filter_mapping = {
            "Geological Feature Requirement": "Geological Req.",
            "Historical Fire Events": "Fire Incidents",
            "Environmental Impact": "Environmental Impact",
            "Off-Gassing": "Off-Gassing "
        }
        
        for filter_col in filter_columns:
            # Check if it's a categorical filter
            if filter_col in categorical_filter_mapping:
                actual_col = categorical_filter_mapping[filter_col]
                
                if actual_col in df.columns:
                    # Special handling for Off-Gassing
                    if filter_col == "Off-Gassing":
                        unique_values = ["No", "Yes"]  # Ordered: No -> Yes
                        selected_values = st.sidebar.pills(
                            f"Filter by {filter_col}",
                            options=unique_values,
                            default=unique_values,
                            selection_mode="multi",
                            key=f"filter_{actual_col}"
                        )
                        # Filter by extracted boolean while preserving full string
                        mask = filtered_df[actual_col].apply(
                            lambda x: extract_offgassing_bool(x) in selected_values if pd.notna(x) else False
                        )
                        filtered_df = filtered_df[mask]
                    elif filter_col == "Geological Feature Requirement":
                        # Order: No -> Yes
                        unique_values = ["No", "Yes"]
                        available_values = [v for v in unique_values if v in filtered_df[actual_col].dropna().unique()]
                        selected_values = st.sidebar.pills(
                            f"Filter by {filter_col}",
                            options=available_values,
                            default=available_values,
                            selection_mode="multi",
                            key=f"filter_{actual_col}"
                        )
                        filtered_df = filtered_df[filtered_df[actual_col].isin(selected_values)]
                    elif filter_col in ["Historical Fire Events", "Environmental Impact"]:
                        # Order: Low -> Medium -> High
                        ordered_values = ["Low", "Medium", "High"]
                        available_values = [v for v in ordered_values if v in filtered_df[actual_col].dropna().unique()]
                        selected_values = st.sidebar.pills(
                            f"Filter by {filter_col}",
                            options=available_values,
                            default=available_values,
                            selection_mode="multi",
                            key=f"filter_{actual_col}"
                        )
                        filtered_df = filtered_df[filtered_df[actual_col].isin(selected_values)]
                    else:
                        # Regular categorical filter using pills (sorted alphabetically)
                        unique_values = sorted(filtered_df[actual_col].dropna().unique())
                        selected_values = st.sidebar.pills(
                            f"Filter by {filter_col}",
                            options=unique_values,
                            default=unique_values,
                            selection_mode="multi",
                            key=f"filter_{actual_col}"
                        )
                        filtered_df = filtered_df[filtered_df[actual_col].isin(selected_values)]
            
            elif filter_col in range_metrics:
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

        # Filter by "Technology Type"
        if "Technology Type" in df.columns:
            technology_types = df["Technology Type"].unique()
            selected_technology_types = []
            for tech_type in technology_types:
                if st.sidebar.checkbox(tech_type, value=True):
                    selected_technology_types.append(tech_type)
            filtered_df = filtered_df[
                filtered_df["Technology Type"].isin(selected_technology_types)
            ]


        # Filter by "Detailed Technology" using pills organized by category
        if "Detailed Technology" in df.columns:
            # Define categories and their technologies (alphabetically ordered)
            tech_categories = {
                "Electrochemical": ["Iron-Flow", "Lead-acid", "Lithium-ion", "Organic-Solid Flow", "Sodium-ion", "Vanadium-Flow", "Zinc-Anode"],
                "Thermal": ["Molten Salt TES ", "Solid Media TES - Pumped TES", "Solid Media TES - TPV ", "Thermochemical "],
                "Mechanical": ["Compressed Air Energy Storage (Caverns)", "Compressed Gas Energy Storage", "Gravitational Storage (Blocks)", "Gravitational Storage (Railcars)", "Liquid Air", "Pumped Storage Hydropower (PSH)"],
                "Chemical": ["Hydrogen"]
            }
            
            # Collect all selected detailed technologies based on active technology types
            all_selected_detailed = []
            
            for tech_type in selected_technology_types:
                if tech_type in tech_categories:
                    st.sidebar.markdown(f"**{tech_type}**")
                    
                    # Get available technologies for this category
                    available_techs = [t for t in tech_categories[tech_type] if t in df["Detailed Technology"].unique()]
                    
                    if available_techs:
                        selected_techs = st.sidebar.pills(
                            f"{tech_type}_detailed",
                            options=available_techs,
                            default=available_techs,
                            selection_mode="multi",
                            label_visibility="collapsed"
                        )
                        all_selected_detailed.extend(selected_techs)
            
            # Filter dataframe by selected detailed technologies
            if all_selected_detailed:
                filtered_df = filtered_df[
                    filtered_df["Detailed Technology"].isin(all_selected_detailed)
                ]

            else:
                # If no detailed technologies selected, show empty dataframe
                df = df[df["Detailed Technology"].isin([])]

        # Function to create range bars with clipping
        def create_range_bar(df, x_col, y_low_col, y_high_col, title):
            if len(df) == 0:
                fig = go.Figure()
                fig.update_layout(title=title, xaxis_title=x_col)
                return fig
                
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
                # Skip rows with NaN values
                if pd.isna(row[y_low_col]) or pd.isna(row[y_high_col]):
                    continue
                    
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

        def set_figure_size(fig):
            fig.update_layout(
                margin=dict(l=50, r=50, t=80, b=50),
                font=dict(size=12),
                autosize=True,
                showlegend=False
            )
            return fig
        
        def set_figure_size_with_legend(fig):
            fig.update_layout(
                margin=dict(l=50, r=50, t=80, b=50),
                font=dict(size=12),
                autosize=True
            )
            return fig

        # Dictionary to hold all figures
        figures = {
            "Duration Range (hr)": set_figure_size(create_range_bar(filtered_df, "Detailed Technology", "Duration - Low (hr)", "Duration - High (hr)", "Duration Range (hr)")),
            "Round-Trip Efficiency (RTE) Range (%)": set_figure_size(create_range_bar(filtered_df, "Detailed Technology", "RTE - Low (%)", "RTE - High (%)", "Round-Trip Efficiency (RTE) Range (%)")),
            "Degradation Rate Range (%/cycle)": set_figure_size(create_range_bar(filtered_df, "Detailed Technology", "Degradation - Low (%/cycle)", "Degradation - High (%/cycle)", "Degradation Rate Range (%/cycle)")),
            "Cycle Life Range (#)": set_figure_size(create_range_bar(filtered_df, "Detailed Technology", "Cycle Life - Low (#)", "Cycle Life - High (#)", "Cycle Life Range (#)")),
            "Ramp Rate Range (% rated power/sec)": set_figure_size(create_range_bar(filtered_df, "Detailed Technology", "Ramp Rate - Low (% rated power/sec)", "Ramp Rate - High (% rated power/sec)", "Ramp Rate Range (% rated power/sec)")),
            "Response Time Range (s)": set_figure_size(create_range_bar(filtered_df, "Detailed Technology", "Response Time - Low (s)", "Response Time - High (s)", "Response Time Range (s)")),
            "Energy Density Range (acre/MWhe)": set_figure_size(create_range_bar(filtered_df, "Detailed Technology", "Energy Density - Low (acre/MWhe)", "Energy Density - High (acre/MWhe)", "Energy Density Range (acre/MWhe)")),
            "Power Density Range (acre/MW)": set_figure_size(create_range_bar(filtered_df, "Detailed Technology", "Power Density - Low (acre/MW)", "Power Density - High (acre/MW)", "Power Density Range (acre/MW)")),
            "CAPEX Energy Basis Range ($/kWhe)": set_figure_size(create_range_bar(filtered_df, "Detailed Technology", "CAPEX Energy Basis - Low ($/kWhe)", "CAPEX Energy Basis - High ($/kWhe)", "CAPEX Energy Basis Range ($/kWhe)")),
            "CAPEX Power Basis Range ($/kWe)": set_figure_size(create_range_bar(filtered_df, "Detailed Technology", "CAPEX Power Basis - Low ($/kWe)", "CAPEX Power Basis - High ($/kWe)", "CAPEX Power Basis Range ($/kWe)")),
            "OPEX Range ($/kW-year)": set_figure_size(create_range_bar(filtered_df, "Detailed Technology", "OPEX - Low ($/kW-year)", "OPEX - High ($/kW-year)", "OPEX Range ($/kW-year)")),
            "Technology Readiness Level (TRL)": set_figure_size(px.bar(filtered_df, x="Detailed Technology", y="TRL", title="Technology Readiness Level (TRL)", color="Detailed Technology")),
            "Application Readiness Level (ARL)": set_figure_size(px.bar(filtered_df, x="Detailed Technology", y="ARL", title="Application Readiness Level (ARL)", color="Detailed Technology")),
            "Manufacturing Readiness Level (MRL)": set_figure_size(px.bar(filtered_df, x="Detailed Technology", y="MRL", title="Manufacturing Readiness Level (MRL)", color="Detailed Technology")),
            "Geological Feature Requirement": set_figure_size_with_legend(px.bar(filtered_df, x="Detailed Technology", color="Geological Req.", title="Geological Feature Requirement")),
            "Historical Fire Events": set_figure_size_with_legend(px.bar(filtered_df, x="Detailed Technology", color="Fire Incidents", title="Historical Fire Events")),
            "Environmental Impact": set_figure_size_with_legend(px.bar(filtered_df, x="Detailed Technology", color="Environmental Impact", title="Environmental Impact")),
            "Separate Power & Energy": set_figure_size_with_legend(px.bar(filtered_df, x="Detailed Technology", color="Separate Power & Energy ", title="Separate Power & Energy")),
        }
        
        # Create custom Off-Gassing chart with Yes/No colors and hover details
        def create_offgassing_chart(df):
            if len(df) == 0:
                # Return empty figure if no data
                fig = go.Figure()
                fig.update_layout(
                    title="Off-Gassing",
                    xaxis_title="Detailed Technology",
                    yaxis_title="Count"
                )
                return fig
            
            # Create a new column for Yes/No display
            df_offgassing = df.copy()
            df_offgassing["Off-Gassing Display"] = df_offgassing["Off-Gassing "].apply(
                lambda x: "Yes" if pd.notna(x) and str(x).strip().startswith("Yes") else "No"
            )
            
            # Define colors for Yes/No
            color_map = {"Yes": "#EF553B", "No": "#00CC96"}  # Plotly default colors
            
            # Track which legend items we've added
            legend_added = set()
            
            # Create figure with custom hover
            fig = go.Figure()
            
            for i, row in df_offgassing.iterrows():
                offgassing_full = row.get("Off-Gassing ", "")
                offgassing_display = row["Off-Gassing Display"]
                
                # Create hover text with full explanation
                hover_text = f"<b>{row['Detailed Technology']}</b><br><br>"
                hover_text += f"Off-Gassing: {offgassing_display}<br>"
                hover_text += f"Details: {offgassing_full}<br>"
                hover_text += "<extra></extra>"
                
                # Only show legend for first occurrence of each Yes/No
                show_legend = offgassing_display not in legend_added
                if show_legend:
                    legend_added.add(offgassing_display)
                
                fig.add_trace(go.Bar(
                    x=[row["Detailed Technology"]],
                    y=[1],
                    name=offgassing_display,
                    legendgroup=offgassing_display,
                    showlegend=show_legend,
                    marker_color=color_map[offgassing_display],
                    hovertemplate=hover_text
                ))
            
            fig.update_layout(
                title="Off-Gassing",
                yaxis_title="Count",
                xaxis_title="Detailed Technology",
                margin=dict(l=50, r=50, t=80, b=50),
                font=dict(size=12),
                autosize=True,
                barmode='group'
            )
            return fig
        
        figures["Off-Gassing"] = create_offgassing_chart(filtered_df)

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
        import traceback
        st.code(traceback.format_exc())

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

        # Filter by "Detailed Technology" using pills organized by category
        if "Detailed Technology" in projects_df.columns:
            # Define categories and their technologies for project tracking (alphabetically ordered)
            project_tech_categories = {
                "Electrochemical": ["Iron Flow", "Lead-Acid", "Lithium-ion", "Sodium-ion", "Vanadium Flow"],
                "Mechanical": ["Compressed Air Storage", "Geopressured Geothermal System (GGS)", "Pumped Hydro Storage"],
                "Thermal": ["Latent Heat TES", "Molten Salt TES", "Sensible Heat TES", "Sodium-sulfur TES"]
            }
            
            # Collect all selected detailed technologies based on active technology types
            all_selected_project_detailed = []
            
            for tech_type in selected_technology_types:
                if tech_type in project_tech_categories:
                    st.sidebar.markdown(f"**{tech_type}**")
                    
                    # Get available technologies for this category
                    available_techs = [t for t in project_tech_categories[tech_type] if t in projects_df["Detailed Technology"].unique()]
                    
                    if available_techs:
                        selected_techs = st.sidebar.pills(
                            f"project_{tech_type}_detailed",
                            options=available_techs,
                            default=available_techs,
                            selection_mode="multi",
                            label_visibility="collapsed"
                        )
                        all_selected_project_detailed.extend(selected_techs)
            
            # Filter dataframe by selected detailed technologies
            if all_selected_project_detailed:
                filtered_projects_df = filtered_projects_df[
                    filtered_projects_df["Detailed Technology"].isin(all_selected_project_detailed)
                ]
            else:
                # If no detailed technologies selected, show empty dataframe
                filtered_projects_df = filtered_projects_df[
                    filtered_projects_df["Detailed Technology"].isin([])
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