import streamlit as st
from modules.data_fetcher import get_last_updated, get_live_economic_indicators

st.set_page_config(
    page_title="Australia Economic Intelligence Platform",
    page_icon="🇦🇺",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    /* Main background — deep navy gradient */
    .stApp {
        background: linear-gradient(135deg, #0a0e1a 0%, #0d1b2a 50%, #0a0e1a 100%);
        font-family: 'Segoe UI', sans-serif;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1b2a 0%, #1a2744 100%);
        border-right: 1px solid #1e3a5f;
    }
    
    /* Metric cards */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #0d1b2a 0%, #1a2744 100%);
        border: 1px solid #1e3a5f;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 4px 15px rgba(0, 100, 255, 0.1);
        transition: transform 0.2s;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 1.2rem !important;
        color: #00d4ff !important;
        font-weight: 700 !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.8rem !important;
        color: #8ab4d4 !important;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 0.75rem !important;
    }
    
    /* Headers — gradient text like your assignment */
    h1 {
        font-size: 1.8rem !important;
        background: linear-gradient(90deg, #00d4ff, #0068ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
        letter-spacing: -0.5px;
    }
    
    h2 {
        font-size: 1.3rem !important;
        color: #00d4ff !important;
        font-weight: 700 !important;
        border-left: 3px solid #00d4ff;
        padding-left: 10px;
    }
    
    h3 {
        font-size: 1.1rem !important;
        color: #8ab4d4 !important;
        font-weight: 600 !important;
    }
    
    /* Divider */
    hr {
        border: none !important;
        border-top: 1px solid #1e3a5f !important;
        margin: 1.5rem 0 !important;
    }
    
    /* Buttons */
    .stButton button {
        background: linear-gradient(90deg, #0068ff, #00d4ff);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.5rem 1rem;
        transition: opacity 0.2s;
    }
    
    .stButton button:hover {
        opacity: 0.9;
    }
    
    /* Download button */
    .stDownloadButton button {
        background: linear-gradient(90deg, #00cc88, #00d4ff);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
    }
    
    /* Selectbox */
    .stSelectbox > div {
        background: #0d1b2a !important;
        border: 1px solid #1e3a5f !important;
        border-radius: 8px !important;
        color: #c8d8e8 !important;
    }
    
    /* Multiselect */
    .stMultiSelect > div {
        background: #0d1b2a !important;
        border: 1px solid #1e3a5f !important;
        border-radius: 8px !important;
    }
    
    /* Radio */
    .stRadio > div {
        background: #0d1b2a;
        border-radius: 8px;
        padding: 8px;
        border: 1px solid #1e3a5f;
    }
    
    /* Dataframe */
    .stDataFrame {
        border: 1px solid #1e3a5f !important;
        border-radius: 8px !important;
    }
    
    /* Info success warning boxes */
    .stInfo {
        background: rgba(0, 100, 255, 0.1) !important;
        border: 1px solid #1e3a5f !important;
        border-radius: 8px !important;
        color: #c8d8e8 !important;
    }
    
    .stWarning {
        background: rgba(255, 140, 0, 0.1) !important;
        border: 1px solid #ff8c00 !important;
        border-radius: 8px !important;
    }
    
    .stSuccess {
        background: rgba(0, 204, 136, 0.1) !important;
        border: 1px solid #00cc88 !important;
        border-radius: 8px !important;
    }
    
    /* Caption */
    .stCaption, caption {
        color: #8ab4d4 !important;
        font-size: 0.8rem !important;
    }
    
    /* General text */
    p {
        color: #c8d8e8 !important;
        line-height: 1.6 !important;
    }
    
    /* Input */
    .stTextInput input {
        background: #0d1b2a !important;
        border: 1px solid #1e3a5f !important;
        border-radius: 8px !important;
        color: #c8d8e8 !important;
    }
    
    /* Slider */
    .stSlider > div {
        color: #00d4ff !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #0a0e1a; }
    ::-webkit-scrollbar-thumb { background: #1e3a5f; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #00d4ff; }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        background: #0d1b2a;
        border-radius: 8px;
        padding: 4px;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #8ab4d4;
        border-radius: 6px;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #0068ff, #00d4ff) !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# Fetch live indicators
with st.spinner("Fetching live economic data..."):
    indicators = get_live_economic_indicators()

# Header
st.markdown("# ![](https://flagcdn.com/w40/au.png) Australia Economic Intelligence Platform")
st.caption("AI Powered National Economic Dashboard — Real time insights across rental markets, job trends, cost of living, property analysis and AI economic advisory.")

st.divider()

# Live economic indicators
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("🏦 RBA Cash Rate", f"{indicators['interest_rate']}%", f"Effective {indicators['interest_rate_date']}")
with col2:
    st.metric("👷 Unemployment", f"{indicators['unemployment_rate']}%", "ABS Latest Release")
with col3:
    st.metric("📈 Inflation Rate", f"{indicators['inflation_rate']}%", "ABS CPI Latest")
with col4:
    st.metric("🏠 Rent Inflation", f"{indicators['rent_inflation']}%", "ABS CPI Latest")
with col5:
    st.metric("🕐 Last Updated", get_last_updated(), "Daily refresh")

st.divider()

# Sidebar navigation
module = st.sidebar.radio(
    "📌 Select Module",
    [
        "🏠 Rental Crisis Tracker",
        "💼 Job Market Intelligence",
        "💰 Cost of Living Index",
        "🏡 Property vs Rental Analysis",
        "🤖 AI Economic Advisor"
    ]
)

st.sidebar.divider()

# Data sources
st.sidebar.subheader("📊 Data Sources")
st.sidebar.caption("🏛️ ABS - Australian Bureau of Statistics")
st.sidebar.caption("🏠 CoreLogic - Rental & Property Data")
st.sidebar.caption("🔍 Domain.com.au - Property Listings")
st.sidebar.caption("💼 Seek & LinkedIn - Job Market Data")
st.sidebar.caption("💰 Numbeo - Cost of Living Index")
st.sidebar.caption("🏦 RBA - Interest Rate Data")
st.sidebar.caption("📅 Updated: " + get_last_updated())

st.sidebar.divider()

st.sidebar.subheader("ℹ️ Disclaimer")
st.sidebar.caption(
    "Data sourced from official Australian government and industry sources. "
    "Figures represent median values for capital cities. "
    "For informational purposes only. Not financial advice."
)

st.sidebar.divider()

st.sidebar.caption("**Built by Shubham Reddy**")
st.sidebar.caption("Master of Data Science — RMIT Melbourne")
st.sidebar.write("[LinkedIn](https://linkedin.com/in/shubham-reddy) | [GitHub](https://github.com/Shubham-Reddy)")

# Module routing
if module == "🏠 Rental Crisis Tracker":
    from modules.rental import show_rental
    show_rental()

elif module == "💼 Job Market Intelligence":
    from modules.jobs import show_jobs
    show_jobs()

elif module == "💰 Cost of Living Index":
    from modules.costliving import show_costliving
    show_costliving()

elif module == "🏡 Property vs Rental Analysis":
    from modules.property import show_property
    show_property()

elif module == "🤖 AI Economic Advisor":
    from modules.ai_advisor import show_advisor
    show_advisor()