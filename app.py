import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="HopeResearch",
    page_icon="🧬",
    layout="wide"
)


def get_risk_label(score):
    if score >= 5:
        return "High"
    elif score >= 3:
        return "Moderate"
    return "Low"


def get_age_group(age):
    if age <= 8:
        return "5-8"
    elif age <= 12:
        return "9-12"
    elif age <= 15:
        return "13-15"
    return "16-18"


def calculate_risks(row):
    iron = 0
    b12 = 0
    zinc = 0

    if row["vegetables_per_day"] < 3:
        iron += 2
    if row["meat_per_week"] < 2:
        iron += 1
        b12 += 3
        zinc += 2
    if row["dairy_per_week"] < 2:
        b12 += 1
    if row["food_access"] <= 2:
        iron += 2
        b12 += 1
        zinc += 2
    if row["supplements"] == 0:
        iron += 1
        b12 += 1
        zinc += 1
    if row["age"] < 12:
        iron += 1
        zinc += 1

    return pd.Series({
        "age_group": get_age_group(row["age"]),
        "iron_risk": get_risk_label(iron),
        "b12_risk": get_risk_label(b12),
        "zinc_risk": get_risk_label(zinc),
    })


def make_risk_chart(data, column, title):
    counts = data[column].value_counts().reset_index()
    counts.columns = ["Risk", "Count"]

    fig = px.bar(
        counts,
        x="Risk",
        y="Count",
        color="Risk",
        color_discrete_map={
            "High": "#22c55e",
            "Moderate": "#84cc16",
            "Low": "#14532d"
        },
        title=title
    )

    fig.update_layout(
        paper_bgcolor="#050807",
        plot_bgcolor="#050807",
        font_color="#f8fff4",
        title_font_size=18,
        height=330,
        margin=dict(l=20, r=20, t=50, b=20),
        legend_title_text=""
    )

    return fig


def make_age_chart(data, column, title):
    high_risk = data[data[column] == "High"]
    counts = high_risk["age_group"].value_counts().reset_index()
    counts.columns = ["Age Group", "High-Risk Count"]

    fig = px.bar(
        counts,
        x="Age Group",
        y="High-Risk Count",
        color_discrete_sequence=["#22c55e"],
        title=title
    )

    fig.update_layout(
        paper_bgcolor="#050807",
        plot_bgcolor="#050807",
        font_color="#f8fff4",
        title_font_size=18,
        height=330,
        margin=dict(l=20, r=20, t=50, b=20)
    )

    return fig


