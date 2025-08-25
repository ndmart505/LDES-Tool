import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# If running locally, change the 'csv_url' variable to the path of your local CSV file.
csv_url = "https://raw.githubusercontent.com/ndmart505/LDES-Tool/main/ldes_real_data_v0.csv"

# Streamlit Function
def plotdata(df):
    # Sidebar filters
    st.sidebar.header("Filters")

    # Filter by "Technology Type"
    if "Technology Type" in df.columns:
        technology_types = df["Technology Type"].unique()
        selected_technology_types = []
        for tech_type in technology_types:
            # Create a checkbox for each technology type
            if st.sidebar.checkbox(tech_type, value=True):
                selected_technology_types.append(tech_type)
        # Filter the DataFrame based on selected technology types
        df = df[df["Technology Type"].isin(selected_technology_types)]

    # Allow users to select columns to filter by
    filter_columns = st.sidebar.multiselect("Select columns to filter by", options=df.columns)

    # Filter by "Detailed Technology"
    if "Detailed Technology" in filter_columns:
        detailed_technologies = df["Detailed Technology"].unique()
        selected_detailed_technologies = []
        for detailed_tech in detailed_technologies:
            # Create a checkbox for each detailed technology
            if st.sidebar.checkbox(detailed_tech, value=True):
                selected_detailed_technologies.append(detailed_tech)
        # Filter the DataFrame based on selected detailed technologies
        df = df[df["Detailed Technology"].isin(selected_detailed_technologies)]

    # Create sliders for numerical columns selected for filtering
    filters = {}
    for col in filter_columns:
        if col not in ["Technology Type", "Detailed Technology"] and df[col].dtype in [int, float]:
            # Get the minimum and maximum values for the column
            min_val = df[col].min()
            max_val = df[col].max()
            # Create a slider for filtering the column
            filters[col] = st.sidebar.slider(f"Filter by {col}", min_value=min_val, max_value=max_val, value=(min_val, max_val))

    # Apply numerical filters to the DataFrame
    filtered_df = df.copy()
    for col, (min_val, max_val) in filters.items():
        filtered_df = filtered_df[(filtered_df[col] >= min_val) & (filtered_df[col] <= max_val)]

    # Function to create range bars for columns with low and high values
    def create_range_bar(df, x_col, y_low_col, y_high_col, title):
        """
        Creates a stacked bar graph to visualize ranges (low and high values).

        Parameters:
        - df: DataFrame containing the data.
        - x_col: Column for the x-axis (categorical data).
        - y_low_col: Column for the lower bound of the range.
        - y_high_col: Column for the upper bound of the range.
        - title: Title of the graph.

        Returns:
        - fig: Plotly Figure object.
        """
        fig = go.Figure()
        for i, row in df.iterrows():
            fig.add_trace(go.Bar(
                x=[row[x_col]],
                y=[row[y_high_col] - row[y_low_col]],  # Height of the bar
                base=[row[y_low_col]],  # Starting point of the bar
                name=row[x_col]
            ))
        fig.update_layout(title=title, barmode='group')
        return fig

    # Sidebar for custom graph
    st.sidebar.header("Custom Graph")

    # Dropdown to select the y-axis value for the custom graph
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

    # Sets all figures to responsive size
    def set_figure_size(fig):
        fig.update_layout(
            margin=dict(l=50, r=50, t=80, b=50),
            font=dict(size=12),
            autosize=True
        )
        return fig

    # Function to create custom graph based on selection
    def create_custom_graph(df, metric_type):
        # Define the mapping of metric types to their low/high column names
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
        
        # Check if the selected metric has a range (low/high values)
        if metric_type in range_metrics:
            low_col, high_col = range_metrics[metric_type]
            return create_range_bar(df, "Detailed Technology", low_col, high_col, f"{metric_type} Range")
        else:
            # For single-value metrics (TRL, ARL, MRL)
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

    # Allows user to select graph
    selected_chart = st.selectbox("Select Graph to View:", list(figures.keys()))
    st.plotly_chart(figures[selected_chart], use_container_width=True, use_container_height=True)

    # Display the filtered data
    st.header("Filtered Data")
    st.dataframe(filtered_df)

# Set default view to wide
st.set_page_config(layout="wide")

# Create UI
st.markdown(
    """
    <div style="text-align: center;">
        <img src="https://www.sandia.gov/app/uploads/sites/256/2025/07/LDES-Logo-blackBG.png" width="653" height="115">
    </div>
    """, 
    unsafe_allow_html=True
)
st.title("Energy Storage Technologies Visualization App")

# Create tabs
tab1, tab2 = st.tabs(["Documentation", "Visualization"])

# Documentation Tab
with tab1:
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

# Visualization Tab
with tab2:
    # Load data from the CSV file and plot
    try:
        df = pd.read_csv(csv_url)
        st.success("File successfully loaded")
        plotdata(df)
        st.header("Data loaded from CSV")
        st.dataframe(df)
    except Exception as e:
        st.error(f"Error loading the CSV file: {e}")
