import streamlit as st

def render():
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
    
    st.title("Energy Storage Technologies Visualization App")
    
    st.markdown("""
        Welcome to the LDES Energy Storage Technologies Visualization App! This tool is 
        designed to facilitate dynamic visualization of long-duration energy storage metrics and projects.  

        By leveraging data sourced from industry reports, academic literature, and expert insights, 
        the app empowers users to effectively filter and down-select options based on high-priority metrics. 
        Our goal is to enhance your decision-making process and provide a comprehensive understanding of 
        energy storage technologies.
    """)

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
        st.markdown("")

    st.markdown("""
        Use the buttons above to navigate between different sections:
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

        - **Round Trip Efficiency AC-AC (%):** Ratio of energy discharged from the system (AC) from a starting state of charge
         to the energy received (AC) to bring the system to the same starting charge.

        - **Discharge Duration (hrs):** The duration at which the system discharges the rated nameplate power. Optimal discharge durations provided. 

        - **Degradation Rate (% Energy Capacity Change/Cycle):** Rate at which the energy capacity of the ESS degrades. 
        Rate is dependent on ambient conditions, depth of discharge, charge rate, and discharge rate. 
        Provide nominal values and relevant conditions.

        - **Cycle Life (# of cycles):** Number of cycles expected within the life of the energy storage system (i.e. cycles until retirement).

        - **Ramp Rate (% rated power/s):** The speed at which storage can increase or decrease power input and output. Starting state provided in tabulated data. 

        - **Response Time (s):** Time required for a system to output (or input) energy at full rated power. Starting state provided in tabulated data. 
                    
        - **Energy Density (acre/MWhe):** Amount of land required to deploy 1 unit of energy capacity (electrical equivalent) of the ESS Storage Block. 
                    
        - **Power Density (acre/MWe):** Amount of land required to deploy 1 unit of power (electrical equivalent) of the ESS Power Equipment. 
        If the storage and power blocks are separate (e.g., thermal energy storage), this value corresponds to the footprint of the power-related equipment only.             
        """, unsafe_allow_html=True)

    with right_col:
        st.markdown("""              
        - **Geological Feature Requirement (Yes or No):** Does the technology require a natural geological feature? 

        - **Historical Fire Events (≥5 = high, 1–5 = medium, 0 = low):**  Number of fire events associated with LDES technology because of the LDES system itself.

        - **Off-gassing (Yes or No):** Does the system produce gases as a byproduct of the system operations? 

        - **Environmental Impact (Qualitative Low, Medium, High):** Will the system be negatively intrusive in the natural environment in which it is situated (water consumption, soil erosion, form-factor, etc.)?

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

    st.subheader("Notes:")    

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