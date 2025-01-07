import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import streamlit as st
from conf import varconstant
from func import common


def main_forecast():

    # Load the CSV file
    data = common.load_csv(varconstant.csv_file_path_th_domestic_tour)
    data['travel_date'] = pd.to_datetime(data['travel_date'])

    # Aggregate data for time series forecasting
    time_series_data = data.groupby('travel_date').agg({
        'no_tourist_all': 'sum',
        'revenue_all': 'sum'
    }).reset_index()

    # Prepare data for forecasting
    X = time_series_data.index.values.reshape(-1, 1)  # Use time index as feature
    y_tourists = time_series_data['no_tourist_all']

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y_tourists, test_size=0.2, random_state=42)

    # Train Random Forest model
    rf_model = RandomForestRegressor(random_state=42)
    rf_model.fit(X_train, y_train)

    # Make predictions
    y_pred = rf_model.predict(X_test)

    # Calculate Mean Squared Error
    mse = mean_squared_error(y_test, y_pred)

    # Streamlit app
    st.title('Tourism Forecasting')

    # Display MSE
    st.write(f'Mean Squared Error: {mse}')

    # Forecast future values
    future_indices = np.arange(len(X), len(X) + 12).reshape(-1, 1)  # Forecast for the next 12 months
    future_predictions = rf_model.predict(future_indices)

    # Display predictions
    st.write('Future Predictions:')
    st.write(future_predictions)

### main ###
main_forecast()