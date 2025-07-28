import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# If running locally, change the 'csv_url' variable to the path of your local CSV file.
csv_url = "https://raw.githubusercontent.com/ndmart505/LDES-Tool/main/ldes_data_example.csv"

# Streamlit Function
def plotdata(df, key_prefix=""):
    # Set default view to wide
    st.set_page_config(layout="wide")
    
    # Sidebar filters
    st.sidebar.header("Filters")

    # Filter by "Technology Type"
    if "Technology Type" in df.columns:
        technology_types = df["Technology Type"].unique()
        selected_technology_types = []
        for tech_type in technology_types:
            # Create a checkbox for each technology type
            if st.sidebar.checkbox(tech_type, value=True, key=f"{key_prefix}tech_type_{tech_type}"):
                selected_technology_types.append(tech_type)
        # Filter the DataFrame based on selected technology types
        df = df[df["Technology Type"].isin(selected_technology_types)]

    # Allow users to select columns to filter by
    filter_columns = st.sidebar.multiselect("Select columns to filter by", options=df.columns, key=f"{key_prefix}filter_columns")

    # Filter by "Detailed Technology"
    if "Detailed Technology" in filter_columns:
        detailed_technologies = df["Detailed Technology"].unique()
        selected_detailed_technologies = []
        for detailed_tech in detailed_technologies:
            # Create a checkbox for each detailed technology
            if st.sidebar.checkbox(detailed_tech, value=True, key=f"{key_prefix}detailed_tech_{detailed_tech}"):
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
            filters[col] = st.sidebar.slider(f"Filter by {col}", min_value=min_val, max_value=max_val, value=(min_val, max_val), key=f"{key_prefix}slider_{col}")

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
            "Rating – Low (MW)", "Rating – High (MW)",
            "Duration – Low (hr)", "Duration – High (hr)",
            "RTE (%)",
            "Degradation – Low (%/cycle)", "Degradation – High (%/cycle)",
            "Ramp Rate – Low (%/hr)", "Ramp Rate – High (%/hr)",
            "Response Time (off) (h)", "Inertia Constant (s)",
            "Operating Temp – Low (°C)", "Operating Temp – High (°C)",
            "Footprint – Low (m²/MWh)", "Footprint – High (m²/MWh)",
            "TRL", "ARL"
        ],
        key=f"{key_prefix}y_axis_value"
    )

    # Sets all figures to uniform size
    def set_figure_size(fig, width=1500, height=1000):
        fig.update_layout(width=width, height=height)
        return fig

    # Dictionary to hold all figures
    figures = {
        "Custom Graph": set_figure_size(
            create_range_bar(filtered_df, "Detailed Technology", "RTE – Low (%)", "RTE – High (%)",
                            "Round-Trip Efficiency (RTE) Range (%)")
            if y_axis_value == "RTE (%)"
            else 
            px.bar(filtered_df, x="Detailed Technology", y=y_axis_value, title=f"Custom Graph: {y_axis_value}", color="Detailed Technology")),
        "Capacity Range (MW)": set_figure_size(create_range_bar(filtered_df, "Detailed Technology", "Rating – Low (MW)", "Rating – High (MW)", "Capacity Range (MW)")),
        "Duration Range (hr)": set_figure_size(create_range_bar(filtered_df, "Detailed Technology", "Duration – Low (hr)", "Duration – High (hr)", "Duration Range (hr)")),
        "Round-Trip Efficiency (RTE) Range (%)": set_figure_size(create_range_bar(filtered_df, "Detailed Technology", "RTE – Low (%)", "RTE – High (%)", "Round-Trip Efficiency (RTE) Range (%)")),
        "Degradation Rate Range (%/cycle)": set_figure_size(create_range_bar(filtered_df, "Detailed Technology", "Degradation – Low (%/cycle)", "Degradation – High (%/cycle)", "Degradation Rate Range (%/cycle)")),
        "Ramp Rate Range (%/hr)": set_figure_size(create_range_bar(filtered_df, "Detailed Technology", "Ramp Rate – Low (%/hr)", "Ramp Rate – High (%/hr)", "Ramp Rate Range (%/hr)")),
        "Operating Temperature Range (°C)": set_figure_size(create_range_bar(filtered_df, "Detailed Technology", "Operating Temp – Low (°C)", "Operating Temp – High (°C)", "Operating Temperature Range (°C)")),
        "Footprint Range (m²/MWh)": set_figure_size(create_range_bar(filtered_df, "Detailed Technology", "Footprint – Low (m²/MWh)", "Footprint – High (m²/MWh)", "Footprint Range (m²/MWh)")),
        "Technology Readiness Level (TRL)": set_figure_size(px.bar(filtered_df, x="Detailed Technology", y="TRL", title="Technology Readiness Level (TRL)", color="Detailed Technology")),
        "Application Readiness Level (ARL)": set_figure_size(px.bar(filtered_df, x="Detailed Technology", y="ARL", title="Application Readiness Level (ARL)", color="Detailed Technology")),
        "Response Time from Off State (h)": set_figure_size(px.bar(filtered_df, x="Detailed Technology", y="Response Time (off) (h)", title="Response Time from Off State (h)", color="Detailed Technology")),
        "Inertia Constant (s)": set_figure_size(px.bar(filtered_df, x="Detailed Technology", y="Inertia Constant (s)", title="Inertia Constant (s)", color="Detailed Technology")),
        "Expected Downtime": set_figure_size(px.bar(filtered_df, x="Detailed Technology", color="Expected Downtime", title="Expected Downtime")),
        "Geological Feature Requirement": set_figure_size(px.bar(filtered_df, x="Detailed Technology", color="Geological Req.", title="Geological Feature Requirement")),
        "Historical Fire Events": set_figure_size(px.bar(filtered_df, x="Detailed Technology", color="Fire Incidents", title="Historical Fire Events")),
        "Environmental Impact": set_figure_size(px.bar(filtered_df, x="Detailed Technology", color="Environmental Impact", title="Environmental Impact")),
    }

    # Allows user to select graph
    selected_chart = st.selectbox("Select Graph to View:", list(figures.keys()), key=f"{key_prefix}graph_selector")
    st.plotly_chart(figures[selected_chart], use_container_width=True,key=f"{key_prefix}plotly_chart")

    # Display the filtered data
    st.header("Filtered Data")
    st.dataframe(filtered_df)

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
selected_tab = st.radio(
    label="",
    options=["Documentation", "Visualization","Custom Data Set"],
    horizontal=True
)

# Documentation Tab
if selected_tab == "Documentation":
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
elif selected_tab == "Visualization":
    # Load data from the CSV file and plot
    try:
        df = pd.read_csv(csv_url)
        st.success("File successfully loaded")
        plotdata(df, key_prefix="viz_")
        st.header("Data loaded from CSV")
        st.dataframe(df)
    except Exception as e:
        st.error(f"Error loading the CSV file: {e}")

# Custom Data Set Tab
elif selected_tab == "Custom Data Set":
    st.header("Upload and Visualize Custom Data Set")
    uploaded_file = st.file_uploader("Upload a Custom Data Set as a CSV file", type="csv")

    if uploaded_file is not None:
        try:
            custom_df = pd.read_csv(uploaded_file)
            st.success("Custom CSV file loaded")
            plotdata(custom_df, key_prefix="custom_")
        except Exception as e:
            st.error(f"Error processing uploaded file: {e}")
    else: 
        st.info("Please upload a CSV file to get started.")
