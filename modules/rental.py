import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium
from sklearn.linear_model import LinearRegression
import numpy as np

# Full dataset — all cities both property types
RENTAL_DATA = {
    "City": ["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide",
             "Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide"],
    "Property Type": ["House", "House", "House", "House", "House",
                      "Unit", "Unit", "Unit", "Unit", "Unit"],
    "Median Weekly Rent": [850, 650, 620, 700, 550,
                           650, 480, 450, 500, 400],
    "Annual Change %": [8.2, 6.5, 12.3, 15.1, 9.8,
                        5.1, 4.2, 8.7, 11.2, 7.3],
    "Vacancy Rate %": [1.2, 1.8, 0.9, 0.7, 1.1,
                       1.5, 2.1, 1.0, 0.8, 1.3]
}

CITY_COORDS = {
    "Sydney": [-33.8688, 151.2093],
    "Melbourne": [-37.8136, 144.9631],
    "Brisbane": [-27.4698, 153.0251],
    "Perth": [-31.9505, 115.8605],
    "Adelaide": [-34.9285, 138.6007]
}

def build_map(map_df, value_col):
    m = folium.Map(location=[-25.2744, 133.7751], zoom_start=4)
    for _, row in map_df.iterrows():
        city = row["City"]
        if city in CITY_COORDS:
            coords = CITY_COORDS[city]
            value = row[value_col]
            folium.CircleMarker(
                location=coords,
                radius=25,
                popup=f"{city}: ${value}/wk",
                tooltip=f"{city}: ${value}/wk",
                color="#FF4B4B",
                fill=True,
                fill_color="#FF4B4B",
                fill_opacity=0.7
            ).add_to(m)
            folium.Marker(
                location=coords,
                icon=folium.DivIcon(
                    html=f'<div style="font-size:11px;color:white;font-weight:bold;background:#FF4B4B;padding:4px 6px;border-radius:4px;white-space:nowrap">{city}<br>${value}/wk</div>'
                )
            ).add_to(m)
    return m

def predict_rent(current_rent, growth_rate, months=6):
    X = np.array([0, 3, 6, 9, 12]).reshape(-1, 1)
    monthly_growth = growth_rate / 100 / 12
    y = np.array([current_rent * (1 + monthly_growth) ** i for i in range(5)])
    model = LinearRegression()
    model.fit(X, y)
    predicted = model.predict(np.array([[months]]))[0]
    return round(predicted, 0)

