# Re-aggregate data by month for forecasting
monthly_data = data.resample('M').sum()

# Prepare data for linear regression forecasting
revenue_series = monthly_data['revenue_all'].reset_index()
revenue_series['time_index'] = np.arange(len(revenue_series))

# Define features and target
X = revenue_series[['time_index']]
y = revenue_series['revenue_all']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=False)

# Train the linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict future values
future_time_index = np.arange(len(revenue_series), len(revenue_series) + 12).reshape(-1, 1)
forecast = model.predict(future_time_index)

# Plot the original data and forecast
plt.figure(figsize=(10, 6))
plt.plot(revenue_series['time_index'], revenue_series['revenue_all'], label='Original Data')
plt.plot(future_time_index, forecast, label='Forecast', color='red')
plt.legend()
plt.title('Revenue Forecast')
plt.xlabel('Time Index')
plt.ylabel('Revenue')
plt.grid()
plt.show()

forecast