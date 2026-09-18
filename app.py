import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Car Hunter",
    page_icon="🚗",
    layout="centered"
)

st.title("🚗 Car Hunter")
st.caption("מחפש מציאות לרכב")

st.divider()

st.subheader("🔎 הגדרות חיפוש")

models = st.multiselect(
    "דגמים",
    ["Mazda CX-5", "Toyota RAV4"],
    default=["Mazda CX-5", "Toyota RAV4"]
)

max_price = st.number_input(
    "מחיר מקסימלי",
    min_value=5000,
    max_value=100000,
    value=30000,
    step=1000
)

max_km = st.number_input(
    "קילומטרים מקסימליים",
    min_value=50000,
    max_value=500000,
    value=300000,
    step=10000
)

st.write("📍 אזור: **כל הארץ**")

st.divider()

# Demo listings
cars = pd.DataFrame([
    {
        "דגם": "Mazda CX-5",
        "שנה": 2015,
        "ק״מ": 185000,
        "יד": 2,
        "מחיר": 28500,
        "אזור": "פתח תקווה"
    },
    {
        "דגם": "Mazda CX-5",
        "שנה": 2016,
        "ק״מ": 235000,
        "יד": 3,
        "מחיר": 30000,
        "אזור": "חיפה"
    },
    {
        "דגם": "Toyota RAV4",
        "שנה": 2014,
        "ק״מ": 210000,
        "יד": 2,
        "מחיר": 29500,
        "אזור": "ראשון לציון"
    },
    {
        "דגם": "Toyota RAV4",
        "שנה": 2013,
        "ק״מ": 310000,
        "יד": 3,
        "מחיר": 24000,
        "אזור": "באר שבע"
    }
])


def calculate_score(car):
    score = 50

    # מחיר
    if car["מחיר"] <= 25000:
        score += 20
    elif car["מחיר"] <= 28000:
        score += 15
    elif car["מחיר"] <= 30000:
        score += 10

    # קילומטראז'
    if car["ק״מ"] <= 200000:
        score += 20
    elif car["ק״מ"] <= 250000:
        score += 12
    elif car["ק״מ"] <= 300000:
        score += 5

    # יד
    if car["יד"] == 1:
        score += 10
    elif car["יד"] == 2:
        score += 7
    elif car["יד"] == 3:
        score += 4

    return min(score, 100)


if st.button("🔍 חפש מציאות", use_container_width=True):

    results = cars[
        (cars["דגם"].isin(models)) &
        (cars["מחיר"] <= max_price) &
        (cars["ק״מ"] <= max_km)
    ].copy()

    if results.empty:
        st.warning("לא נמצאו רכבים שמתאימים לחיפוש.")
    else:

        results["🔥 Deal Score"] = results.apply(
            calculate_score,
            axis=1
        )

        results = results.sort_values(
            "🔥 Deal Score",
            ascending=False
        )

        st.subheader("🚨 המציאות שמצאתי")

        for _, car in results.iterrows():

            score = car["🔥 Deal Score"]

            if score >= 80:
                label = "🔥 מציאה חזקה"
            elif score >= 70:
                label = "🟢 שווה בדיקה"
            else:
                label = "🟡 לבדוק"

            with st.container(border=True):

                st.markdown(
                    f"### {car['דגם']} — {car['שנה']}"
                )

                st.write(
                    f"💰 **₪{car['מחיר']:,}**   |   "
                    f"🛣️ **{car['ק״מ']:,} ק״מ**   |   "
                    f"👤 **יד {car['יד']}**"
                )

                st.write(f"📍 {car['אזור']}")

                st.metric(
                    "🔥 Deal Score",
                    f"{score}/100"
                )

                st.write(f"**{label}**")

st.divider()

st.caption("Car Hunter V1.1")