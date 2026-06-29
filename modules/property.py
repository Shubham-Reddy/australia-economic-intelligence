import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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

def build_property_map(map_df, value_col):
    m = folium.Map(location=[-25.2744, 133.7751], zoom_start=3)
    for _, row in map_df.iterrows():
        city = row["City"]
        if city in CITY_COORDS:
            coords = CITY_COORDS[city]
            value = row[value_col]
            folium.CircleMarker(
                location=coords,
                radius=25,
                popup=f"{city}: ${value:,} median house price",
                tooltip=f"{city}: ${value:,}",
                color="#9B59B6",
                fill=True,
                fill_color="#9B59B6",
                fill_opacity=0.7
            ).add_to(m)
            folium.Marker(
                location=coords,
                icon=folium.DivIcon(
                    html=f'<div style="font-size:11px;color:white;font-weight:bold;background:#9B59B6;padding:4px 6px;border-radius:4px;white-space:nowrap">{city}<br>${value/1000000:.2f}M</div>'
                )
            ).add_to(m)
    return m

def show_property():
    st.title("🏡 Australian Property vs Rental Analysis")
    st.write("Buy vs rent comparison and property value analysis across Australian cities.")
    
    st.divider()
    
    property_data = {
        "City": ["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide"],
        "Median House Price": [1450000, 920000, 850000, 780000, 720000],
        "Median Unit Price": [850000, 620000, 580000, 520000, 480000],
        "Weekly Rent House": [850, 650, 620, 700, 550],
        "Weekly Rent Unit": [650, 480, 450, 500, 400],
        "Annual Price Growth %": [8.2, 6.5, 12.3, 15.1, 9.8],
        "Gross Rental Yield %": [3.1, 3.7, 3.9, 4.8, 4.2],
        "Years to Break Even": [28, 24, 22, 19, 21]
    }
    
    df = pd.DataFrame(property_data)
    
    cities = st.multiselect(
        "Select Cities",
        ["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide"],
        default=["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide"]
    )
    
    filtered_df = df[df["City"].isin(cities)]
    
    st.divider()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Most Expensive", "Sydney", "$1.45M median")
    with col2:
        st.metric("Best Yield", "Perth", "4.8% gross yield")
    with col3:
        st.metric("Fastest Growing", "Perth", "+15.1% YoY")
    with col4:
        st.metric("Best Break Even", "Perth", "19 years")
    
    st.divider()
    
    # Interactive map
    st.subheader("🗺️ Interactive Property Price Map")
    if not filtered_df.empty:
        property_map = build_property_map(filtered_df, "Median House Price")
        st_folium(property_map, width=700, height=500)
    
    st.divider()
    
    st.subheader("🏠 Median Property Prices by City")
    price_melted = filtered_df.melt(
        id_vars="City",
        value_vars=["Median House Price", "Median Unit Price"],
        var_name="Property Type",
        value_name="Median Price"
    )
    
    fig1 = px.bar(
        price_melted,
        x="City",
        y="Median Price",
        color="Property Type",
        barmode="group",
        title="Median Property Prices Across Australian Cities (AUD)",
        color_discrete_map={"Median House Price": "#FF4B4B", "Median Unit Price": "#0068C9"}
    )
    fig1.update_layout(height=400)
    st.plotly_chart(fig1, use_container_width=True)
    
    st.divider()
    
    st.subheader("📈 Gross Rental Yield by City")
    fig2 = px.bar(
        filtered_df,
        x="City",
        y="Gross Rental Yield %",
        color="City",
        title="Gross Rental Yield by City (%)",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig2.add_hline(
        y=4.0,
        line_dash="dash",
        line_color="yellow",
        annotation_text="Good yield threshold 4%"
    )
    fig2.update_layout(height=400)
    st.plotly_chart(fig2, use_container_width=True)
    
    st.divider()
    
    st.subheader("⏱️ Years to Break Even — Buy vs Rent")
    fig3 = px.bar(
        filtered_df,
        x="City",
        y="Years to Break Even",
        color="City",
        title="Years Until Buying Becomes Cheaper Than Renting",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig3.update_layout(height=400)
    st.plotly_chart(fig3, use_container_width=True)
    
    st.divider()
    
    st.subheader("📊 Annual Property Price Growth")
    fig4 = px.bar(
        filtered_df,
        x="City",
        y="Annual Price Growth %",
        color="City",
        title="Annual Property Price Growth by City (%)",
        color_discrete_sequence=px.colors.qualitative.Set1
    )
    fig4.update_layout(height=400)
    st.plotly_chart(fig4, use_container_width=True)
    
    st.divider()
    
    st.subheader("🧮 Buy vs Rent Calculator")
    
    col1, col2 = st.columns(2)
    with col1:
        selected_city = st.selectbox("Select City", cities)
        property_type = st.radio("Property Type", ["House", "Unit"])
    with col2:
        deposit_percent = st.slider("Deposit %", 10, 30, 20)
        interest_rate = st.slider("Interest Rate %", 4.0, 8.0, 6.0)
        years = st.slider("Investment Period (Years)", 5, 30, 10)
    
    city_row = df[df["City"] == selected_city].iloc[0]
    
    if property_type == "House":
        price = city_row["Median House Price"]
        weekly_rent = city_row["Weekly Rent House"]
    else:
        price = city_row["Median Unit Price"]
        weekly_rent = city_row["Weekly Rent Unit"]
    
    deposit = price * (deposit_percent / 100)
    loan = price - deposit
    monthly_rate = interest_rate / 100 / 12
    months = years * 12
    monthly_repayment = loan * (monthly_rate * (1 + monthly_rate)**months) / ((1 + monthly_rate)**months - 1)
    weekly_repayment = monthly_repayment * 12 / 52
    total_rent_paid = weekly_rent * 52 * years
    total_mortgage_paid = monthly_repayment * 12 * years
    future_value = price * (1 + city_row["Annual Price Growth %"] / 100) ** years
    equity_gained = future_value - price
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Weekly Mortgage", f"${weekly_repayment:,.0f}")
        st.metric("Weekly Rent", f"${weekly_rent:,.0f}")
    with col2:
        st.metric("Total Rent Paid", f"${total_rent_paid:,.0f}")
        st.metric("Total Mortgage Paid", f"${total_mortgage_paid:,.0f}")
    with col3:
        st.metric("Future Property Value", f"${future_value:,.0f}")
        st.metric("Equity Gained", f"${equity_gained:,.0f}")
    
    st.divider()
    
    st.subheader("📋 Full Property Data")
    st.dataframe(filtered_df, use_container_width=True)
    
    st.download_button(
        label="⬇️ Download Property Data as CSV",
        data=filtered_df.to_csv(index=False),
        file_name="australia_property_data.csv",
        mime="text/csv"
    )