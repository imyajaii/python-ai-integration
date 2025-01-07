
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from statsmodels.tsa.holtwinters import ExponentialSmoothing

import func_common

def preprocessing_data(data):
    data['travel_date'] = pd.to_datetime(data['travel_date'])
    return data

def forecast_covid(data):

    # Streamlit App Layout
    st.title("Covid Recovery: Tourism Trends and Forecast")
    st.write("This application analyzes historical tourism data from 2019 to 2023 and forecasts trends for 2024–2026.")

    data = preprocessing_data(data)

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
    forecast_data = pd.DataFrame({
        'year': forecast_years,
        'forecast_tourists': forecast_tourists,
        'forecast_revenue': forecast_revenue
    })

    # Display Historical Data
    st.subheader("Historical Data (2019–2023)")
    st.write(annual_data)

    # Display Forecast Data
    st.subheader("Forecast Data (2024–2026)")
    st.write(forecast_data)

    # Plot Tourist Numbers Forecast
    st.subheader("Tourist Numbers Forecast")
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    ax1.plot(annual_data['year'], annual_data['no_tourist_all'], label='Historical Tourists', marker='o')
    ax1.plot(forecast_data['year'], forecast_data['forecast_tourists'], label='Forecast Tourists', marker='o')
    ax1.set_title('Tourist Numbers Forecast')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Number of Tourists')
    ax1.legend()
    ax1.grid()
    ax1.yaxis.set_major_formatter(ticker.FuncFormatter(func_common.millions_formatter))
    st.pyplot(fig1)

    # Plot Revenue Forecast
    st.subheader("Revenue Forecast")
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    ax2.plot(annual_data['year'], annual_data['revenue_all'], label='Historical Revenue', marker='o')
    ax2.plot(forecast_data['year'], forecast_data['forecast_revenue'], label='Forecast Revenue', marker='o')
    ax2.set_title('Revenue Forecast')
    ax2.set_xlabel('Year')
    ax2.set_ylabel('Revenue (in Baht)')
    ax2.legend()
    ax2.grid()
    ax2.yaxis.set_major_formatter(ticker.FuncFormatter(func_common.billions_formatter))
    st.pyplot(fig2)

    st.header("AI Integration")
    st.write("Uses Exponential Smoothing for accurate time-series forecasting.")


    st.subheader("Exponential Smoothing")
    st.write("**Exponential Smoothing** is a widely used forecasting method for time-series data due to its simplicity, efficiency, and ability to capture trends and seasonality. Here's why it was chosen for the analysis and forecasting of post-pandemic recovery trends in tourist numbers and revenue:")

    st.write("**1. Ability to Handle Trends**")
    st.write("Exponential Smoothing is particularly effective at capturing trends in time-series data. For the dataset provided, which spans 2019–2023, the data exhibits clear trends influenced by the COVID-19 pandemic (sharp declines in 2020–2021) and subsequent recovery (2022–2023). The method adjusts forecasts based on recent changes, making it suitable for tracking recovery patterns.")

    st.write("**2. Flexibility in Model Selection**")
    st.write("There are different types of Exponential Smoothing models:")
    st.markdown("- :blue-background[Simple Exponential Smoothing:] For data without a trend or seasonality.")
    st.markdown("- :blue-background[Holt's Linear Trend Method:] For data with a trend (used here for both tourist numbers and revenue).")
    st.markdown("- :blue-background[Holt-Winters Seasonal Method:] For data with both trend and seasonality.")
    st.write("In this case, Holt's method was appropriate because the dataset showed a clear trend but lacked strong seasonality over the years analyzed.")

    st.write("**3. Responsiveness to Recent Data**")
    st.write("Exponential Smoothing gives more weight to recent observations, making it highly responsive to abrupt changes like those caused by the pandemic. This ensures that the model adapts quickly to shifts in trends during recovery periods, such as the rebound seen in 2022–2023.")

    st.write("**4. Simplicity and Interpretability**")
    st.write("Compared to more complex machine learning models, Exponential Smoothing is computationally efficient and easy to implement. It provides interpretable results, which are crucial for understanding post-pandemic recovery dynamics.")

    st.write("**5. Suitable for Short-Term Forecasting**")
    st.write("Exponential Smoothing is ideal for short- to medium-term forecasting (e.g., 2024–2026 in this case). It balances accuracy with simplicity without overfitting the data.")

    st.write("**6. Practical Application**")
    st.write("The attached charts (Tourist Numbers Forecast and Revenue Forecast) illustrate how Exponential Smoothing has been applied:")
    st.markdown("- :blue-background[Tourist Numbers Forecast:] Shows a declining trend for 2024–2026 after a partial recovery in 2023.")
    st.markdown(" - :blue-background[Revenue Forecast:] Reflects similar dynamics, with revenues stabilizing at lower levels compared to pre-pandemic highs.")
    st.write("These forecasts align with real-world expectations, where the tourism sector may face challenges like economic uncertainties or slower-than-expected international travel recovery.")

    st.write("In summary, Exponential Smoothing was chosen because it effectively captures trends, adapts to recent changes, and provides reliable short-term forecasts while being computationally efficient and easy to interpret.")