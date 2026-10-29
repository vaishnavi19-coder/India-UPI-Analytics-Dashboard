import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from html import escape

st.set_page_config(page_title="India UPI Analytics", page_icon="🇮🇳", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
:root {color-scheme:dark;}
.stApp {background:radial-gradient(ellipse at 80% 0%,#10276a 0%,#061637 35%,#030c24 85%);color:#eef5ff;}
.block-container {padding-top:1.35rem;padding-bottom:2rem;max-width:1700px;}
[data-testid="stSidebar"] {background:linear-gradient(180deg,#05143b,#020b25)!important;border-right:1px solid #174dba;}
[data-testid="stSidebar"] .block-container {padding-top:1.3rem;}
[data-testid="stSidebar"] [role="radiogroup"] label {padding:10px;border-radius:11px;transition:background .2s;}
[data-testid="stSidebar"] [role="radiogroup"] label:hover {background:#132b6b;}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {background:linear-gradient(95deg,#0864d9,#4021bc);border:1px solid #3b8fff;box-shadow:0 0 15px #0a65df60;}
[data-testid="stSidebar"] hr {border-color:#20447c;}
h1,h2,h3 {color:#f5f8ff!important;}
[data-testid="stPlotlyChart"] {border:1px solid #1164cf;border-radius:15px;background:#061838;box-shadow:inset 0 0 20px #12377540,0 5px 20px #0006;padding:3px;overflow:hidden;}
[data-testid="stPlotlyChart"]:hover {border-color:#31b7ff;box-shadow:0 0 19px #067df544;}
[data-testid="stDataFrame"] {border:1px solid #1556a0;border-radius:12px;}
[data-testid="stMetric"] {background:#0a2250;border:1px solid #1556a0;border-radius:14px;padding:12px;}
.stDownloadButton button {background:linear-gradient(90deg,#0968e4,#4936c7);color:white;border:0;border-radius:10px;}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    data = pd.read_csv("data/upi_transactions_cleaned.csv")
    data["Date"] = pd.to_datetime(data["Date"])
    data["Year"] = data["Date"].dt.year
    for c in ["Transaction_Volume", "Transaction_Value", "Banks_Live", "Volume_MoM_Growth", "Volume_YoY_Growth"]:
        data[c] = pd.to_numeric(data[c], errors="coerce")
    return data.sort_values("Date").reset_index(drop=True)

try:
    df = load_data()
except (FileNotFoundError, KeyError, ValueError) as exc:
    st.error(f"Could not load data/upi_transactions_cleaned.csv: {exc}")
    st.stop()

st.sidebar.markdown("<h2 style='font-size:24px;margin:4px 0 24px'>🇮🇳 UPI Analytics</h2>", unsafe_allow_html=True)
st.sidebar.markdown("**Dashboard Navigation**")


# Hide Sidebar Radio Circles


# Hide Radio Buttons - Premium Sidebar

st.markdown("""
<style>
[data-testid="stSidebar"] [role="radiogroup"] [data-testid="stRadio"] {
    width: 100%;
}

[data-testid="stSidebar"] [role="radiogroup"] label input[type="radio"] {
    display: none !important;
}

[data-testid="stSidebar"] [role="radiogroup"] label > div:first-child {
    display: none !important;
}

[data-testid="stSidebar"] [role="radiogroup"] label {
    padding: 12px 14px !important;
    border-radius: 12px !important;
    width: 100%;
}

[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
    background: linear-gradient(90deg, #005eff, #4520c9) !important;
    border: 1px solid #38bdf8 !important;
    box-shadow: 0 0 15px rgba(0,94,255,0.4);
}
</style>
""", unsafe_allow_html=True)


# Vertical Sidebar Navigation Styling
st.markdown("""
<style>
[data-testid="stSidebar"] [data-testid="stPills"] [role="radiogroup"] {
    display: flex !important;
    flex-direction: column !important;
    align-items: stretch !important;
    gap: 8px !important;
}

[data-testid="stSidebar"] [data-testid="stPills"] button {
    width: 100% !important;
    justify-content: flex-start !important;
    text-align: left !important;
    border-radius: 12px !important;
    padding: 12px 16px !important;
    color: #e0eaff !important;
    background: transparent !important;
    border: 1px solid transparent !important;
}

[data-testid="stSidebar"] [data-testid="stPills"] button[aria-pressed="true"] {
    background: linear-gradient(90deg, #005eff, #4520c9) !important;
    border: 1px solid #38bdf8 !important;
    box-shadow: 0 0 15px rgba(0, 94, 255, 0.4) !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)


page = st.sidebar.pills(
    "Dashboard Navigation",
    options=[
        "Overview",
        "Transaction Trends",
        "Growth Analysis",
        "Banking Insights",
        "Explore Data"
    ],
    default="Overview",
    selection_mode="single",
    format_func=lambda x: {
        "Overview": "⌂  Overview",
        "Transaction Trends": "📈  Transaction Trends",
        "Growth Analysis": "▥  Growth Analysis",
        "Banking Insights": "🏛  Banking Insights",
        "Explore Data": "⚲  Explore Data"
    }[x],
    label_visibility="collapsed",
    width="stretch"
)

if page is None:
    page = "Overview"


st.sidebar.divider()
st.sidebar.markdown("**🗓️ Filter by Year**")
years = sorted(df["Year"].dropna().astype(int).unique().tolist())

# Premium Year Dropdown Styling

# Year Filter - Blue Purple Dropdown
st.markdown("""
<style>
section[data-testid="stSidebar"] div[data-testid="stSelectbox"] div[data-baseweb="select"] > div:first-child,
section[data-testid="stSidebar"] div[data-testid="stSelectbox"] div[data-baseweb="select"] > div:first-child > div {
    background: linear-gradient(90deg, #0756d8, #4520c9) !important;
    background-color: #0756d8 !important;
    border-color: #38bdf8 !important;
    border-radius: 12px !important;
}

section[data-testid="stSidebar"] div[data-testid="stSelectbox"] div[data-baseweb="select"] {
    border-radius: 12px !important;
    box-shadow: 0 0 12px rgba(0, 94, 255, 0.35) !important;
}
</style>
""", unsafe_allow_html=True)



year_filter = st.sidebar.selectbox(
    "Filter by Year",
    options=["All Years (2021 - 2026)"] + [str(y) for y in years],
    index=0,
    label_visibility="collapsed"
)

if year_filter == "All Years (2021 - 2026)":
    selected_years = years
else:
    selected_years = [int(year_filter)]

if not selected_years:
    selected_years = years
filtered = df[df["Year"].isin(selected_years)].copy()
st.sidebar.markdown("<p style='color:#8faad1;font-size:12px;margin-top:28px'>Data Period: Jan 2021 – Sep 2026<br>Python · Pandas · Plotly · Streamlit</p>", unsafe_allow_html=True)

st.markdown("""
<div style="background:linear-gradient(115deg,#063b9a,#06286c 50%,#3916a7);border:1px solid #3184ff;border-radius:20px;padding:23px 30px;margin-bottom:18px;box-shadow:0 0 24px #0957ff30;">
<div style="display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap;">
<div><div style="color:#2fe5ff;font-size:12px;letter-spacing:3px;font-weight:800">DIGITAL INDIA • FINTECH ANALYTICS</div>
<div style="font-size:37px;font-weight:800;color:white;margin-top:8px">India UPI Analytics</div>
<div style="color:#c8d9ff;font-size:15px;margin-top:5px">Exploring India's Digital Payment Revolution</div>
<div style="color:#3ee4ff;font-size:13px;margin-top:14px">▦ &nbsp; January 2021 – September 2026</div></div>
<div style="border:1px solid #21c8ff;background:#072967cc;box-shadow:0 0 15px #00aaff55;border-radius:15px;padding:15px 22px;text-align:center;">
<div style="color:#2ce5ff;font-size:12px;letter-spacing:1px">DATA COVERAGE</div><div style="color:white;font-weight:800;font-size:16px;margin:5px 0">JAN 2021 — SEP 2026</div>
<div style="color:#38edb6;font-size:12px">Historical UPI Insights</div></div></div></div>
""", unsafe_allow_html=True)

if filtered.empty:
    st.warning("No data for the selected years.")
    st.stop()

vol = filtered["Transaction_Volume"].sum() / 1e9
val = filtered["Transaction_Value"].sum() / 1e12
banks = int(filtered.iloc[-1]["Banks_Live"])
avg = filtered["Transaction_Value"].sum() / filtered["Transaction_Volume"].sum()
peak_yoy = filtered["Volume_YoY_Growth"].max()
latest_date = filtered["Date"].max().strftime("%b %Y")
yearly = filtered.groupby("Year", as_index=False).agg(volume=("Transaction_Volume", "sum"), value=("Transaction_Value", "sum"))
yearly["Volume (B)"] = yearly["volume"] / 1e9
yearly["Value (T)"] = yearly["value"] / 1e12
yearly["Avg Value"] = yearly["value"] / yearly["volume"]
yearly["Year"] = yearly["Year"].astype(str)
monthly = filtered.copy()
monthly["Volume (B)"] = monthly["Transaction_Volume"] / 1e9
monthly["Value (T)"] = monthly["Transaction_Value"] / 1e12


def theme(fig, height=300, legend=False):
    fig.update_layout(template="plotly_dark", height=height, paper_bgcolor="#061838", plot_bgcolor="#061838",
                      font=dict(color="#dceaff", size=11), title=dict(font=dict(size=14, color="white")),
                      margin=dict(l=12, r=12, t=55, b=22), showlegend=legend,
                      xaxis=dict(gridcolor="#163260", zerolinecolor="#163260"),
                      yaxis=dict(gridcolor="#163260", zerolinecolor="#163260"),
                      coloraxis_showscale=False)
    return fig


def chart(fig, height=300, legend=False):
    st.plotly_chart(theme(fig, height, legend), use_container_width=True, config={"displaylogo": False})


def kpi(icon, label, value, start, end, note=""):
    st.markdown(f"""<div style="background:linear-gradient(145deg,{start},{end});border:1px solid {start};
    border-radius:15px;min-height:155px;padding:15px 13px;box-shadow:0 0 13px {start}55;">
    <div style="font-size:23px">{icon}</div><div style="font-size:12px;color:#e9f4ff;margin-top:9px">{escape(label)}</div>
    <div style="font-size:clamp(15px,1.6vw,24px);font-weight:800;color:white;margin-top:7px;overflow-wrap:anywhere">{escape(value)}</div>
    <div style="font-size:10px;color:#c4f7ed;margin-top:5px">{escape(note)}</div></div>""", unsafe_allow_html=True)


def yearly_volume():
    fig = go.Figure()
    fig.add_bar(x=yearly["Year"], y=yearly["Volume (B)"], name="Volume (B)", marker_color="#1bb7ff")
    fig.add_bar(x=yearly["Year"], y=yearly["Value (T)"], name="Value (T)", marker_color="#9857ff")
    fig.update_layout(title="Yearly Transaction Volume & Value", barmode="group")
    chart(fig, 310, True)


def monthly_trend():
    fig = go.Figure()
    fig.add_scatter(x=monthly["Date"], y=monthly["Volume (B)"], mode="lines+markers", name="Volume (B)", line=dict(color="#20c9ff", width=2), marker=dict(size=4))
    fig.add_scatter(x=monthly["Date"], y=monthly["Value (T)"], mode="lines+markers", name="Value (T)", line=dict(color="#a855f7", width=2), marker=dict(size=4))
    fig.update_layout(title="Monthly Transaction Trend")
    chart(fig, 310, True)


def yearly_value():
    fig = px.bar(yearly, x="Year", y="Value (T)", title="Yearly Transaction Value", color_discrete_sequence=["#7656ff"], text_auto=".1f")
    fig.update_traces(textposition="outside")
    chart(fig, 310)


def bank_growth():
    data = filtered.groupby("Year", as_index=False).tail(1).sort_values("Date")
    fig = go.Figure(go.Scatter(x=data["Year"].astype(str), y=data["Banks_Live"], mode="lines+markers", line=dict(color="#2fe69c", width=3), fill="tozeroy", fillcolor="rgba(36,220,151,.22)"))
    fig.update_layout(title="Banks Live Growth")
    chart(fig, 265)


def average_value():
    fig = px.bar(yearly, x="Year", y="Avg Value", title="Avg. Transaction Value", color_discrete_sequence=["#ff9138"])
    chart(fig, 265)


def mom_growth():
    data = filtered.dropna(subset=["Volume_MoM_Growth"])
    fig = go.Figure(go.Bar(x=data["Date"], y=data["Volume_MoM_Growth"], marker_color=["#26e5a5" if v >= 0 else "#ff4668" for v in data["Volume_MoM_Growth"]]))
    fig.update_layout(title="MoM Growth (%)")
    chart(fig, 265)


def yoy_growth():
    data = filtered.dropna(subset=["Volume_YoY_Growth"])
    fig = go.Figure(go.Scatter(x=data["Date"], y=data["Volume_YoY_Growth"], mode="lines+markers", line=dict(color="#aa64ff", width=3), marker=dict(size=4)))
    fig.update_layout(title="YoY Growth (%)")
    chart(fig, 265)


if page == "Overview":
    kpis = [
        ("💳", "Total Volume", f"{vol:,.2f} B", "#1269ff", "#093c9c", "Selected years"),
        ("💰", "Total Value", f"₹{val:,.2f} T", "#00c8a0", "#06666e", "Selected years"),
        ("🏦", "Active Banks", f"{banks:,}", "#8c42ff", "#3e20a8", "Latest selected month"),
        ("📅", "Latest Data", latest_date, "#ff891d", "#9d381e", "Latest selected month"),
        ("₹", "Avg. Transaction Value", f"₹{avg:,.0f}", "#00a9e9", "#07539e", "Selected years"),
        ("📈", "Peak YoY Growth", f"{peak_yoy:+.1f}%" if pd.notna(peak_yoy) else "N/A", "#9c48ff", "#4c1aaf", "Highest observed")
    ]
    for col, values in zip(st.columns(6, gap="small"), kpis):
        with col:
            kpi(*values)
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    top = st.columns(3, gap="small")
    with top[0]: yearly_volume()
    with top[1]: monthly_trend()
    with top[2]: yearly_value()
    st.markdown("<h3 style='font-size:21px;margin:14px 0 12px'>Growth & Banking Insights</h3>", unsafe_allow_html=True)
    bottom = st.columns(4, gap="small")
    with bottom[0]: bank_growth()
    with bottom[1]: average_value()
    with bottom[2]: mom_growth()
    with bottom[3]: yoy_growth()
    st.caption("2026 covers January–September only. All KPIs and charts use the selected years. The yearly chart compares billion transactions with ₹ trillion on the same visual scale; read each legend unit separately.")
elif page == "Transaction Trends":
    st.subheader("Transaction Trends")
    a, b = st.columns(2)
    with a: yearly_volume()
    with b: monthly_trend()
    yearly_value()
    average_value()
elif page == "Growth Analysis":
    st.subheader("Growth Analysis")
    a, b = st.columns(2)
    with a: mom_growth()
    with b: yoy_growth()
    st.caption("Growth rates are from the original dataset; selecting a year does not recalculate earlier-period comparisons.")
elif page == "Banking Insights":
    st.subheader("Banking Insights")
    bank_growth()
    st.caption("Year-end bank counts are shown for complete years; 2026 uses September.")
else:
    st.subheader("Explore UPI Data")
    st.dataframe(filtered, use_container_width=True, hide_index=True)
    st.download_button("⬇ Download Filtered CSV", filtered.to_csv(index=False).encode("utf-8"), "upi_filtered_data.csv", "text/csv")

st.divider()
st.markdown("<p style='text-align:center;color:#8da8d0;font-size:12px'>INDIA UPI ANALYTICS &nbsp; | &nbsp; Python • Pandas • Plotly • Streamlit &nbsp; | &nbsp; Jan 2021 – Sep 2026</p>", unsafe_allow_html=True)
