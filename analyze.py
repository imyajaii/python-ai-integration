import pandas as pd
import streamlit as st
import plotly.express as px
import google.generativeai as genai
from dotenv import load_dotenv
import os
import threading

# Load CSV data into a DataFrame
def load_csv(file_path):
    return pd.read_csv(file_path)

def clean_data(data):
    # Convert travel_date to datetime
    data['travel_date'] = pd.to_datetime(data['travel_date'])
    return data

def get_summary(data):

    # Perform initial analysis
    summary = {
        'total_tourists': data['no_tourist_all'].sum(),
        'total_foreign_tourists': data['no_tourist_foreign'].sum(),
        'total_thai_tourists': data['no_tourist_thai'].sum(),
        'total_revenue': data['revenue_all'].sum(),
        'foreign_revenue': data['revenue_foreign'].sum(),
        'thai_revenue': data['revenue_thai'].sum(),
        'average_occupancy_rate': data['ratio_tourist_stay'].mean()
    }

    return summary

def group_summary(data):

    # Group by region for regional insights
    region_summary = data.groupby('region_eng').agg({
        'no_tourist_all': 'sum',
        'revenue_all': 'sum',
        'ratio_tourist_stay': 'mean'
    }).reset_index()

    # Group by province for top provinces
    province_summary = data.groupby('province_eng').agg({
        'no_tourist_all': 'sum',
        'revenue_all': 'sum',
        'ratio_tourist_stay': 'mean'
    }).reset_index()

    return region_summary,province_summary

def get_insights(data):
    summary = get_summary(data)
    province_summary,region_summary = group_summary(data)
    return summary, region_summary, province_summary

def display_streamlit_app(summary,region_summary,top_provinces_tourists,top_provinces_revenue):

    # Streamlit app setup
    st.title('Thailand Domestic Tourism Analysis (2019-2023)')

    # Display overall summary
    st.header('Overall Summary')
    st.write(summary)

    # Regional insights visualization
    st.header('Regional Insights')

    fig_region,fig_revenue,fig_top_tourists,fig_top_revenue = create_visualize(region_summary,top_provinces_tourists,top_provinces_revenue)

    # Export figures to HTML for visualization
    fig_region.write_html("region_tourists.html")
    fig_revenue.write_html("region_revenue.html")
    fig_top_tourists.write_html("top_provinces_tourists.html")
    fig_top_revenue.write_html("top_provinces_revenue.html")

def create_visualize(region_summary,top_provinces_tourists,top_provinces_revenue):
    fig_region = px.bar(region_summary, x='region_eng', y='no_tourist_all', title='Total Tourists by Region', labels={'no_tourist_all': 'Number of Tourists', 'region_eng': 'Region'})
    st.plotly_chart(fig_region)

    fig_revenue = px.bar(region_summary, x='region_eng', y='revenue_all', title='Total Revenue by Region', labels={'revenue_all': 'Revenue (THB)', 'region_eng': 'Region'})
    st.plotly_chart(fig_revenue)

    # Top provinces visualization
    st.header('Top Provinces by Tourists and Revenue')

    fig_top_tourists = px.bar(top_provinces_tourists, x='province_eng', y='no_tourist_all', title='Top Provinces by Tourists', labels={'no_tourist_all': 'Number of Tourists', 'province_eng': 'Province'})
    st.plotly_chart(fig_top_tourists)

    fig_top_revenue = px.bar(top_provinces_revenue, x='province_eng', y='revenue_all', title='Top Provinces by Revenue', labels={'revenue_all': 'Revenue (THB)', 'province_eng': 'Province'})
    st.plotly_chart(fig_top_revenue)

    return fig_region,fig_revenue,fig_top_tourists,fig_top_revenue

# Function to interact with Gemini API
def chat_with_gemini(prompt, result_container):
    model = genai.GenerativeModel('gemini-1.5-flash')
    chat = model.start_chat(history=[])

    try:
        response = chat.send_message(prompt)
        result_container.append(response.text)
    except Exception as e:
        result_container.append(f"An error occurred: {str(e)}")

def integrate_gemini(summary,region_summary,top_provinces_tourists,top_provinces_revenue):
    
    # Load environment variables from .env file
    load_dotenv()

    GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=GOOGLE_API_KEY)

    # Prepare the prompt for Gemini AI
    prompt = f"""
    Analyze the following tourism data and provide key insights:

    Overall Summary:
    {summary}

    Regional Insights:
    {region_summary.to_string()}

    Top Provinces by Tourists:
    {top_provinces_tourists.to_string()}

    Top Provinces by Revenue:
    {top_provinces_revenue.to_string()}
    """

    # Generate insights using Gemini AI
    result_container = []

    # Start a thread to handle the API call
    thread = threading.Thread(target=chat_with_gemini, args=(prompt, result_container))
    thread.start()

    # Wait for the thread to complete with a timeout
    thread.join(timeout=1000)  # Set your desired timeout here

    if thread.is_alive():
        st.write("The request is taking too long. Please try again later.")
        thread.join()  # Optionally wait for the thread to finish if needed
    else:
        st.write("Gemini API Response:")
        st.write(result_container[0])

# Main function to run the analysis and get insights from Gemini API
def main():

    ### Analyze provided dataset on domestic tourism in thailand from Jan 2019 to Feb 2023

    # Load the CSV file
    csv_file_path = 'data/thailand_domestic_tourism.csv'
    data = load_csv(csv_file_path)

    # Clean data
    data = clean_data(data)

    # Get insights
    summary, province_summary,region_summary = get_insights(data)

    # Sort provinces by total tourists and revenue
    top_provinces_tourists = province_summary.sort_values(by='no_tourist_all', ascending=False).head(5)
    top_provinces_revenue = province_summary.sort_values(by='revenue_all', ascending=False).head(5)

    summary, region_summary, top_provinces_tourists, top_provinces_revenue

    ### Summarize the key insights derived from the analysis using Plotly and Streamlit
    display_streamlit_app(summary,region_summary,top_provinces_tourists,top_provinces_revenue)

    ### Integrate the analysis results with Gemini AI API
    integrate_gemini(summary,region_summary,top_provinces_tourists,top_provinces_revenue)

if __name__ == "__main__":
    main()