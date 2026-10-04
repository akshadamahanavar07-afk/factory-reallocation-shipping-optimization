
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Factory Reallocation & Shipping Optimization",
    page_icon="🏭",
    layout="wide"
)

st.title("🏭 Factory Reallocation & Shipping Optimization")
st.write("Nassau Candy Distributor Recommendation System")

recommendations = pd.read_csv("final_factory_recommendations.csv")

# KPI Cards
col1, col2, col3 = st.columns(3)

col1.metric("Total Products", len(recommendations))

col2.metric(
    "Products with Improvement",
    (recommendations["Distance Reduction (%)"] > 0).sum()
)

col3.metric(
    "Average Distance Reduction",
    f"{recommendations['Distance Reduction (%)'].mean():.2f}%"
)

st.divider()

# Product Selector
st.subheader("🔎 Factory Recommendation")

product = st.selectbox(
    "Select Product",
    recommendations["Product"].unique()
)

selected = recommendations[
    recommendations["Product"] == product
]

st.dataframe(
    selected,
    use_container_width=True
)

st.divider()

st.subheader("🔄 What-If Scenario Analysis")

st.write(
    "Compare the current factory with the recommended factory "
    "for the selected product."
)

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Current Factory",
        selected["Current Factory"].iloc[0]
    )

    st.metric(
        "Current Distance",
        f"{selected['Current Distance (km)'].iloc[0]:,.2f} km"
    )

with col2:
    st.metric(
        "Recommended Factory",
        selected["Recommended Factory"].iloc[0]
    )

    st.metric(
        "Recommended Distance",
        f"{selected['Recommended Distance (km)'].iloc[0]:,.2f} km"
    )

st.metric(
    "Distance Reduction",
    f"{selected['Distance Reduction (%)'].iloc[0]:.2f}%"
)

st.divider()

st.subheader("📊 Factory Distance Comparison")

chart_data = selected[
    ["Current Distance (km)", "Recommended Distance (km)"]
].T

chart_data.columns = ["Distance (km)"]

st.bar_chart(chart_data)

st.divider()

st.subheader("⚠️ Risk & Impact Panel")

reduction = selected["Distance Reduction (%)"].iloc[0]

if reduction >= 30:
    st.warning(
        "High-impact reassignment: significant distance reduction."
    )
elif reduction > 0:
    st.info(
        "Potential improvement: reassignment may reduce shipping distance."
    )
else:
    st.success(
        "Current factory is already the closest option for this product."
    )

st.write(
    "Scenario Confidence Score:",
    f"{min(max(reduction / 100, 0), 1) * 100:.2f}%"
)
