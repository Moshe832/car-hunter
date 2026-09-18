import streamlit as st

st.set_page_config(
    page_title="Car Hunter",
    page_icon="🚗",
    layout="centered"
)

st.title("🚗 Car Hunter")
st.subheader("מצא לי מציאה")

st.divider()

# Search criteria
st.markdown("### 🔎 מה אנחנו מחפשים?")

models = st.multiselect(
    "דגמים",
    ["Mazda CX-5", "Toyota RAV4"],
    default=["Mazda CX-5", "Toyota RAV4"]
)

max_price = st.number_input(
    "מחיר מקסימלי (₪)",
    min_value=5000,
    max_value=200000,
    value=30000,
    step=1000
)

min_year = st.number_input(
    "שנתון מינימלי",
    min_value=2000,
    max_value=2026,
    value=2010,
    step=1
)

max_km = st.number_input(
    "קילומטרים מקסימליים",
    min_value=50000,
    max_value=500000,
    value=300000,
    step=10000
)

location = st.selectbox(
    "אזור",
    ["כל הארץ", "מרכז", "צפון", "דרום", "ירושלים"]
)

st.divider()

if st.button("🔍 חפש מציאות", use_container_width=True):

    st.success("החיפוש מוכן!")

    st.markdown("### 🚨 הגדרות החיפוש שלך")

    st.write(f"**דגמים:** {', '.join(models)}")
    st.write(f"**מחיר עד:** ₪{max_price:,}")
    st.write(f"**משנת:** {min_year}")
    st.write(f"**ק״מ עד:** {max_km:,}")
    st.write(f"**אזור:** {location}")

    st.divider()

    st.info(
        "🚧 מנוע חיפוש המודעות עדיין בבנייה. "
        "בשלב הבא נחבר מקורות מודעות אמיתיים."
    )

st.divider()

st.caption("Car Hunter V1 • מחפש מציאות, לא רק מכוניות")