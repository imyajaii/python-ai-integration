import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# Load the dataset
@st.cache
def load_data():
    data = pd.read_csv('../data/thailand_domestic_tourism.csv')
    data['travel_date'] = pd.to_datetime(data['travel_date'])
    return data

data = load_data()

# Filter data for the years 2019 to 2023
data = data[(data['travel_date'] >= '2019-01-01') & (data['travel_date'] <= '2023-12-31')]

# Group by year and calculate total tourists and revenue
data['year'] = data['travel_date'].dt.year
annual_data = data.groupby('year').agg({'no_tourist_all': 'sum', 'revenue_all': 'sum'}).reset_index()

# Forecasting using Exponential Smoothing
model_tourists = ExponentialSmoothing(annual_data['no_tourist_all'], trend='add', seasonal=None).fit()
model_revenue = ExponentialSmoothing(annual_data['revenue_all'], trend='add', seasonal=None).fit()

# Forecast for the next 3 years (2024-2026)
forecast_years = [2024, 2025, 2026]
forecast_tourists = model_tourists.forecast(len(forecast_years))
forecast_revenue = model_revenue.forecast(len(forecast_years))

# Combine results into a DataFrame
forecast_df = pd.DataFrame({
    'year': forecast_years,
    'forecast_tourists': forecast_tourists,
    'forecast_revenue': forecast_revenue
})

# Streamlit App Layout
st.title("Post-Pandemic Recovery: Tourism Trends and Forecast")
st.write("This application analyzes historical tourism data from 2019 to 2023 and forecasts trends for 2024–2026.")

# Display Historical Data
st.subheader("Historical Data (2019–2023)")
st.write(annual_data)

# Display Forecast Data
st.subheader("Forecast Data (2024–2026)")
st.write(forecast_df)

# Plot Tourist Numbers Forecast
st.subheader("Tourist Numbers Forecast")
fig1, ax1 = plt.subplots(figsize=(10, 5))
ax1.plot(annual_data['year'], annual_data['no_tourist_all'], label='Historical Tourists', marker='o')
ax1.plot(forecast_df['year'], forecast_df['forecast_tourists'], label='Forecast Tourists', marker='o')
ax1.set_title('Tourist Numbers Forecast')
ax1.set_xlabel('Year')
ax1.set_ylabel('Number of Tourists')
ax1.legend()
ax1.grid()
st.pyplot(fig1)

# Plot Revenue Forecast
st.subheader("Revenue Forecast")
fig2, ax2 = plt.subplots(figsize=(10, 5))
ax2.plot(annual_data['year'], annual_data['revenue_all'], label='Historical Revenue', marker='o')
ax2.plot(forecast_df['year'], forecast_df['forecast_revenue'], label='Forecast Revenue', marker='o')
ax2.set_title('Revenue Forecast')
ax2.set_xlabel('Year')
ax2.set_ylabel('Revenue (in Baht)')
ax2.legend()
ax2.grid()
st.pyplot(fig2)