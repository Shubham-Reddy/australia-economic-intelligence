import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium

def apply_dark_theme(fig, title="", source=""):
    fig.update_layout(
        plot_bgcolor="rgba(13, 27, 42, 0.8)",
        paper_bgcolor="rgba(13, 27, 42, 0)",
        font=dict(
            family="Segoe UI, sans-serif",
            color="#c8d8e8",
            size=12
        ),
        title=dict(
            text=title,
            font=dict(size=14, color="#00d4ff", family="Segoe UI"),
            x=0.02
        ),
        xaxis=dict(
            gridcolor="#1e3a5f",
            linecolor="#1e3a5f",
            tickcolor="#8ab4d4",
            tickfont=dict(color="#8ab4d4", size=11),
            title_font=dict(color="#8ab4d4")
        ),
        yaxis=dict(
            gridcolor="#1e3a5f",
            linecolor="#1e3a5f",
            tickcolor="#8ab4d4",
            tickfont=dict(color="#8ab4d4", size=11),
            title_font=dict(color="#8ab4d4")
        ),
        legend=dict(
            bgcolor="rgba(13, 27, 42, 0.9)",
            bordercolor="#1e3a5f",
            borderwidth=1,
            font=dict(color="#c8d8e8", size=11)
        ),
        margin=dict(l=40, r=40, t=60, b=80),
        annotations=[
            dict(
                text=f"Source: {source}" if source else "",
                xref="paper", yref="paper",
                x=0, y=-0.15,
                showarrow=False,
                font=dict(size=10, color="#8ab4d4"),
                align="left"
            )
        ] if source else [],
        height=420
    )
    return fig

CITY_COORDS = {
    "Sydney": [-33.8688, 151.2093],
    "Melbourne": [-37.8136, 144.9631],
    "Brisbane": [-27.4698, 153.0251],
    "Perth": [-31.9505, 115.8605],
    "Adelaide": [-34.9285, 138.6007]
}

def build_cost_map(map_df, value_col):
    m = folium.Map(location=[-25.2744, 133.7751], zoom_start=3)
    for _, row in map_df.iterrows():
        city = row["City"]
        if city in CITY_COORDS:
            coords = CITY_COORDS[city]
            value = row[value_col]
            folium.CircleMarker(
                location=coords,
                radius=25,
                popup=f"{city}: ${value}/week total",
                tooltip=f"{city}: ${value}/week",
                color="#FF8C00",
                fill=True,
                fill_color="#FF8C00",
                fill_opacity=0.7
            ).add_to(m)
            folium.Marker(
                location=coords,
                icon=folium.DivIcon(
                    html=f'<div style="font-size:11px;color:white;font-weight:bold;background:#FF8C00;padding:4px 6px;border-radius:4px;white-space:nowrap">{city}<br>${value}/wk</div>'
                )
            ).add_to(m)
    return m

def show_costliving():
    st.title("💰 Australian Cost of Living Index")
    st.write("Comprehensive cost of living analysis across major Australian cities.")
    
    st.divider()
    
    cost_data = {
        "City": ["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide"],
        "Weekly Rent": [750, 565, 535, 600, 475],
        "Weekly Groceries": [120, 110, 105, 115, 100],
        "Weekly Transport": [50, 45, 40, 35, 38],
        "Weekly Utilities": [45, 40, 38, 42, 35],
        "Weekly Entertainment": [80, 70, 65, 68, 60],
        "Weekly Total": [1045, 830, 783, 860, 708],
        "International Student Weekly Income": [900, 900, 900, 900, 900]
    }
    
    df = pd.DataFrame(cost_data)
    
    cities = st.multiselect(
        "Select Cities to Compare",
        ["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide"],
        default=["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide"]
    )
    
    filtered_df = df[df["City"].isin(cities)]
    
    st.divider()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Most Expensive", "Sydney", "$1,045/week")
    with col2:
        st.metric("Most Affordable", "Adelaide", "$708/week")
    with col3:
        st.metric("Best Value", "Brisbane", "$783/week")
    with col4:
        st.metric("Student Savings", "Adelaide", "+$192/week")
    
    st.divider()
    
    # Interactive map
    st.subheader("🗺️ Interactive Cost of Living Map")
    if not filtered_df.empty:
        cost_map = build_cost_map(filtered_df, "Weekly Total")
        st_folium(cost_map, width=700, height=500)
    
    st.divider()
    
    st.subheader("📊 Total Weekly Cost of Living by City")
    fig1 = px.bar(
        filtered_df,
        x="City",
        y="Weekly Total",
        color="City",
        title="Total Weekly Cost of Living (AUD)",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig1.add_hline(
        y=900,
        line_dash="dash",
        line_color="yellow",
        annotation_text="Average student weekly income $900"
    )
    fig1.update_layout(height=400)
    st.plotly_chart(fig1, use_container_width=True)
    
    st.divider()
    
    st.subheader("🥧 Cost Breakdown by Category")
    selected_city = st.selectbox("Select City for Breakdown", cities)
    city_data = filtered_df[filtered_df["City"] == selected_city].iloc[0]
    
    breakdown_data = {
        "Category": ["Rent", "Groceries", "Transport", "Utilities", "Entertainment"],
        "Weekly Cost": [
            city_data["Weekly Rent"],
            city_data["Weekly Groceries"],
            city_data["Weekly Transport"],
            city_data["Weekly Utilities"],
            city_data["Weekly Entertainment"]
        ]
    }
    
    breakdown_df = pd.DataFrame(breakdown_data)
    
    fig2 = px.pie(
        breakdown_df,
        values="Weekly Cost",
        names="Category",
        title=f"Cost of Living Breakdown — {selected_city}",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig2.update_layout(height=400)
    st.plotly_chart(fig2, use_container_width=True)
    
    st.divider()
    
    st.subheader("📈 Cost Breakdown Comparison Across Cities")
    melted_df = filtered_df.melt(
        id_vars="City",
        value_vars=["Weekly Rent", "Weekly Groceries", "Weekly Transport", "Weekly Utilities", "Weekly Entertainment"],
        var_name="Category",
        value_name="Weekly Cost"
    )
    
    fig3 = px.bar(
        melted_df,
        x="City",
        y="Weekly Cost",
        color="Category",
        title="Weekly Cost Breakdown by City (AUD)",
        barmode="stack"
    )
    fig3.update_layout(height=400)
    st.plotly_chart(fig3, use_container_width=True)
    
    st.divider()
    
    st.subheader("🎓 International Student Affordability Index")
    filtered_df = filtered_df.copy()
    filtered_df["Surplus/Deficit"] = filtered_df["International Student Weekly Income"] - filtered_df["Weekly Total"]
    filtered_df["Affordability"] = filtered_df["Surplus/Deficit"].apply(
        lambda x: "Surplus" if x > 0 else "Deficit"
    )
    
    fig4 = px.bar(
        filtered_df,
        x="City",
        y="Surplus/Deficit",
        color="Affordability",
        title="Weekly Surplus or Deficit for International Students (AUD)",
        color_discrete_map={"Surplus": "#00CC44", "Deficit": "#FF4B4B"}
    )
    fig4.add_hline(y=0, line_dash="dash", line_color="white")
    fig4.update_layout(height=400)
    st.plotly_chart(fig4, use_container_width=True)
    
    st.divider()
    
    st.subheader("📋 Full Cost of Living Data")
    st.dataframe(filtered_df, use_container_width=True)
    
    st.download_button(
        label="⬇️ Download Cost of Living Data as CSV",
        data=filtered_df.to_csv(index=False),
        file_name="australia_cost_of_living.csv",
        mime="text/csv"
    )