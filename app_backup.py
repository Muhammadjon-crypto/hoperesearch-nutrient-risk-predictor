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
    else:
        return "Low"


def get_age_group(age):
    if age <= 8:
        return "5-8"
    elif age <= 12:
        return "9-12"
    elif age <= 15:
        return "13-15"
    else:
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


st.markdown(
    """
    <style>
    .stApp {
        background: radial-gradient(circle at top left, #13231b 0%, #050807 45%, #020403 100%);
        color: #f4f7f2;
    }

    [data-testid="stSidebar"] {
        background-color: #050807;
    }

    .hero {
        padding: 4rem 2rem 3rem 2rem;
        border-radius: 24px;
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.15), rgba(6, 95, 70, 0.08));
        border: 1px solid rgba(163, 230, 53, 0.20);
        box-shadow: 0 0 60px rgba(34, 197, 94, 0.10);
        margin-bottom: 2rem;
    }

    .hero-title {
        font-size: 4rem;
        line-height: 1.05;
        font-weight: 800;
        letter-spacing: -0.06em;
        color: #f8fff4;
        margin-bottom: 1rem;
    }

    .hero-subtitle {
        font-size: 1.25rem;
        color: #b8c7b0;
        max-width: 760px;
        line-height: 1.7;
    }

    .tag {
        display: inline-block;
        padding: 0.4rem 0.8rem;
        border: 1px solid rgba(163, 230, 53, 0.25);
        border-radius: 999px;
        color: #bef264;
        background: rgba(22, 101, 52, 0.18);
        font-size: 0.85rem;
        margin-bottom: 1.25rem;
    }

    .metric-card {
        padding: 1.4rem;
        border-radius: 20px;
        background: rgba(255, 255, 255, 0.045);
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 0 40px rgba(0, 0, 0, 0.20);
    }

    .metric-label {
        color: #a8b5a2;
        font-size: 0.9rem;
        margin-bottom: 0.35rem;
    }

    .metric-value {
        color: #f8fff4;
        font-size: 2rem;
        font-weight: 800;
    }

    .section-title {
        font-size: 1.8rem;
        font-weight: 750;
        color: #f8fff4;
        margin-top: 2.5rem;
        margin-bottom: 1rem;
    }

    .small-note {
        color: #94a38f;
        font-size: 0.95rem;
        line-height: 1.6;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #f8fff4 !important;
    }

    .stDataFrame {
        border-radius: 16px;
    }

    div[data-testid="stFileUploader"] {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 18px;
        padding: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.markdown(
    """
    <div class="hero">
        <div class="tag">AI-assisted public health analytics</div>
        <div class="hero-title">HopeResearch Nutrient Risk Platform</div>
        <div class="hero-subtitle">
            A community nutrition analytics tool designed to estimate micronutrient risk patterns,
            identify vulnerable groups, and support data-driven outreach for underserved communities.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


st.markdown("### Upload community survey data")
st.markdown(
    '<div class="small-note">CSV columns needed: age, vegetables_per_day, meat_per_week, dairy_per_week, food_access, supplements.</div>',
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader("Upload survey CSV", type=["csv"], label_visibility="collapsed")


if uploaded_file:
    data = pd.read_csv(uploaded_file)
    risk_results = data.apply(calculate_risks, axis=1)
    final_data = pd.concat([data, risk_results], axis=1)

    population_size = len(final_data)

    iron_high = (final_data["iron_risk"] == "High").sum()
    b12_high = (final_data["b12_risk"] == "High").sum()
    zinc_high = (final_data["zinc_risk"] == "High").sum()

    iron_high_percent = round((iron_high / population_size) * 100, 1)
    b12_high_percent = round((b12_high / population_size) * 100, 1)
    zinc_high_percent = round((zinc_high / population_size) * 100, 1)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Population analyzed</div>
                <div class="metric-value">{population_size}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">High iron risk</div>
                <div class="metric-value">{iron_high_percent}%</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">High B12 risk</div>
                <div class="metric-value">{b12_high_percent}%</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">High zinc risk</div>
                <div class="metric-value">{zinc_high_percent}%</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown('<div class="section-title">Analyzed Survey Data</div>', unsafe_allow_html=True)
    st.dataframe(final_data, use_container_width=True)

    st.markdown('<div class="section-title">Risk Distribution</div>', unsafe_allow_html=True)

    chart_col1, chart_col2, chart_col3 = st.columns(3)

    with chart_col1:
        st.markdown("#### Iron")

        iron_counts = final_data["iron_risk"].value_counts().reset_index()
        iron_counts.columns = ["Risk", "Count"]

        fig = px.bar(
            iron_counts,
            x="Risk",
            y="Count",
            color="Risk",
            color_discrete_map={
                "High": "#22c55e",
                "Moderate": "#84cc16",
                "Low": "#14532d"
            },
            title="Iron Risk Distribution"
        )

        fig.update_layout(
            paper_bgcolor="#050807",
            plot_bgcolor="#050807",
            font_color="white"
        )

        st.plotly_chart(fig, use_container_width=True)

    with chart_col2:
        st.markdown("#### Vitamin B12")
        st.bar_chart(final_data["b12_risk"].value_counts())

    with chart_col3:
        st.markdown("#### Zinc")
        st.bar_chart(final_data["zinc_risk"].value_counts())

    st.markdown(
        '<div class="section-title">Age Group High-Risk Analysis</div>',
        unsafe_allow_html=True
    )

    age_col1, age_col2, age_col3 = st.columns(3)

    with age_col1:
        st.markdown("#### Iron")
        iron_age = final_data[final_data["iron_risk"] == "High"]["age_group"].value_counts()
        st.bar_chart(iron_age)

    with age_col2:
        st.markdown("#### Vitamin B12")
        b12_age = final_data[final_data["b12_risk"] == "High"]["age_group"].value_counts()
        st.bar_chart(b12_age)

    with age_col3:
        st.markdown("#### Zinc")
        zinc_age = final_data[final_data["zinc_risk"] == "High"]["age_group"].value_counts()
        st.bar_chart(zinc_age)

    st.markdown(
        '<div class="section-title">Community Recommendations</div>',
        unsafe_allow_html=True
    )

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

    st.markdown('<div class="section-title">Intervention Simulator</div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="small-note">Estimate how outreach interventions could reduce high-risk prevalence.</div>',
        unsafe_allow_html=True
    )

    sim_col1, sim_col2, sim_col3 = st.columns(3)

    with sim_col1:
        iron_reduction = st.slider("Projected iron risk reduction (%)", 0, 50, 10)

    with sim_col2:
        b12_reduction = st.slider("Projected B12 risk reduction (%)", 0, 50, 10)

    with sim_col3:
        zinc_reduction = st.slider("Projected zinc risk reduction (%)", 0, 50, 10)

    projected_iron = max(0, round(iron_high_percent - iron_reduction, 1))
    projected_b12 = max(0, round(b12_high_percent - b12_reduction, 1))
    projected_zinc = max(0, round(zinc_high_percent - zinc_reduction, 1))

    st.markdown("### Projected Post-Intervention Risk")

    proj_col1, proj_col2, proj_col3 = st.columns(3)

    with proj_col1:
        st.metric("Projected iron high risk", f"{projected_iron}%", f"-{iron_reduction}%")

    with proj_col2:
        st.metric("Projected B12 high risk", f"{projected_b12}%", f"-{b12_reduction}%")

    with proj_col3:
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

    st.markdown(
        '<div class="small-note">Disclaimer: This is an educational screening prototype, not a diagnostic medical tool.</div>',
        unsafe_allow_html=True
    )

    csv = final_data.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download analyzed results",
        data=csv,
        file_name="analyzed_survey_results.csv",
        mime="text/csv"
    )

else:
    st.markdown(
        """
        <div class="small-note">
        Upload a CSV file to begin. This app currently supports community survey analysis,
        age-group risk visualization, and basic outreach recommendations.
        </div>
        """,
        unsafe_allow_html=True
    )