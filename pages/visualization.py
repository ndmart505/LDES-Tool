import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from utils.config import CSV_URL, RANGE_METRICS, CATEGORICAL_FILTERS, TECH_CATEGORIES_VIZ

def render():
    st.title("Energy Storage Technologies Visualization")
    
    try:
        df = pd.read_csv(CSV_URL)
        
        st.sidebar.header("Visualization Filters")
        
        available_filters = []
        
        for metric_name, (low_col, high_col) in RANGE_METRICS.items():
            if low_col in df.columns and high_col in df.columns:
                available_filters.append(metric_name)
        
        single_value_columns = ["TRL", "ARL", "MRL"]
        for col in single_value_columns:
            if col in df.columns:
                available_filters.append(col)
        
        for col, display_name in CATEGORICAL_FILTERS.items():
            if col in df.columns:
                available_filters.append(display_name)
        
        filter_columns = st.sidebar.multiselect("Select data to filter by", options=available_filters)

        active_filter_ranges = {}

        filtered_df = df.copy()
        
        def extract_offgassing_bool(value):
            if pd.isna(value):
                return None
            value_str = str(value).strip()
            if value_str.startswith("Yes"):
                return "Yes"
            elif value_str.startswith("No"):
                return "No"
            return None
        
        categorical_filter_mapping = {
            "Geological Feature Requirement": "Geological Req.",
            "Historical Fire Events": "Fire Incidents",
            "Environmental Impact": "Environmental Impact",
            "Off-Gassing": "Off-Gassing "
        }
        
        for filter_col in filter_columns:
            if filter_col in categorical_filter_mapping:
                actual_col = categorical_filter_mapping[filter_col]
                
                if actual_col in df.columns:
                    if filter_col == "Off-Gassing":
                        unique_values = ["No", "Yes"]
                        selected_values = st.sidebar.pills(
                            f"Filter by {filter_col}",
                            options=unique_values,
                            default=unique_values,
                            selection_mode="multi",
                            key=f"filter_{actual_col}"
                        )
                        mask = filtered_df[actual_col].apply(
                            lambda x: extract_offgassing_bool(x) in selected_values if pd.notna(x) else False
                        )
                        filtered_df = filtered_df[mask]
                    elif filter_col == "Geological Feature Requirement":
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
                        unique_values = sorted(filtered_df[actual_col].dropna().unique())
                        selected_values = st.sidebar.pills(
                            f"Filter by {filter_col}",
                            options=unique_values,
                            default=unique_values,
                            selection_mode="multi",
                            key=f"filter_{actual_col}"
                        )
                        filtered_df = filtered_df[filtered_df[actual_col].isin(selected_values)]
            
            elif filter_col in RANGE_METRICS:
                low_col, high_col = RANGE_METRICS[filter_col]
                
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

        if "Technology Type" in df.columns:
            technology_types = df["Technology Type"].unique()
            selected_technology_types = []
            for tech_type in technology_types:
                if st.sidebar.checkbox(tech_type, value=True):
                    selected_technology_types.append(tech_type)
            filtered_df = filtered_df[
                filtered_df["Technology Type"].isin(selected_technology_types)
            ]

        if "Detailed Technology" in df.columns:
            all_selected_detailed = []
            
            for tech_type in selected_technology_types:
                if tech_type in TECH_CATEGORIES_VIZ:
                    st.sidebar.markdown(f"**{tech_type}**")
                    
                    available_techs = [t for t in TECH_CATEGORIES_VIZ[tech_type] if t in df["Detailed Technology"].unique()]
                    
                    if available_techs:
                        selected_techs = st.sidebar.pills(
                            f"{tech_type}_detailed",
                            options=available_techs,
                            default=available_techs,
                            selection_mode="multi",
                            label_visibility="collapsed"
                        )
                        all_selected_detailed.extend(selected_techs)
            
            if all_selected_detailed:
                filtered_df = filtered_df[
                    filtered_df["Detailed Technology"].isin(all_selected_detailed)
                ]
            else:
                filtered_df = filtered_df[filtered_df["Detailed Technology"].isin([])]

        def create_range_bar(df, x_col, y_low_col, y_high_col, title):
            if len(df) == 0:
                fig = go.Figure()
                fig.update_layout(title=title, xaxis_title=x_col)
                return fig
                
            fig = go.Figure()
            
            clip_range = None
            metric_name = None
            
            for metric, (low_col, high_col) in RANGE_METRICS.items():
                if low_col == y_low_col and high_col == y_high_col:
                    metric_name = metric
                    if metric in active_filter_ranges:
                        clip_range = active_filter_ranges[metric]
                    break
            
            for i, row in df.iterrows():
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
        
        def create_offgassing_chart(df):
            if len(df) == 0:
                fig = go.Figure()
                fig.update_layout(
                    title="Off-Gassing",
                    xaxis_title="Detailed Technology",
                    yaxis_title="Count"
                )
                return fig
            
            df_offgassing = df.copy()
            df_offgassing["Off-Gassing Display"] = df_offgassing["Off-Gassing "].apply(
                lambda x: "Yes" if pd.notna(x) and str(x).strip().startswith("Yes") else "No"
            )
            
            color_map = {"Yes": "#EF553B", "No": "#00CC96"}
            
            legend_added = set()
            
            fig = go.Figure()
            
            for i, row in df_offgassing.iterrows():
                offgassing_full = row.get("Off-Gassing ", "")
                offgassing_display = row["Off-Gassing Display"]
                
                hover_text = f"<b>{row['Detailed Technology']}</b><br><br>"
                hover_text += f"Off-Gassing: {offgassing_display}<br>"
                hover_text += f"Details: {offgassing_full}<br>"
                hover_text += "<extra></extra>"
                
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