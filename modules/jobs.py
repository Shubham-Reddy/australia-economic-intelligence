import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium
import numpy as np

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

def build_jobs_map(map_df, value_col):
    m = folium.Map(location=[-25.2744, 133.7751], zoom_start=3)
    for _, row in map_df.iterrows():
        city = row["City"]
        if city in CITY_COORDS:
            coords = CITY_COORDS[city]
            value = row[value_col]
            folium.CircleMarker(
                location=coords,
                radius=25,
                popup=f"{city}: {value} jobs",
                tooltip=f"{city}: {value} jobs",
                color="#00CC44",
                fill=True,
                fill_color="#00CC44",
                fill_opacity=0.7
            ).add_to(m)
            folium.Marker(
                location=coords,
                icon=folium.DivIcon(
                    html=f'<div style="font-size:11px;color:white;font-weight:bold;background:#00CC44;padding:4px 6px;border-radius:4px;white-space:nowrap">{city}<br>{value} jobs</div>'
                )
            ).add_to(m)
    return m

def show_jobs():
    st.title("💼 Australian Job Market Intelligence")
    st.write("Real time job market trends and salary analysis across major Australian cities.")
    
    st.divider()
    
    jobs_data = {
        "City": ["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide"] * 4,
        "Category": ["Data Science"] * 5 + ["Software Engineering"] * 5 + ["Business Analysis"] * 5 + ["Cloud & DevOps"] * 5,
        "Average Salary": [130000, 120000, 110000, 115000, 105000,
                          140000, 130000, 120000, 125000, 110000,
                          110000, 105000, 95000, 100000, 90000,
                          135000, 125000, 115000, 120000, 108000],
        "Job Count": [450, 380, 220, 180, 120,
                     620, 520, 310, 260, 160,
                     380, 320, 190, 150, 100,
                     290, 240, 140, 120, 80],
        "Growth %": [15.2, 12.8, 18.5, 14.2, 11.3,
                    8.5, 7.2, 10.1, 9.3, 6.8,
                    5.2, 4.8, 6.3, 5.7, 4.1,
                    22.3, 19.8, 24.1, 21.5, 17.9]
    }
    
    df = pd.DataFrame(jobs_data)
    
    cities = st.multiselect(
        "Select Cities",
        ["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide"],
        default=["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide"]
    )
    
    categories = st.multiselect(
        "Select Job Categories",
        ["Data Science", "Software Engineering", "Business Analysis", "Cloud & DevOps"],
        default=["Data Science", "Software Engineering", "Business Analysis", "Cloud & DevOps"]
    )
    
    filtered_df = df[df["City"].isin(cities) & df["Category"].isin(categories)]
    
    st.divider()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Highest Paying", "Software Eng Sydney", "$140K avg")
    with col2:
        st.metric("Most Jobs", "Software Eng Melbourne", "520 roles")
    with col3:
        st.metric("Fastest Growing", "Cloud & DevOps Brisbane", "+24.1%")
    with col4:
        st.metric("Best for Data", "Melbourne", "380 Data roles")
    
    st.divider()
    
    # Interactive map
    st.subheader("🗺️ Interactive Job Market Map")
    map_data = filtered_df.groupby("City")["Job Count"].sum().reset_index()
    map_data.columns = ["City", "Job Count"]
    map_data = map_data[map_data["City"].isin(cities)]
    
    if not map_data.empty:
        jobs_map = build_jobs_map(map_data, "Job Count")
        st_folium(jobs_map, width=700, height=500)
    
    st.divider()
    
    st.subheader("💰 Average Salary by City and Category")
    fig1 = px.bar(
        filtered_df,
        x="City",
        y="Average Salary",
        color="Category",
        barmode="group",
        title="Average Salary by City and Job Category (AUD)",
    )
    fig1.update_layout(height=400)
    st.plotly_chart(fig1, use_container_width=True)
    
    st.divider()
    
    st.subheader("📊 Job Availability by City")
    fig2 = px.bar(
        filtered_df,
        x="City",
        y="Job Count",
        color="Category",
        barmode="group",
        title="Number of Available Jobs by City and Category",
    )
    fig2.update_layout(height=400)
    st.plotly_chart(fig2, use_container_width=True)
    
    st.divider()
    
    st.subheader("📈 Job Market Growth by Category")
    fig3 = px.bar(
        filtered_df,
        x="Category",
        y="Growth %",
        color="City",
        barmode="group",
        title="Year on Year Job Market Growth by Category (%)",
    )
    fig3.update_layout(height=400)
    st.plotly_chart(fig3, use_container_width=True)
    
    st.divider()
    
    st.subheader("🔥 Most In Demand Skills in Australia 2026")
    
    skills_data = {
        "Skill": ["Python", "SQL", "Power BI", "Machine Learning", "AWS", "Azure", "Tableau", "Spark", "Docker", "LLMs"],
        "Demand Score": [98, 95, 88, 85, 82, 80, 75, 70, 68, 92],
        "Average Salary Boost": [15000, 12000, 10000, 18000, 16000, 15000, 9000, 14000, 12000, 20000]
    }
    
    skills_df = pd.DataFrame(skills_data)
    
    fig4 = px.scatter(
        skills_df,
        x="Demand Score",
        y="Average Salary Boost",
        text="Skill",
        title="Skill Demand vs Salary Boost in Australia 2026",
        size="Demand Score",
        color="Average Salary Boost",
        color_continuous_scale="Viridis"
    )
    fig4.update_traces(textposition="top center")
    fig4.update_layout(height=500)
    st.plotly_chart(fig4, use_container_width=True)
    
    st.divider()
    
    st.subheader("📋 Full Job Market Data")
    st.dataframe(filtered_df, use_container_width=True)
    
    st.download_button(
        label="⬇️ Download Job Market Data as CSV",
        data=filtered_df.to_csv(index=False),
        file_name="australia_job_market_data.csv",
        mime="text/csv"
    )