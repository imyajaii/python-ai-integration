import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from google.cloud import bigquery
from google.cloud import storage

# Initialize Google Cloud services
def initialize_gcp():
    client = bigquery.Client()
    storage_client = storage.Client()
    return client, storage_client

# Load data from CSV
def load_data():
    return pd.read_csv('../data/thailand_domestic_tourism.csv')

# Upload data to Google Cloud Storage
def upload_to_gcs(storage_client, bucket_name, source_file_name, destination_blob_name):
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    st.success(f"File {source_file_name} uploaded to {destination_blob_name}.")

# Submit batch prediction job using Gemini API
def submit_gemini_batch_prediction(input_uri, output_uri):
    from vertexai.batch_prediction import BatchPredictionJob
    from vertexai import init

    PROJECT_ID = "gen-lang-client-0934252543"
    LOCATION = "us-central1"
    MODEL_NAME = "publishers/google/models/gemini-1.5-flash-002"

    init(project=PROJECT_ID, location=LOCATION)

    batch_prediction_job = BatchPredictionJob.submit(
        display_name="tourism_forecast",
        model=MODEL_NAME,
        input_config={"instancesFormat": "jsonl", "gcsSource": {"uris": [input_uri]}},
        output_config={"predictionsFormat": "jsonl", "gcsDestination": {"outputUriPrefix": output_uri}},
    )

    st.write(f"Batch prediction job submitted: {batch_prediction_job.resource_name}")
    return batch_prediction_job

# Main Streamlit App
st.title("Thailand Domestic Tourism Forecast")
st.sidebar.header("Options")

# Load and display data
data = load_data()
st.subheader("Historical Data")
st.write(data.head())

data['travel_date'] = pd.to_datetime(data['travel_date'])
data['year'] = data['travel_date'].dt.year

# Plot trends
st.subheader("Tourism Trends (2019–2023)")
fig, ax1 = plt.subplots(figsize=(10, 6))
ax2 = ax1.twinx()

ax1.bar(data['year'], data['no_tourist_all'], color='blue', alpha=0.7, label='Tourists')
ax2.plot(data['year'], data['revenue_all'], color='red', marker='o', label='Revenue')

ax1.set_xlabel('Year')
ax1.set_ylabel('Number of Tourists', color='blue')
ax2.set_ylabel('Revenue (THB)', color='red')
plt.title("Trends in Domestic Tourism")
st.pyplot(fig)

# Upload data to GCS and trigger Gemini prediction
if st.sidebar.button("Upload Data & Predict"):
    client, storage_client = initialize_gcp()
    
    # Upload CSV to GCS
    bucket_name = "your-gcs-bucket"
    source_file_name = "thailand_domestic_tourism.csv"
    destination_blob_name = "tourism_data.csv"
    
    upload_to_gcs(storage_client, bucket_name, source_file_name, destination_blob_name)
    
    # Submit batch prediction job
    input_uri = f"gs://{bucket_name}/{destination_blob_name}"
    output_uri = f"gs://{bucket_name}/predictions/"
    
    job = submit_gemini_batch_prediction(input_uri, output_uri)
    
    st.info(f"Prediction job submitted: {job.resource_name}")

# Display insights
st.subheader("Key Insights")
st.write("""
1. Domestic tourism saw significant fluctuations due to COVID-19.
2. Revenue recovery is slower than tourist numbers.
3. Forecasts predict steady growth in tourism post-pandemic.
""")

# Recommendations
st.subheader("Recommendations")
st.write("""
1. Target marketing campaigns in high-revenue regions like Bangkok and Phuket.
2. Develop tourism infrastructure in underperforming regions.
3. Monitor external factors like global economic conditions and pandemics.
""")
