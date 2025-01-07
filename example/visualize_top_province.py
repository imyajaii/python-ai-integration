import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the data
@st.cache_data
def load_data():
    data = pd.read_csv('../data/thailand_domestic_tourism_original.csv')
    return data

data = load_data()

st.write(data)

# Set up the Streamlit app
st.title('Top Performing Provinces in Thailand')

# Create tabs for Revenue and Tourist Numbers
tab1, tab2 = st.tabs(["Revenue", "Tourist Numbers"])

with tab1:
    st.header("Top 10 Provinces by Revenue")
    
    # Filter data for revenue
    revenue_data = data[data['variable'] == 'revenue_all'].sort_values('value', ascending=False)
    top_10_revenue = revenue_data.head(10)
    
    # Create a bar plot using Seaborn
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x='province_eng', y='value', data=top_10_revenue, ax=ax)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    ax.set_ylabel('Revenue')
    ax.set_title('Top 10 Provinces by Revenue')
    
    # Display the plot
    st.pyplot(fig)

with tab2:
    st.header("Top 10 Provinces by Tourist Numbers")
    
    # Filter data for tourist numbers (assuming 'ratio_tourist_stay' represents tourist numbers)
    tourist_data = data[data['variable'] == 'ratio_tourist_stay'].sort_values('value', ascending=False)
    top_10_tourists = tourist_data.head(10)
    
    # Create a bar plot using Seaborn
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x='province_eng', y='value', data=top_10_tourists, ax=ax)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    ax.set_ylabel('Tourist Numbers')
    ax.set_title('Top 10 Provinces by Tourist Numbers')
    
    # Display the plot
    st.pyplot(fig)

# Add a note about the data
st.sidebar.markdown("""
    **Note:** This visualization is based on the available data in the CSV file. 
    'revenue_all' is used for revenue, and 'ratio_tourist_stay' is assumed to represent tourist numbers.
    """)