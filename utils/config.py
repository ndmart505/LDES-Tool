CSV_URL = "ldes_real_data_v1.csv"
PROJECTS_URL = "LDES project tracking list v4.csv"
LOGO_URL = "https://www.sandia.gov/app/uploads/sites/256/2025/07/LDES-Logo-blackBG.png"

TECH_CATEGORIES_VIZ = {
    "Electrochemical": ["Iron-Flow", "Lead-acid", "Lithium-ion", "Organic-Solid Flow", "Sodium-ion", "Vanadium-Flow", "Zinc-Anode"],
    "Thermal": ["Molten Salt TES ", "Solid Media TES - Pumped TES", "Solid Media TES - TPV ", "Thermochemical "],
    "Mechanical": ["Compressed Air Energy Storage (Caverns)", "Compressed Gas Energy Storage", "Gravitational Storage (Blocks)", "Gravitational Storage (Railcars)", "Liquid Air", "Pumped Storage Hydropower (PSH)"],
    "Chemical": ["Hydrogen"]
}

TECH_CATEGORIES_PROJECT = {
    "Electrochemical": ["Iron Flow", "Lead-Acid", "Lithium-ion", "Sodium-ion", "Vanadium Flow"],
    "Mechanical": ["Compressed Air Storage", "Geopressured Geothermal System (GGS)", "Pumped Hydro Storage"],
    "Thermal": ["Latent Heat TES", "Molten Salt TES", "Sensible Heat TES", "Sodium-Sulfur TES"]
}

RANGE_METRICS = {
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

CATEGORICAL_FILTERS = {
    "Geological Req.": "Geological Feature Requirement",
    "Fire Incidents": "Historical Fire Events",
    "Environmental Impact": "Environmental Impact",
    "Off-Gassing ": "Off-Gassing"
}