def show_suburb_search(df):
    st.subheader("🔍 Suburb Level Search")
    
    suburb_data = {
        "Suburb": [
            "CBD", "Fitzroy", "Richmond", "St Kilda", "Southbank",
            "Surry Hills", "Newtown", "Bondi", "Pyrmont", "Glebe",
            "South Brisbane", "New Farm", "Fortitude Valley", "West End", "Paddington",
            "Subiaco", "Fremantle", "Cottesloe", "Leederville", "Victoria Park",
            "Norwood", "Unley", "Glenelg", "Prospect", "Burnside"
        ],
        "City": [
            "Melbourne", "Melbourne", "Melbourne", "Melbourne", "Melbourne",
            "Sydney", "Sydney", "Sydney", "Sydney", "Sydney",
            "Brisbane", "Brisbane", "Brisbane", "Brisbane", "Brisbane",
            "Perth", "Perth", "Perth", "Perth", "Perth",
            "Adelaide", "Adelaide", "Adelaide", "Adelaide", "Adelaide"
        ],
        "Median Weekly Rent House": [
            650, 720, 680, 750, 680,
            900, 820, 1100, 850, 780,
            680, 720, 650, 630, 700,
            750, 680, 820, 700, 650,
            580, 620, 650, 560, 640
        ],
        "Median Weekly Rent Unit": [
            480, 520, 500, 550, 510,
            700, 620, 850, 650, 580,
            500, 530, 480, 460, 510,
            550, 500, 620, 520, 480,
            420, 450, 480, 410, 460
        ],
        "Affordability Score": [
            65, 70, 67, 73, 66,
            88, 80, 107, 83, 76,
            66, 70, 63, 61, 68,
            73, 66, 80, 68, 63,
            56, 60, 63, 54, 62
        ]
    }
    
    suburb_df = pd.DataFrame(suburb_data)
    
    col1, col2 = st.columns(2)
    with col1:
        selected_city = st.selectbox("Select City", ["All", "Melbourne", "Sydney", "Brisbane", "Perth", "Adelaide"])
    with col2:
        search = st.text_input("Search Suburb", placeholder="e.g. Fitzroy, Bondi...")
    
    filtered = suburb_df.copy()
    if selected_city != "All":
        filtered = filtered[filtered["City"] == selected_city]
    if search:
        filtered = filtered[filtered["Suburb"].str.contains(search, case=False)]
    
    if not filtered.empty:
        st.subheader("📊 Suburb Rental Comparison")
        
        fig = px.bar(
            filtered,
            x="Suburb",
            y=["Median Weekly Rent House", "Median Weekly Rent Unit"],
            barmode="group",
            title="Median Weekly Rent by Suburb",
            color_discrete_map={
                "Median Weekly Rent House": "#FF4B4B",
                "Median Weekly Rent Unit": "#0068C9"
            }
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("💸 Affordability Score by Suburb")
        st.caption("Affordability score = rent as % of average student income. Lower is better.")
        
        fig2 = px.bar(
            filtered,
            x="Suburb",
            y="Affordability Score",
            color="Affordability Score",
            color_continuous_scale="RdYlGn_r",
            title="Suburb Affordability Score (% of student income spent on rent)"
        )
        fig2.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Ideal: 30% of income")
        fig2.update_layout(height=400)
        st.plotly_chart(fig2, use_container_width=True)
        
        st.subheader("📋 Suburb Data Table")
        st.dataframe(filtered, use_container_width=True)
        
        st.download_button(
            label="⬇️ Download Suburb Data",
            data=filtered.to_csv(index=False),
            file_name="suburb_rental_data.csv",
            mime="text/csv"
        )
    else:
        st.info("No suburbs found. Try a different search.")

def show_rental():
    st.title("🏠 Australian Rental Crisis Tracker")
    st.write("Real time rental price analysis and ML powered predictions across major Australian cities.")
    st.divider()

    df = pd.DataFrame(RENTAL_DATA)

    # Filters
    cities = st.multiselect(
        "Select Cities",
        ["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide"],
        default=["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide"]
    )

    property_type = st.radio(
        "Property Type",
        ["House", "Unit", "Both"],
        horizontal=True
    )

    # Filter
    filtered_df = df[df["City"].isin(cities)]
    if property_type != "Both":
        filtered_df = filtered_df[filtered_df["Property Type"] == property_type]

    st.divider()

    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Highest Rent", "Sydney", "$850/wk")
    with col2:
        st.metric("Fastest Growing", "Perth", "+15.1% YoY")
    with col3:
        st.metric("Lowest Vacancy", "Perth", "0.7%")
    with col4:
        st.metric("Most Affordable", "Adelaide", "$550/wk")

    st.divider()

    # Interactive map — always uses House data for all selected cities
    st.subheader("🗺️ Interactive Australia Rental Map")
    map_df = df[df["City"].isin(cities) & (df["Property Type"] == "House")]
    if not map_df.empty:
        rental_map = build_map(map_df, "Median Weekly Rent")
        st_folium(rental_map, width=700, height=500)

    st.divider()

    # Median rent chart
    st.subheader("📊 Median Weekly Rent by City")
    fig1 = px.bar(
        filtered_df,
        x="City",
        y="Median Weekly Rent",
        color="Property Type",
        barmode="group",
        title="Median Weekly Rent Across Australian Cities (AUD)",
        color_discrete_map={"House": "#FF4B4B", "Unit": "#0068C9"}
    )
    fig1.update_layout(height=400)
    st.plotly_chart(fig1, use_container_width=True)

    st.divider()

    # Annual change chart
    st.subheader("📈 Annual Rental Price Change")
    fig2 = px.bar(
        filtered_df,
        x="City",
        y="Annual Change %",
        color="Property Type",
        barmode="group",
        title="Year on Year Rental Price Change (%)",
        color_discrete_map={"House": "#FF4B4B", "Unit": "#0068C9"}
    )
    fig2.add_hline(y=0, line_dash="dash", line_color="white")
    fig2.update_layout(height=400)
    st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    # Vacancy rate chart
    st.subheader("🏢 Rental Vacancy Rates")
    fig3 = px.bar(
        filtered_df,
        x="City",
        y="Vacancy Rate %",
        color="Property Type",
        barmode="group",
        title="Rental Vacancy Rates by City (%)",
        color_discrete_map={"House": "#FF4B4B", "Unit": "#0068C9"}
    )
    fig3.add_hline(
        y=3.0,
        line_dash="dash",
        line_color="yellow",
        annotation_text="Healthy vacancy rate 3%"
    )
    fig3.update_layout(height=400)
    st.plotly_chart(fig3, use_container_width=True)

    st.divider()

    # ML Prediction
    st.subheader("🤖 ML Powered Rent Prediction — Next 6 Months")
    st.write("Using Linear Regression to predict future rental prices based on current annual growth trends.")

    prediction_rows = []
    for _, row in filtered_df.iterrows():
        predicted = predict_rent(row["Median Weekly Rent"], row["Annual Change %"], months=6)
        prediction_rows.append({
            "City": row["City"],
            "Property Type": row["Property Type"],
            "Current Weekly Rent": f"${row['Median Weekly Rent']}",
            "Predicted Rent in 6 Months": f"${predicted:.0f}",
            "Predicted Weekly Increase": f"${predicted - row['Median Weekly Rent']:.0f}"
        })

    pred_df = pd.DataFrame(prediction_rows)

    fig5 = px.bar(
        filtered_df.assign(
            Predicted=filtered_df.apply(
                lambda r: predict_rent(r["Median Weekly Rent"], r["Annual Change %"]), axis=1
            )
        ).melt(
            id_vars=["City", "Property Type"],
            value_vars=["Median Weekly Rent", "Predicted"],
            var_name="Type",
            value_name="Weekly Rent"
        ),
        x="City",
        y="Weekly Rent",
        color="Type",
        barmode="group",
        facet_col="Property Type" if property_type == "Both" else None,
        title="Current vs ML Predicted Weekly Rent in 6 Months",
        color_discrete_map={
            "Median Weekly Rent": "#0068C9",
            "Predicted": "#FF4B4B"
        }
    )
    fig5.update_layout(height=400)
    st.plotly_chart(fig5, use_container_width=True)

    st.dataframe(pred_df, use_container_width=True)

    st.divider()

    # Affordability index
    st.subheader("💸 International Student Affordability Index")
    st.write("Based on average international student income of $800 to $1,200 per week.")

    aff_data = {
        "City": ["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide"],
        "Median Weekly Rent": [750, 565, 535, 600, 475],
        "% of Student Income": [75, 56, 54, 60, 48],
        "Affordability": ["Very Difficult", "Difficult", "Moderate", "Difficult", "Affordable"]
    }
    aff_df = pd.DataFrame(aff_data)
    aff_filtered = aff_df[aff_df["City"].isin(cities)]

    fig4 = px.bar(
        aff_filtered,
        x="City",
        y="% of Student Income",
        color="Affordability",
        title="Rental Cost as % of International Student Weekly Income",
        color_discrete_map={
            "Very Difficult": "#FF0000",
            "Difficult": "#FF8C00",
            "Moderate": "#FFD700",
            "Affordable": "#00CC44"
        }
    )
    fig4.add_hline(
        y=30,
        line_dash="dash",
        line_color="green",
        annotation_text="Recommended max 30% of income"
    )
    fig4.update_layout(height=400)
    st.plotly_chart(fig4, use_container_width=True)

    st.divider()

    # Raw data and download
    st.subheader("📋 Full Data Table")
    st.dataframe(filtered_df, use_container_width=True)
    st.divider()
    show_suburb_search(filtered_df)
    st.download_button(
        label="⬇️ Download Rental Data as CSV",
        data=filtered_df.to_csv(index=False),
        file_name="australia_rental_data.csv",
        mime="text/csv"
    )