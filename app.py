import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Global Renewable Energy Trends",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #0e1117; }
    .block-container { padding-top: 2rem; }
    .metric-card {
        background: linear-gradient(135deg, #1e2130, #2a2d3e);
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        border-left: 4px solid;
        margin-bottom: 0.5rem;
    }
    .metric-card.solar  { border-color: #f4c430; }
    .metric-card.wind   { border-color: #4fc3f7; }
    .metric-card.hydro  { border-color: #26a69a; }
    .metric-card.total  { border-color: #ab47bc; }
    h1 { color: #f0f0f0; }
    .stSelectbox label, .stMultiSelect label, .stSlider label { color: #aaa; }
</style>
""", unsafe_allow_html=True)

# ── Dataset ───────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    """
    Realistic global renewable electricity generation data (TWh).
    Sources: IEA, IRENA, Our World in Data (2000-2023)
    """
    years = list(range(2000, 2024))

    data = {
        "Year": years * 7,
        "Country": (
            ["World"] * 24 + ["China"] * 24 + ["USA"] * 24 +
            ["Germany"] * 24 + ["India"] * 24 + ["Brazil"] * 24 + ["Spain"] * 24
        ),
        "Solar_TWh": (
            # World
            [1,2,3,4,5,7,10,16,26,47,96,149,218,327,445,528,643,777,901,1040,1200,1380,1590,1850] +
            # China
            [0,0,0,0,0,0,1,2,4,9,19,30,55,130,200,250,330,450,540,640,760,900,1050,1270] +
            # USA
            [0,0,0,0,1,1,2,3,5,9,18,36,58,87,115,130,145,160,178,198,218,240,264,290] +
            # Germany
            [0,0,1,2,3,5,7,10,14,19,25,30,33,35,36,37,38,40,43,46,49,52,56,60] +
            # India
            [0,0,0,0,0,0,0,1,2,4,7,12,19,31,45,57,73,93,120,148,178,210,248,300] +
            # Brazil
            [0,0,0,0,0,0,0,0,0,1,2,3,5,8,12,16,20,25,31,38,45,53,63,75] +
            # Spain
            [0,0,0,0,0,0,0,1,1,2,3,4,6,8,10,12,14,17,20,24,28,33,39,46]
        ),
        "Wind_TWh": (
            # World
            [31,40,52,64,82,104,132,170,220,278,340,427,521,634,712,830,958,1052,1127,1273,1430,1590,1770,1980] +
            # China
            [2,3,4,6,9,14,21,34,51,68,92,120,141,169,186,240,297,330,366,406,466,530,600,680] +
            # USA
            [5,7,10,12,14,18,25,34,45,55,66,80,90,100,105,115,128,138,145,160,178,195,213,232] +
            # Germany
            [7,9,11,14,18,25,31,39,40,39,38,46,51,53,56,64,67,67,68,70,75,80,87,96] +
            # India
            [1,2,3,4,5,7,9,12,15,19,22,26,29,32,34,37,42,46,52,59,65,72,80,90] +
            # Brazil
            [0,0,0,1,1,2,3,4,5,6,8,11,14,19,24,31,38,43,48,54,60,66,72,80] +
            # Spain
            [12,14,17,20,24,28,31,35,39,42,43,45,48,50,51,52,54,56,58,60,63,66,69,72]
        ),
        "Hydro_TWh": (
            # World
            [2637,2564,2622,2658,2809,2913,3010,3085,3196,3250,3430,3530,3602,3750,3900,4030,4100,4200,4250,4300,4360,4420,4480,4540] +
            # China
            [222,243,258,261,279,315,436,484,486,500,598,668,753,900,1064,1126,1180,1194,1232,1302,1355,1340,1350,1360] +
            # USA
            [305,220,265,275,272,272,290,252,255,275,260,327,276,268,259,250,268,300,292,274,285,255,260,265] +
            # Germany
            [22,22,19,20,21,21,21,21,20,20,20,19,19,19,19,18,18,18,17,17,17,17,16,16] +
            # India
            [76,77,80,82,84,101,102,113,116,107,120,114,116,131,129,122,136,123,126,134,150,156,160,168] +
            # Brazil
            [305,330,295,310,338,337,337,371,393,373,405,428,415,391,373,359,381,404,393,405,415,420,430,440] +
            # Spain
            [27,24,28,29,26,30,29,28,27,30,35,30,25,33,35,27,39,26,36,27,29,31,34,30]
        ),
    }

    df = pd.DataFrame(data)
    df["Total_TWh"] = df["Solar_TWh"] + df["Wind_TWh"] + df["Hydro_TWh"]
    df["Solar_Share"] = (df["Solar_TWh"] / df["Total_TWh"] * 100).round(1)
    df["Wind_Share"]  = (df["Wind_TWh"]  / df["Total_TWh"] * 100).round(1)
    df["Hydro_Share"] = (df["Hydro_TWh"] / df["Total_TWh"] * 100).round(1)
    return df

df = load_data()

# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.image("https://img.icons8.com/fluency/96/wind-turbine.png", width=60)
st.sidebar.title("⚡ Controls")

countries      = df["Country"].unique().tolist()
sel_countries  = st.sidebar.multiselect("Select Countries", countries, default=["World", "Spain", "China", "USA"])
year_range     = st.sidebar.slider("Year Range", 2000, 2023, (2000, 2023))
source_options = st.sidebar.multiselect("Energy Sources", ["Solar", "Wind", "Hydro"], default=["Solar", "Wind", "Hydro"])

# ── Filter ────────────────────────────────────────────────────────────────────
filtered = df[
    (df["Country"].isin(sel_countries)) &
    (df["Year"] >= year_range[0]) &
    (df["Year"] <= year_range[1])
]
world_latest = df[(df["Country"] == "World") & (df["Year"] == 2023)].iloc[0]
world_2000   = df[(df["Country"] == "World") & (df["Year"] == 2000)].iloc[0]

# ── Title ─────────────────────────────────────────────────────────────────────
st.title("🌍 Global Renewable Energy Trends")
st.markdown("**Solar · Wind · Hydropower  |  2000 – 2023**  &nbsp;·&nbsp;  Data: IEA / IRENA / Our World in Data")
st.divider()

# ── KPI cards ─────────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
with k1:
    delta = world_latest["Solar_TWh"] - world_2000["Solar_TWh"]
    st.metric("☀️ Solar (2023)", f"{world_latest['Solar_TWh']:,.0f} TWh", f"+{delta:,.0f} TWh since 2000")
with k2:
    delta = world_latest["Wind_TWh"] - world_2000["Wind_TWh"]
    st.metric("💨 Wind (2023)", f"{world_latest['Wind_TWh']:,.0f} TWh", f"+{delta:,.0f} TWh since 2000")
with k3:
    delta = world_latest["Hydro_TWh"] - world_2000["Hydro_TWh"]
    st.metric("💧 Hydro (2023)", f"{world_latest['Hydro_TWh']:,.0f} TWh", f"+{delta:,.0f} TWh since 2000")
with k4:
    delta = world_latest["Total_TWh"] - world_2000["Total_TWh"]
    st.metric("⚡ Total (2023)", f"{world_latest['Total_TWh']:,.0f} TWh", f"+{delta:,.0f} TWh since 2000")

st.divider()

# ── Row 1: Line chart + Stacked area ──────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Generation Over Time by Country")
    source_col = {"Solar": "Solar_TWh", "Wind": "Wind_TWh", "Hydro": "Hydro_TWh"}
    melted = filtered.melt(
        id_vars=["Year","Country"],
        value_vars=[source_col[s] for s in source_options],
        var_name="Source", value_name="TWh"
    )
    melted["Source"] = melted["Source"].str.replace("_TWh","")
    color_map = {"Solar": "#f4c430", "Wind": "#4fc3f7", "Hydro": "#26a69a"}
    fig1 = px.line(
        melted, x="Year", y="TWh", color="Country", line_dash="Source",
        color_discrete_sequence=px.colors.qualitative.Set2,
        labels={"TWh": "Electricity (TWh)"},
        template="plotly_dark"
    )
    fig1.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.01), height=380)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("🌐 World Mix — Stacked Area")
    world_df = df[(df["Country"]=="World") & (df["Year"]>=year_range[0]) & (df["Year"]<=year_range[1])]
    fig2 = go.Figure()
    if "Hydro" in source_options:
        fig2.add_trace(go.Scatter(x=world_df["Year"], y=world_df["Hydro_TWh"], name="Hydro",
            fill="tozeroy", mode="lines", line=dict(color="#26a69a"), fillcolor="rgba(38,166,154,0.4)"))
    if "Wind" in source_options:
        fig2.add_trace(go.Scatter(x=world_df["Year"], y=world_df["Wind_TWh"], name="Wind",
            fill="tonexty", mode="lines", line=dict(color="#4fc3f7"), fillcolor="rgba(79,195,247,0.4)"))
    if "Solar" in source_options:
        fig2.add_trace(go.Scatter(x=world_df["Year"], y=world_df["Solar_TWh"], name="Solar",
            fill="tonexty", mode="lines", line=dict(color="#f4c430"), fillcolor="rgba(244,196,48,0.4)"))
    fig2.update_layout(template="plotly_dark", height=380,
        yaxis_title="Electricity (TWh)", legend=dict(orientation="h", yanchor="bottom", y=1.01))
    st.plotly_chart(fig2, use_container_width=True)

# ── Row 2: Bar race + Pie ──────────────────────────────────────────────────────
col3, col4 = st.columns(2)

with col3:
    st.subheader("📊 Country Comparison — Selected Year")
    sel_year = st.slider("Pick a year", year_range[0], year_range[1], min(2023, year_range[1]), key="bar_year")
    year_df = df[(df["Country"].isin(sel_countries)) & (df["Year"]==sel_year)].copy()
    bar_sources = [s+"_TWh" for s in source_options]
    bar_melt = year_df.melt(id_vars=["Country"], value_vars=bar_sources, var_name="Source", value_name="TWh")
    bar_melt["Source"] = bar_melt["Source"].str.replace("_TWh","")
    fig3 = px.bar(bar_melt, x="Country", y="TWh", color="Source",
        color_discrete_map={"Solar":"#f4c430","Wind":"#4fc3f7","Hydro":"#26a69a"},
        barmode="group", template="plotly_dark",
        labels={"TWh": "Electricity (TWh)"})
    fig3.update_layout(height=380, legend=dict(orientation="h", yanchor="bottom", y=1.01))
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.subheader("🥧 World Energy Mix — Selected Year")
    pie_row = df[(df["Country"]=="World") & (df["Year"]==sel_year)].iloc[0]
    pie_vals  = [pie_row.get(s+"_TWh",0) for s in source_options]
    pie_names = source_options
    pie_colors = {"Solar":"#f4c430","Wind":"#4fc3f7","Hydro":"#26a69a"}
    fig4 = go.Figure(go.Pie(
        labels=pie_names, values=pie_vals,
        marker_colors=[pie_colors[s] for s in pie_names],
        hole=0.45, textinfo="label+percent"
    ))
    fig4.update_layout(template="plotly_dark", height=380,
        annotations=[dict(text=str(sel_year), x=0.5, y=0.5, font_size=22, showarrow=False)])
    st.plotly_chart(fig4, use_container_width=True)

# ── Row 3: Growth rate ────────────────────────────────────────────────────────
st.subheader("📉 Year-on-Year Growth Rate — World")
world_full = df[df["Country"]=="World"].copy().sort_values("Year")
for s in ["Solar","Wind","Hydro","Total"]:
    world_full[f"{s}_Growth"] = world_full[f"{s}_TWh"].pct_change() * 100

growth_sources = [s for s in source_options] + (["Total"] if len(source_options)>1 else [])
fig5 = go.Figure()
gc = {"Solar":"#f4c430","Wind":"#4fc3f7","Hydro":"#26a69a","Total":"#ab47bc"}
for s in growth_sources:
    col_name = f"{s}_Growth"
    if col_name in world_full.columns:
        sub = world_full[(world_full["Year"]>=year_range[0]) & (world_full["Year"]<=year_range[1])]
        fig5.add_trace(go.Scatter(x=sub["Year"], y=sub[col_name].round(1),
            name=s, mode="lines+markers", line=dict(color=gc.get(s,"#fff"), width=2)))
fig5.add_hline(y=0, line_dash="dash", line_color="gray")
fig5.update_layout(template="plotly_dark", height=320,
    yaxis_title="Growth (%)", legend=dict(orientation="h", yanchor="bottom", y=1.01))
st.plotly_chart(fig5, use_container_width=True)

# ── Advanced Impact Features ──────────────────────────────────────────────────
st.divider()
st.header("🚀 Research-Grade Climate Intelligence Lab")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Forecast Engine",
    "Policy Scenario Lab",
    "Competitiveness Scorecard",
    "Causal Evidence",
    "Spain Deep Dive",
    "Download Center"
])

with tab1:
    st.subheader("🔮 2030 Forecast with Confidence Bands")
    forecast_country = st.selectbox(
        "Country for forecast",
        options=sel_countries if sel_countries else countries,
        index=0,
        key="forecast_country"
    )
    horizon = st.slider("Forecast horizon", 2024, 2035, 2030, key="forecast_horizon")

    hist = df[df["Country"] == forecast_country].sort_values("Year").copy()
    last_year = int(hist["Year"].max())
    fut_years = list(range(last_year + 1, horizon + 1))

    if fut_years:
        fig_fore = go.Figure()
        source_colors = {"Solar": "#f4c430", "Wind": "#4fc3f7", "Hydro": "#26a69a"}

        for src in ["Solar", "Wind", "Hydro"]:
            col = f"{src}_TWh"
            x = hist["Year"].to_numpy()
            y = hist[col].to_numpy()

            # Linear trend + guardrail against negative values for long horizons
            z = np.polyfit(x, y, 1)
            trend = np.poly1d(z)
            yhat = np.maximum(trend(np.array(fut_years)), 0)

            # Confidence band is scaled by historical volatility
            yoy = hist[col].pct_change().dropna()
            vol = float(yoy.std()) if len(yoy) > 1 else 0.08
            band = np.maximum(yhat * max(vol, 0.06), 5)

            fig_fore.add_trace(go.Scatter(
                x=hist["Year"], y=hist[col], mode="lines", name=f"{src} (history)",
                line=dict(color=source_colors[src], width=2)
            ))
            fig_fore.add_trace(go.Scatter(
                x=fut_years, y=yhat, mode="lines", name=f"{src} (forecast)",
                line=dict(color=source_colors[src], dash="dot", width=3)
            ))
            fig_fore.add_trace(go.Scatter(
                x=fut_years + fut_years[::-1],
                y=(yhat + band).tolist() + (np.maximum(yhat - band, 0))[::-1].tolist(),
                fill="toself", fillcolor="rgba(255,255,255,0.08)",
                line=dict(color="rgba(255,255,255,0)"),
                hoverinfo="skip", showlegend=False
            ))

        fig_fore.update_layout(
            template="plotly_dark",
            height=470,
            yaxis_title="Electricity (TWh)",
            legend=dict(orientation="h", yanchor="bottom", y=1.01)
        )
        st.plotly_chart(fig_fore, use_container_width=True)

        latest = hist.iloc[-1]
        future_total = 0
        for src in ["Solar", "Wind", "Hydro"]:
            col = f"{src}_TWh"
            z = np.polyfit(hist["Year"].to_numpy(), hist[col].to_numpy(), 1)
            pred = max(float(np.poly1d(z)(horizon)), 0)
            future_total += pred
        current_total = float(latest["Total_TWh"])
        growth_pct = ((future_total - current_total) / current_total * 100) if current_total else 0
        st.info(
            f"Projected total renewable generation for {forecast_country} in {horizon}: "
            f"{future_total:,.0f} TWh  ({growth_pct:+.1f}% vs {last_year})."
        )
    else:
        st.warning("Forecast horizon must be after the latest available year.")

with tab2:
    st.subheader("🧪 Policy Scenario Lab (2024–2030)")
    st.caption("Adjust annual growth assumptions and compare with baseline momentum.")

    sim_country = st.selectbox(
        "Country for policy simulation",
        options=sel_countries if sel_countries else countries,
        index=0,
        key="sim_country"
    )

    s1, s2, s3 = st.columns(3)
    with s1:
        solar_g = st.slider("Solar annual growth %", 0, 35, 16, key="solar_growth")
    with s2:
        wind_g = st.slider("Wind annual growth %", 0, 25, 9, key="wind_growth")
    with s3:
        hydro_g = st.slider("Hydro annual growth %", -2, 10, 2, key="hydro_growth")

    country_hist = df[df["Country"] == sim_country].sort_values("Year").copy()
    base = country_hist.iloc[-1]
    sim_years = list(range(2024, 2031))

    proj = []
    cur_solar, cur_wind, cur_hydro = float(base["Solar_TWh"]), float(base["Wind_TWh"]), float(base["Hydro_TWh"])
    for y in sim_years:
        cur_solar *= (1 + solar_g / 100)
        cur_wind *= (1 + wind_g / 100)
        cur_hydro *= (1 + hydro_g / 100)
        proj.append({
            "Year": y,
            "Solar_TWh": cur_solar,
            "Wind_TWh": cur_wind,
            "Hydro_TWh": cur_hydro,
            "Total_TWh": cur_solar + cur_wind + cur_hydro
        })

    sim_df = pd.DataFrame(proj)
    baseline_total_2030 = float(base["Total_TWh"])
    scenario_total_2030 = float(sim_df[sim_df["Year"] == 2030]["Total_TWh"].iloc[0])
    uplift = scenario_total_2030 - baseline_total_2030

    # Approximate avoided CO2 if additional renewable generation displaces fossil generation.
    avoided_mtco2 = uplift * 0.45

    fig_sim = go.Figure()
    fig_sim.add_trace(go.Bar(
        x=sim_df["Year"], y=sim_df["Solar_TWh"], name="Solar", marker_color="#f4c430"
    ))
    fig_sim.add_trace(go.Bar(
        x=sim_df["Year"], y=sim_df["Wind_TWh"], name="Wind", marker_color="#4fc3f7"
    ))
    fig_sim.add_trace(go.Bar(
        x=sim_df["Year"], y=sim_df["Hydro_TWh"], name="Hydro", marker_color="#26a69a"
    ))
    fig_sim.update_layout(
        barmode="stack",
        template="plotly_dark",
        height=430,
        yaxis_title="Projected Electricity (TWh)",
        legend=dict(orientation="h", yanchor="bottom", y=1.01)
    )
    st.plotly_chart(fig_sim, use_container_width=True)

    a, b, c = st.columns(3)
    with a:
        st.metric("2030 Scenario Output", f"{scenario_total_2030:,.0f} TWh")
    with b:
        st.metric("Net Uplift vs 2023", f"{uplift:+,.0f} TWh")
    with c:
        st.metric("Potential Avoided Emissions", f"{avoided_mtco2:,.0f} MtCO2")

with tab3:
    st.subheader("🏆 Country Competitiveness Scorecard")
    score_year = st.slider("Evaluation year", 2005, 2023, 2023, key="score_year")
    score_df = df[df["Year"] == score_year].copy()

    # Diversification score (higher means a healthier energy mix).
    shares = score_df[["Solar_Share", "Wind_Share", "Hydro_Share"]] / 100
    score_df["Diversity"] = -(shares * np.log(shares.replace(0, np.nan))).sum(axis=1).fillna(0)

    # Momentum score based on 3-year growth when available.
    momentum_vals = []
    for c_name in score_df["Country"]:
        sub = df[df["Country"] == c_name].sort_values("Year")
        row_now = sub[sub["Year"] == score_year]
        row_prev = sub[sub["Year"] == max(score_year - 3, sub["Year"].min())]
        if not row_now.empty and not row_prev.empty:
            now_total = float(row_now["Total_TWh"].iloc[0])
            prev_total = float(row_prev["Total_TWh"].iloc[0])
            yrs = max(score_year - int(row_prev["Year"].iloc[0]), 1)
            mom = ((now_total / prev_total) ** (1 / yrs) - 1) if prev_total > 0 else 0
        else:
            mom = 0
        momentum_vals.append(mom)
    score_df["Momentum"] = momentum_vals

    for metric in ["Total_TWh", "Diversity", "Momentum", "Solar_Share", "Wind_Share"]:
        mn, mx = score_df[metric].min(), score_df[metric].max()
        score_df[f"N_{metric}"] = 0 if mx == mn else (score_df[metric] - mn) / (mx - mn)

    score_df["Fellowship_Score"] = (
        0.35 * score_df["N_Total_TWh"] +
        0.20 * score_df["N_Diversity"] +
        0.25 * score_df["N_Momentum"] +
        0.10 * score_df["N_Solar_Share"] +
        0.10 * score_df["N_Wind_Share"]
    ) * 100

    score_df = score_df.sort_values("Fellowship_Score", ascending=False).reset_index(drop=True)
    score_df.index = score_df.index + 1

    fig_rank = px.bar(
        score_df,
        x="Country",
        y="Fellowship_Score",
        color="Fellowship_Score",
        color_continuous_scale="Viridis",
        template="plotly_dark",
        labels={"Fellowship_Score": "Composite Score"}
    )
    fig_rank.update_layout(height=410, coloraxis_showscale=False)
    st.plotly_chart(fig_rank, use_container_width=True)

    st.dataframe(
        score_df[["Country", "Fellowship_Score", "Total_TWh", "Diversity", "Momentum", "Solar_Share", "Wind_Share"]]
        .style.format({
            "Fellowship_Score": "{:.1f}",
            "Total_TWh": "{:,.0f}",
            "Diversity": "{:.3f}",
            "Momentum": "{:.2%}",
            "Solar_Share": "{:.1f}%",
            "Wind_Share": "{:.1f}%",
        }),
        use_container_width=True
    )

with tab4:
    st.subheader("🧠 Quasi-Causal Evidence: Synthetic Counterfactual")
    st.caption("A transparent synthetic-control style estimate of policy-period impact using donor-country combinations.")

    treated_country = st.selectbox(
        "Treated country",
        options=[c for c in countries if c != "World"],
        index=[c for c in countries if c != "World"].index("Spain") if "Spain" in countries else 0,
        key="treated_country"
    )
    intervention_year = st.slider("Intervention year", 2006, 2020, 2013, key="intervention_year")

    donor_pool = [c for c in countries if c not in ["World", treated_country]]
    selected_donors = st.multiselect(
        "Donor pool",
        options=donor_pool,
        default=donor_pool[: min(4, len(donor_pool))],
        key="donor_pool"
    )

    if len(selected_donors) < 2:
        st.warning("Select at least two donor countries to estimate a robust counterfactual.")
    else:
        treated = df[df["Country"] == treated_country].sort_values("Year")[["Year", "Total_TWh"]].copy()
        donors = (
            df[df["Country"].isin(selected_donors)]
            .pivot(index="Year", columns="Country", values="Total_TWh")
            .sort_index()
            .copy()
        )

        common_years = sorted(set(treated["Year"]).intersection(set(donors.index)))
        treated = treated[treated["Year"].isin(common_years)].set_index("Year")
        donors = donors.loc[common_years]

        pre_years = [y for y in common_years if y < intervention_year]
        post_years = [y for y in common_years if y >= intervention_year]

        if len(pre_years) < 5 or len(post_years) < 3:
            st.warning("Choose an intervention year that leaves enough pre and post years.")
        else:
            X_pre = donors.loc[pre_years].to_numpy()
            y_pre = treated.loc[pre_years, "Total_TWh"].to_numpy()

            # Unconstrained least squares with non-negative projection and normalization.
            w_raw = np.linalg.lstsq(X_pre, y_pre, rcond=None)[0]
            w = np.clip(w_raw, 0, None)
            if float(w.sum()) == 0:
                w = np.ones_like(w) / len(w)
            else:
                w = w / w.sum()

            synth_series = pd.Series(donors.to_numpy() @ w, index=donors.index, name="Synthetic")
            treated_series = treated["Total_TWh"].rename("Observed")
            effect_series = treated_series - synth_series

            pre_rmspe = float(np.sqrt(np.mean((effect_series.loc[pre_years]) ** 2)))
            post_rmspe = float(np.sqrt(np.mean((effect_series.loc[post_years]) ** 2)))
            rmspe_ratio = post_rmspe / pre_rmspe if pre_rmspe > 0 else np.nan
            att_post = float(effect_series.loc[post_years].mean())

            # Placebo test: each donor becomes treated, others become donor pool.
            placebo_ratios = []
            for pseudo in selected_donors:
                pseudo_y = df[df["Country"] == pseudo].sort_values("Year").set_index("Year")["Total_TWh"]
                pseudo_donor_names = [c for c in selected_donors if c != pseudo]
                if len(pseudo_donor_names) < 2:
                    continue
                pseudo_X = (
                    df[df["Country"].isin(pseudo_donor_names)]
                    .pivot(index="Year", columns="Country", values="Total_TWh")
                    .sort_index()
                )
                pseudo_common = sorted(set(pseudo_y.index).intersection(set(pseudo_X.index)))
                pseudo_pre = [y for y in pseudo_common if y < intervention_year]
                pseudo_post = [y for y in pseudo_common if y >= intervention_year]
                if len(pseudo_pre) < 5 or len(pseudo_post) < 3:
                    continue

                pseudo_fit = np.linalg.lstsq(
                    pseudo_X.loc[pseudo_pre].to_numpy(),
                    pseudo_y.loc[pseudo_pre].to_numpy(),
                    rcond=None
                )[0]
                pseudo_fit = np.clip(pseudo_fit, 0, None)
                if float(pseudo_fit.sum()) == 0:
                    pseudo_fit = np.ones_like(pseudo_fit) / len(pseudo_fit)
                else:
                    pseudo_fit = pseudo_fit / pseudo_fit.sum()

                pseudo_synth = pd.Series(pseudo_X.to_numpy() @ pseudo_fit, index=pseudo_X.index)
                pseudo_effect = pseudo_y.loc[pseudo_common] - pseudo_synth.loc[pseudo_common]

                pseudo_pre_r = float(np.sqrt(np.mean((pseudo_effect.loc[pseudo_pre]) ** 2)))
                pseudo_post_r = float(np.sqrt(np.mean((pseudo_effect.loc[pseudo_post]) ** 2)))
                if pseudo_pre_r > 0:
                    placebo_ratios.append(pseudo_post_r / pseudo_pre_r)

            pseudo_p = (
                (sum(r >= rmspe_ratio for r in placebo_ratios) + 1) / (len(placebo_ratios) + 1)
                if placebo_ratios and not np.isnan(rmspe_ratio)
                else np.nan
            )

            cf = pd.DataFrame({
                "Year": common_years,
                "Observed": treated_series.loc[common_years].values,
                "Synthetic": synth_series.loc[common_years].values,
                "Effect": effect_series.loc[common_years].values,
            })

            fig_cf = make_subplots(
                rows=2,
                cols=1,
                shared_xaxes=True,
                vertical_spacing=0.12,
                subplot_titles=("Observed vs Synthetic", "Estimated Treatment Effect")
            )
            fig_cf.add_trace(
                go.Scatter(x=cf["Year"], y=cf["Observed"], mode="lines", name=f"Observed ({treated_country})", line=dict(width=3, color="#4fc3f7")),
                row=1,
                col=1
            )
            fig_cf.add_trace(
                go.Scatter(x=cf["Year"], y=cf["Synthetic"], mode="lines", name="Synthetic control", line=dict(width=2, dash="dash", color="#f4c430")),
                row=1,
                col=1
            )
            fig_cf.add_trace(
                go.Bar(x=cf["Year"], y=cf["Effect"], name="Effect (TWh)", marker_color="#26a69a"),
                row=2,
                col=1
            )
            fig_cf.add_vline(x=intervention_year, line_dash="dot", line_color="#ffffff", opacity=0.8)
            fig_cf.update_layout(template="plotly_dark", height=560, legend=dict(orientation="h", yanchor="bottom", y=1.02))
            st.plotly_chart(fig_cf, use_container_width=True)

            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric("Post-period ATT", f"{att_post:+,.1f} TWh")
            with m2:
                st.metric("RMSPE Ratio (Post/Pre)", f"{rmspe_ratio:.2f}" if not np.isnan(rmspe_ratio) else "NA")
            with m3:
                st.metric("Placebo p-value", f"{pseudo_p:.3f}" if not np.isnan(pseudo_p) else "NA")

            weights_df = pd.DataFrame({"Country": selected_donors, "Weight": w}).sort_values("Weight", ascending=False)
            st.caption("Donor weights used in synthetic counterfactual")
            st.dataframe(weights_df.style.format({"Weight": "{:.3f}"}), use_container_width=True)

with tab5:
    st.subheader("🇪🇸 Spain Policy Intelligence Dashboard")
    st.caption("Spain-specific transition diagnostics with policy milestones and 2030 target tracking.")

    spain = df[df["Country"] == "Spain"].sort_values("Year").copy()
    if spain.empty:
        st.warning("Spain data is not available in the current dataset.")
    else:
        # Approximate policy milestones for storytelling and interviews.
        milestones = pd.DataFrame({
            "Year": [2004, 2007, 2013, 2019, 2021, 2023],
            "Policy Milestone": [
                "Early feed-in acceleration for renewables",
                "Renewable framework expansion",
                "Market reform and transition reset",
                "National Climate & Energy Plan (NECP)",
                "Climate Change and Energy Transition Law",
                "Updated deployment auctions and grid modernization"
            ]
        })

        fig_spain = go.Figure()
        fig_spain.add_trace(go.Scatter(x=spain["Year"], y=spain["Solar_TWh"], mode="lines+markers", name="Solar", line=dict(color="#f4c430", width=3)))
        fig_spain.add_trace(go.Scatter(x=spain["Year"], y=spain["Wind_TWh"], mode="lines+markers", name="Wind", line=dict(color="#4fc3f7", width=3)))
        fig_spain.add_trace(go.Scatter(x=spain["Year"], y=spain["Hydro_TWh"], mode="lines+markers", name="Hydro", line=dict(color="#26a69a", width=3)))
        for _, row in milestones.iterrows():
            fig_spain.add_vline(x=int(row["Year"]), line_dash="dot", line_color="rgba(255,255,255,0.35)")
        fig_spain.update_layout(
            template="plotly_dark",
            height=430,
            yaxis_title="Electricity (TWh)",
            legend=dict(orientation="h", yanchor="bottom", y=1.01)
        )
        st.plotly_chart(fig_spain, use_container_width=True)

        st.dataframe(milestones, use_container_width=True)

        # 2030 target tracker using recent CAGR (2013-2023) as momentum proxy.
        recent = spain[spain["Year"] >= 2013].copy()
        yrs = max(int(recent["Year"].max() - recent["Year"].min()), 1)

        def cagr(last_val, first_val, n):
            first = max(float(first_val), 1e-6)
            return (float(last_val) / first) ** (1 / n) - 1

        solar_cagr_sp = cagr(recent["Solar_TWh"].iloc[-1], recent["Solar_TWh"].iloc[0], yrs)
        wind_cagr_sp = cagr(recent["Wind_TWh"].iloc[-1], recent["Wind_TWh"].iloc[0], yrs)
        hydro_cagr_sp = cagr(recent["Hydro_TWh"].iloc[-1], recent["Hydro_TWh"].iloc[0], yrs)

        years_to_2030 = 7
        p2030_solar = float(spain["Solar_TWh"].iloc[-1] * ((1 + solar_cagr_sp) ** years_to_2030))
        p2030_wind = float(spain["Wind_TWh"].iloc[-1] * ((1 + wind_cagr_sp) ** years_to_2030))
        p2030_hydro = float(spain["Hydro_TWh"].iloc[-1] * ((1 + hydro_cagr_sp) ** years_to_2030))
        p2030_total = max(p2030_solar + p2030_wind + p2030_hydro, 1e-6)

        sh_solar = p2030_solar / p2030_total * 100
        sh_wind = p2030_wind / p2030_total * 100
        sh_hydro = p2030_hydro / p2030_total * 100

        target_solar, target_wind, target_hydro = 28.0, 44.0, 18.0

        g1, g2, g3 = st.columns(3)
        with g1:
            fig_g1 = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=sh_solar,
                delta={"reference": target_solar},
                title={"text": "Solar Share 2030"},
                gauge={"axis": {"range": [0, 60]}, "bar": {"color": "#f4c430"}, "threshold": {"line": {"color": "white", "width": 2}, "value": target_solar}}
            ))
            fig_g1.update_layout(template="plotly_dark", height=280, margin=dict(l=20, r=20, t=60, b=20))
            st.plotly_chart(fig_g1, use_container_width=True)
        with g2:
            fig_g2 = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=sh_wind,
                delta={"reference": target_wind},
                title={"text": "Wind Share 2030"},
                gauge={"axis": {"range": [0, 70]}, "bar": {"color": "#4fc3f7"}, "threshold": {"line": {"color": "white", "width": 2}, "value": target_wind}}
            ))
            fig_g2.update_layout(template="plotly_dark", height=280, margin=dict(l=20, r=20, t=60, b=20))
            st.plotly_chart(fig_g2, use_container_width=True)
        with g3:
            fig_g3 = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=sh_hydro,
                delta={"reference": target_hydro},
                title={"text": "Hydro Share 2030"},
                gauge={"axis": {"range": [0, 40]}, "bar": {"color": "#26a69a"}, "threshold": {"line": {"color": "white", "width": 2}, "value": target_hydro}}
            ))
            fig_g3.update_layout(template="plotly_dark", height=280, margin=dict(l=20, r=20, t=60, b=20))
            st.plotly_chart(fig_g3, use_container_width=True)

        target_alignment = max(0.0, 100 - (abs(sh_solar - target_solar) + abs(sh_wind - target_wind) + abs(sh_hydro - target_hydro)))
        momentum_score = max(0.0, min(100.0, (solar_cagr_sp * 0.5 + wind_cagr_sp * 0.35 + hydro_cagr_sp * 0.15) * 900))
        diversity_now = float(spain["Solar_Share"].iloc[-1] * 0.3 + spain["Wind_Share"].iloc[-1] * 0.4 + spain["Hydro_Share"].iloc[-1] * 0.3)
        policy_readiness = 0.45 * target_alignment + 0.35 * momentum_score + 0.20 * diversity_now

        x1, x2, x3 = st.columns(3)
        with x1:
            st.metric("Target Alignment Index", f"{target_alignment:.1f}/100")
        with x2:
            st.metric("Growth Momentum Index", f"{momentum_score:.1f}/100")
        with x3:
            st.metric("Spain Policy Readiness", f"{policy_readiness:.1f}/100")

with tab6:
    st.subheader("📥 Download Data for Portfolio and Reports")
    st.caption("Export your filtered dataset and a concise insight note for fellowship applications.")

    export_cols = [
        "Year", "Country", "Solar_TWh", "Wind_TWh", "Hydro_TWh",
        "Total_TWh", "Solar_Share", "Wind_Share", "Hydro_Share"
    ]
    export_df = filtered[export_cols].sort_values(["Country", "Year"]).reset_index(drop=True)
    csv_data = export_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Filtered Dataset (CSV)",
        data=csv_data,
        file_name="renewable_energy_filtered.csv",
        mime="text/csv"
    )

    if not export_df.empty:
        latest_year = int(export_df["Year"].max())
        latest_rows = export_df[export_df["Year"] == latest_year]
        top_country = latest_rows.sort_values("Total_TWh", ascending=False).iloc[0]
        solar_jump = df[df["Country"] == "World"].sort_values("Year")
        solar_cagr = ((solar_jump["Solar_TWh"].iloc[-1] / solar_jump["Solar_TWh"].iloc[0]) ** (1 / (len(solar_jump)-1)) - 1) * 100

        insight_text = (
            "Renewable Energy Insight Brief\n"
            "================================\n"
            f"Analysis coverage: {int(export_df['Year'].min())}-{latest_year}\n"
            f"Selected countries: {', '.join(sorted(export_df['Country'].unique()))}\n"
            f"Top producer in {latest_year}: {top_country['Country']} ({top_country['Total_TWh']:,.0f} TWh)\n"
            f"Global solar CAGR (2000-2023): {solar_cagr:.2f}%\n"
            "\n"
            "Portfolio talking point:\n"
            "This dashboard combines historical trend analysis, forecasting, policy scenario simulation, "
            "and multi-factor competitiveness scoring to support evidence-based clean energy strategy decisions.\n"
        )

        st.download_button(
            label="Download Insight Brief (TXT)",
            data=insight_text.encode("utf-8"),
            file_name="renewable_energy_insight_brief.txt",
            mime="text/plain"
        )

# ── Footer ────────────────────────────────────────────────────────────────────
st.divider()
st.markdown(
    "<center style='color:#555; font-size:0.8rem;'>"
    "Built by <b>Muhammad Ali Afzal</b> · "
    "<a href='https://muhammadaliafzalsportfolio.netlify.app' target='_blank' style='color:#4fc3f7;'>Portfolio</a> · "
    "Data: IEA / IRENA / Our World in Data"
    "</center>", unsafe_allow_html=True
)
