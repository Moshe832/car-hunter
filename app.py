import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Car Hunter Israel", page_icon="🚗", layout="centered"
)

# Custom CSS for mobile / iPhone look & feel
st.markdown("""
<style>
    .car-card {
        background-color: #1e1e1e;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 16px;
        border: 1px solid #333333;
    }
    .score-badge {
        font-weight: bold;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🚗 Car Hunter Israel")
st.caption("מנוע איתור מציאות רכבים יד־שנייה")


# Mock data generation
@st.cache_data
def load_data():
  data = [
      {
          'id': 1,
          'model': 'Mazda CX-5',
          'year': 2018,
          'km': 75000,
          'hand': 2,
          'price': 62000,
          'location': 'תל אביב',
          'phone': '050-0000001',
      },
      {
          'id': 2,
          'model': 'Toyota RAV4',
          'year': 2017,
          'km': 95000,
          'hand': 1,
          'price': 75000,
          'location': 'חיפה',
          'phone': '050-0000002',
      },
      {
          'id': 3,
          'model': 'Mazda CX-5',
          'year': 2016,
          'km': 110000,
          'hand': 2,
          'price': 51000,
          'location': 'ראשון לציון',
          'phone': '050-0000003',
      },
      {
          'id': 4,
          'model': 'Toyota RAV4',
          'year': 2015,
          'km': 130000,
          'hand': 3,
          'price': 58000,
          'location': 'באר שבע',
          'phone': '050-0000004',
      },
      {
          'id': 5,
          'model': 'Mazda CX-5',
          'year': 2020,
          'km': 45000,
          'hand': 1,
          'price': 85000,
          'location': 'ירושלים',
          'phone': '050-0000005',
      },
  ]
  return pd.DataFrame(data)


df = load_data()


# Deal score logic
def add_deal_score(df: pd.DataFrame, current_year: int = 2026) -> pd.DataFrame:
  df = df.copy()
  df['car_age'] = np.maximum(1, current_year - df['year'])
  df['expected_km'] = df['car_age'] * 15000
  df['km_delta_k'] = (df['km'] - df['expected_km']) / 1000

  group_median = df.groupby(['model', 'year'])['price'].transform('median')
  df['price_delta'] = df['price'] - group_median

  base_score = 60
  price_effect = -(df['price_delta'] / 1000) * 4
  km_effect = -np.maximum(0, df['km_delta_k']) * 0.5
  hand_effect = -df.get('hand', 1) * 2

  df['deal_score'] = np.clip(
      base_score + price_effect + km_effect + hand_effect, 0, 100
  )
  return df.sort_values(by='deal_score', ascending=False)


scored_df = add_deal_score(df)

# Sidebar filters (touch friendly)
st.sidebar.header("🎛️ סינון")
selected_models = st.sidebar.multiselect(
    'דגם רכב', ['Mazda CX-5', 'Toyota RAV4'], default=['Mazda CX-5', 'Toyota RAV4']
)
max_price = st.sidebar.slider(
    'תקציב מקסימלי (₪)', 40000, 100000, 90000, step=5000
)

filtered_df = scored_df[
    (scored_df['model'].isin(selected_models))
    & (scored_df['price'] <= max_price)
]

st.subheader(f"🔍 נמצאו {len(filtered_df)} מודעות (מסודרות לפי כדאיות):")

for _, row in filtered_df.iterrows():
  score = int(row['deal_score'])
  color = '#2e7d32' if score >= 75 else '#f57f17' if score >= 50 else '#c62828'
  st.markdown(
      f"""
    <div class="car-card">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <h3 style="margin: 0;">{row['model']} ({row['year']})</h3>
            <span class="score-badge" style="background-color: {color}; color: white;">ציון: {score}</span>
        </div>
        <p style="margin: 8px 0 4px 0; font-size: 16px;"><b>מחיר:</b> ₪{row['price']:,} | <b>יד:</b> {row['hand']} | <b>ק"מ:</b> {row['km']:,}</p>
        <p style="margin: 0; color: #888; font-size: 14px;">📍 {row['location']} | 📞 {row['phone']}</p>
    </div>
    """,
      unsafe_allow_html=True,
  )
