import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import openai
from statsmodels.tsa.arima.model import ARIMA
from dotenv import load_dotenv
import os
import time  # Import time module

# Load environment variables from .env file
load_dotenv()

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv('../data/thailand_domestic_tourism.csv')

data = load_data()

st.title('Thailand Domestic Tourism Analysis')

# Data preprocessing
data['travel_date'] = pd.to_datetime(data['travel_date'])
data['year'] = data['travel_date'].dt.year

# Basic statistics
st.header('Basic Statistics')
tourists_by_region = data.groupby('region_eng')['no_tourist_all'].sum()
revenue_by_region = data.groupby('region_eng')['revenue_all'].sum()

col1, col2 = st.columns(2)

with col1:
    st.subheader('Total Tourists by Region')
    st.bar_chart(tourists_by_region)

with col2:
    st.subheader('Total Revenue by Region')
    st.bar_chart(revenue_by_region)

# Time series analysis
st.header('Time Series Analysis')
yearly_data = data.groupby('year').agg({'no_tourist_all': 'sum', 'revenue_all': 'sum'})

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(yearly_data.index, yearly_data['no_tourist_all'], marker='o')
ax.set_xlabel('Year')
ax.set_ylabel('Number of Tourists')
ax.set_title('Yearly Tourist Numbers')
st.pyplot(fig)

# ARIMA Forecasting
st.header('ARIMA Forecasting')
model = ARIMA(yearly_data['no_tourist_all'], order=(1,1,1))
results = model.fit()
forecast = results.forecast(steps=3)

st.write("Forecasted tourist numbers for the next 3 years:")
st.write(forecast)

# AI-powered insights
st.header('AI-Powered Insights')

prompt = f"""
Analyze the following tourism data and provide insights:
Total tourists by region: {tourists_by_region.to_dict()}
Total revenue by region: {revenue_by_region.to_dict()}
Yearly tourist numbers: {yearly_data['no_tourist_all'].to_dict()}

Provide 3-5 key insights about the tourism trends in Thailand based on this data.
"""


# response = openai.Completion.create(
#    engine="gpt-3.5-turbo",
#    prompt=prompt,
#    max_tokens=200,
#    n=1,
#    stop=None,
#    temperature=0.7,
#)


response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": prompt}
    ],
    max_tokens=200,
    n=1,
    stop=None,
    temperature=0.7,
)

# Accessing the content correctly
st.write(response.choices[0].message['content'].strip())

# User input for specific analysis
st.header('Custom Analysis')
user_question = st.text_input("Ask a question about the tourism data:")

if user_question:
    ai_prompt = f"Based on the Thailand tourism data provided earlier, answer the following question: {user_question}"
    
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.7,
    )

    # Accessing the content correctly
    st.write(response.choices[0].message['content'].strip())