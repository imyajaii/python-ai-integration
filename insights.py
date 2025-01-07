import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as ticker

import func_common

def preprocessing_data(data):
    data['travel_date'] = pd.to_datetime(data['travel_date'])
    data['year'] = data['travel_date'].dt.year
    return data

def insights_covid(data):
    st.title("Covid Analysis Insights (2019-2023)")

    data = preprocessing_data(data)

    # Aggregate data by year
    yearly_data = data.groupby('year').agg({
        'no_tourist_all': 'sum',
        'revenue_all': 'sum'
    }).reset_index()

    # Visualizations
    st.header("Overall Trends")

    # Tourist Numbers Trend
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=yearly_data, x='year', y='no_tourist_all', marker='o')
    ax.set_title("Total Tourist Numbers by Year")
    ax.set_ylabel("Number of Tourists (M:Million)")
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(func_common.millions_formatter))

    st.pyplot(fig)

    # Revenue Trend
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=yearly_data, x='year', y='revenue_all', marker='o')
    ax.set_title("Total Revenue by Year")
    ax.set_ylabel("Revenue (Thai Baht)")
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(func_common.billions_formatter))
    st.pyplot(fig)

    # Top 10 Provinces by Tourist Numbers in the Latest Year
    st.header("Top 10 Provinces by Tourist Numbers (Latest Year)")
    latest_year = data['year'].max()
    top_provinces = data[data['year'] == latest_year].groupby('province_eng')['no_tourist_all'].sum().nlargest(10).reset_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=top_provinces, x='province_eng', y='no_tourist_all')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    ax.set_title(f"Top 10 Provinces by Tourist Numbers in {latest_year}")
    ax.set_ylabel("Number of Tourists")
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(func_common.millions_formatter))
    st.pyplot(fig)

    # Recovery Rate Analysis
    st.header("Recovery Rate Analysis")
    base_year = 2019
    recovery_data = data.groupby(['year', 'region_eng'])['no_tourist_all'].sum().reset_index()
    recovery_data = recovery_data.pivot(index='region_eng', columns='year', values='no_tourist_all').reset_index()
    recovery_data['Recovery Rate'] = recovery_data[latest_year] / recovery_data[base_year] * 100
    recovery_data = recovery_data.sort_values('Recovery Rate', ascending=False)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=recovery_data, x='region_eng', y='Recovery Rate')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    ax.set_title(f"Tourism Recovery Rate by Region ({base_year} vs {latest_year})")
    ax.set_ylabel("Recovery Rate (%)")
    ax.axhline(y=100, color='r', linestyle='--')
    st.pyplot(fig)

    # Insights and Observations
    st.header("Key Insights")
    st.write("""
    1. The COVID-19 pandemic caused a significant drop in tourist numbers and revenue in 2020 and 2021.
    2. A recovery trend is observed starting from 2022, with varying rates across regions.
    3. Some regions have shown faster recovery rates than others, potentially due to domestic tourism preferences or local policies.
    4. The top provinces by tourist numbers in the latest year may indicate shifting travel patterns post-pandemic.
    5. Overall, the tourism industry has not yet fully recovered to pre-pandemic levels, but shows signs of improvement.
    """)

    st.header("Recommendations")
    st.write("""
    1. Focus on promoting domestic tourism in regions with slower recovery rates.
    2. Investigate successful strategies employed by fast-recovering regions and provinces.
    3. Develop targeted marketing campaigns for top-performing provinces to maintain their appeal.
    4. Implement safety measures and communicate them effectively to boost traveler confidence.
    5. Consider developing new tourism products or experiences that cater to changed traveler preferences post-pandemic.
    """)