st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(circle at 15% 10%, rgba(34,197,94,0.18), transparent 28%),
            radial-gradient(circle at 85% 30%, rgba(132,204,22,0.10), transparent 25%),
            linear-gradient(135deg, #050807 0%, #020403 100%);
        color: #f8fff4;
    }

    [data-testid="stSidebar"] {
        background-color: #050807;
    }

    .nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1.1rem 0 2.3rem 0;
        color: #f8fff4;
    }

    .brand {
        font-size: 1.2rem;
        font-weight: 800;
        letter-spacing: -0.03em;
    }

    .nav-links {
        color: #9cae97;
        font-size: 0.85rem;
        letter-spacing: 0.22em;
        text-transform: uppercase;
    }

    .hero {
        padding: 5rem 3rem;
        border-radius: 30px;
        background:
            linear-gradient(135deg, rgba(34,197,94,0.16), rgba(6,95,70,0.05)),
            radial-gradient(circle at 80% 20%, rgba(190,242,100,0.10), transparent 24%);
        border: 1px solid rgba(190,242,100,0.18);
        box-shadow: 0 0 90px rgba(34,197,94,0.12);
        margin-bottom: 2.5rem;
    }

    .eyebrow {
        display: inline-block;
        padding: 0.45rem 0.85rem;
        border-radius: 999px;
        border: 1px solid rgba(190,242,100,0.28);
        color: #bef264;
        background: rgba(22,101,52,0.18);
        font-size: 0.8rem;
        margin-bottom: 1.4rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    .hero-title {
        font-size: 5.8rem;
        line-height: 0.95;
        font-weight: 900;
        letter-spacing: -0.08em;
        max-width: 1000px;
        color: #f8fff4;
        margin-bottom: 1.5rem;
    }

    .hero-subtitle {
        color: #b7c8af;
        font-size: 1.22rem;
        line-height: 1.75;
        max-width: 820px;
    }

    .section-title {
        font-size: 2rem;
        font-weight: 850;
        letter-spacing: -0.04em;
        margin-top: 2.8rem;
        margin-bottom: 1rem;
        color: #f8fff4;
    }

    .feature-card {
        padding: 1.5rem;
        min-height: 180px;
        border-radius: 22px;
        background: linear-gradient(180deg, rgba(255,255,255,0.055), rgba(255,255,255,0.025));
        border: 1px solid rgba(255,255,255,0.09);
        box-shadow: 0 20px 70px rgba(0,0,0,0.25);
    }

    .feature-num {
        color: #bef264;
        font-size: 0.85rem;
        letter-spacing: 0.2em;
        margin-bottom: 2rem;
    }

    .feature-title {
        color: #f8fff4;
        font-size: 1.35rem;
        font-weight: 750;
        margin-bottom: 0.6rem;
    }

    .feature-text {
        color: #9fb09a;
        line-height: 1.65;
        font-size: 0.95rem;
    }

    .metric-card {
        padding: 1.4rem;
        border-radius: 20px;
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.09);
    }

    .metric-label {
        color: #9fb09a;
        font-size: 0.85rem;
        margin-bottom: 0.45rem;
    }

    .metric-value {
        color: #f8fff4;
        font-size: 2rem;
        font-weight: 850;
    }

    .small-note {
        color: #9fb09a;
        font-size: 0.95rem;
        line-height: 1.65;
    }

    div[data-testid="stFileUploader"] {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 20px;
        padding: 1rem;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #f8fff4 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.markdown(
    """
    <div class="nav">
        <div class="brand">🧬 HopeResearch</div>
        <div class="nav-links">Platform&nbsp;&nbsp;&nbsp;Analytics&nbsp;&nbsp;&nbsp;Interventions</div>
    </div>

    <div class="hero">
        <div class="eyebrow">AI-assisted public health analytics</div>
        <div class="hero-title">Community nutrition intelligence.</div>
        <div class="hero-subtitle">
            HopeResearch helps identify micronutrient risk patterns, surface vulnerable age groups,
            and simulate outreach interventions for underserved communities.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


st.markdown('<div class="section-title">Platform capabilities</div>', unsafe_allow_html=True)

f1, f2, f3 = st.columns(3)

with f1:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-num">01</div>
            <div class="feature-title">Survey analysis.</div>
            <div class="feature-text">Upload community nutrition surveys and automatically classify estimated iron, B12, and zinc risk patterns.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with f2:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-num">02</div>
            <div class="feature-title">Population insight.</div>
            <div class="feature-text">Break risk down by nutrient and age group to identify who may need the most targeted outreach.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with f3:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-num">03</div>
            <div class="feature-title">Intervention planning.</div>
            <div class="feature-text">Simulate how outreach campaigns may reduce high-risk prevalence before deploying nonprofit resources.</div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.markdown('<div class="section-title">Upload community survey data</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="small-note">Required columns: age, vegetables_per_day, meat_per_week, dairy_per_week, food_access, supplements.</div>',
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader("Upload survey CSV", type=["csv"], label_visibility="collapsed")


if uploaded_file:
    data = pd.read_csv(uploaded_file)
    risk_results = data.apply(calculate_risks, axis=1)
    final_data = pd.concat([data, risk_results], axis=1)

    population_size = len(final_data)
    iron_high_percent = round((final_data["iron_risk"].eq("High").sum() / population_size) * 100, 1)
    b12_high_percent = round((final_data["b12_risk"].eq("High").sum() / population_size) * 100, 1)
    zinc_high_percent = round((final_data["zinc_risk"].eq("High").sum() / population_size) * 100, 1)

    m1, m2, m3, m4 = st.columns(4)

    metrics = [
        ("Population analyzed", population_size),
        ("High iron risk", f"{iron_high_percent}%"),
        ("High B12 risk", f"{b12_high_percent}%"),
        ("High zinc risk", f"{zinc_high_percent}%"),
    ]

    for col, (label, value) in zip([m1, m2, m3, m4], metrics):
        with col:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{value}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown('<div class="section-title">Analyzed survey data</div>', unsafe_allow_html=True)
    st.dataframe(final_data, use_container_width=True)

    st.markdown('<div class="section-title">Risk distribution</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.plotly_chart(make_risk_chart(final_data, "iron_risk", "Iron risk"), use_container_width=True)
    with c2:
        st.plotly_chart(make_risk_chart(final_data, "b12_risk", "Vitamin B12 risk"), use_container_width=True)
    with c3:
        st.plotly_chart(make_risk_chart(final_data, "zinc_risk", "Zinc risk"), use_container_width=True)

    st.markdown('<div class="section-title">Age-group high-risk analysis</div>', unsafe_allow_html=True)

    a1, a2, a3 = st.columns(3)
    with a1:
        st.plotly_chart(make_age_chart(final_data, "iron_risk", "Iron high risk by age"), use_container_width=True)
    with a2:
        st.plotly_chart(make_age_chart(final_data, "b12_risk", "B12 high risk by age"), use_container_width=True)
    with a3:
        st.plotly_chart(make_age_chart(final_data, "zinc_risk", "Zinc high risk by age"), use_container_width=True)

    st.markdown('<div class="section-title">Community recommendations</div>', unsafe_allow_html=True)

    if iron_high_percent >= 20:
        st.warning("Iron risk is elevated. Prioritize iron-focused nutrition education and food-support interventions.")
    else:
        st.success("Iron risk is not currently the highest priority based on this dataset.")

    if b12_high_percent >= 20:
        st.warning("Vitamin B12 risk is elevated. Consider fortified-food education and animal-source food access guidance.")
    else:
        st.success("Vitamin B12 risk is not currently the highest priority based on this dataset.")

    if zinc_high_percent >= 20:
        st.warning("Zinc risk is elevated. Consider zinc-rich food education and outreach materials.")
    else:
        st.success("Zinc risk is not currently the highest priority based on this dataset.")

    st.markdown('<div class="section-title">Intervention simulator</div>', unsafe_allow_html=True)

    s1, s2, s3 = st.columns(3)
    with s1:
        iron_reduction = st.slider("Projected iron reduction (%)", 0, 50, 10)
    with s2:
        b12_reduction = st.slider("Projected B12 reduction (%)", 0, 50, 10)
    with s3:
        zinc_reduction = st.slider("Projected zinc reduction (%)", 0, 50, 10)

    projected_iron = max(0, round(iron_high_percent - iron_reduction, 1))
    projected_b12 = max(0, round(b12_high_percent - b12_reduction, 1))
    projected_zinc = max(0, round(zinc_high_percent - zinc_reduction, 1))

    p1, p2, p3 = st.columns(3)
    with p1:
        st.metric("Projected iron high risk", f"{projected_iron}%", f"-{iron_reduction}%")
    with p2:
        st.metric("Projected B12 high risk", f"{projected_b12}%", f"-{b12_reduction}%")
    with p3:
        st.metric("Projected zinc high risk", f"{projected_zinc}%", f"-{zinc_reduction}%")

    intervention_summary = f"""
HopeResearch Intervention Simulation

Current High-Risk Prevalence:
Iron: {iron_high_percent}%
Vitamin B12: {b12_high_percent}%
Zinc: {zinc_high_percent}%

Projected Post-Intervention High-Risk Prevalence:
Iron: {projected_iron}%
Vitamin B12: {projected_b12}%
Zinc: {projected_zinc}%

Disclaimer:
This is a planning simulation, not a clinical prediction.
"""

    st.download_button(
        label="Download intervention simulation",
        data=intervention_summary,
        file_name="intervention_simulation.txt",
        mime="text/plain"
    )

    csv = final_data.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download analyzed results",
        data=csv,
        file_name="analyzed_survey_results.csv",
        mime="text/csv"
    )

    st.markdown(
        '<div class="small-note">Disclaimer: This is an educational screening prototype, not a diagnostic medical tool.</div>',
        unsafe_allow_html=True
    )

else:
    st.markdown(
        """
        <div class="small-note">
        Upload a CSV file to begin the dashboard.
        </div>
        """,
        unsafe_allow_html=True
    )