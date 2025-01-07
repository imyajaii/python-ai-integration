import func_common
import func_preprocessing
import func_visualization

import streamlit as st
from annotated_text import annotated_text

def visualize_region(data):
    # Regional Analysis

    ## Aggregated Regional Data By No of Tourists
    sum_by_tourist_regional_data = func_preprocessing.sum_by_region_tourist(data)

    ## Aggregated Regional Data By Revenue
    sum_by_revenue_regional_data = func_preprocessing.sum_by_region_revenue(data)

    col_tourist,col_revenue = st.columns(2)
    col_tourist.write(sum_by_tourist_regional_data)
    col_revenue.write(sum_by_revenue_regional_data)

    ## Plot function for tourists and revenue distribution by region
    func_visualization.plot_region_distribution(sum_by_tourist_regional_data,sum_by_revenue_regional_data)

    # Insights
    st.subheader("Insight")
    annotated_text(
        ("Regional Disparties: ","Region Distribution"), 
        "There's a significant gap between the central region and others in terms of tourist attraction and revenue generation, indication potential for development in other regions.")

def visualize_top_province(data):

    TOP_PROVINCE = 10

    # Top Performance Provinces
    ## Aggregated Province Data By No of Tourists
    sum_by_tourist_province_data = func_preprocessing.sum_by_province_top_tourist(data,TOP_PROVINCE)

    ## Aggregated Province Data By Revenue
    sum_by_revenue_province_data = func_preprocessing.sum_by_province_top_revenue(data,TOP_PROVINCE)

    ## Plot function for tourists and revenue distribution by province
    func_visualization.plot_province_distribution(sum_by_tourist_province_data,sum_by_revenue_province_data)

    # Insights
    st.subheader("Insight")
    annotated_text(
        ("Bangkok Dominance: ","Top Performing Province"), 
        "The capital city is the primary driver of Thailand's domestic tourism, leading in both tourist numbers and revenue generation.")
