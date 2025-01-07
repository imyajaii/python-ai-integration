import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load and preprocess the data
@st.cache_data
def load_data():
    df = pd.read_csv('../data/thailand_domestic_tourism.csv')
    df['travel_date'] = pd.to_datetime(df['travel_date'])
    df['year'] = df['travel_date'].dt.year
    return df

df = load_data()

st.title("Thai Domestic Tourism: Post-Pandemic Recovery Analysis (2019-2023)")

# Sidebar for filtering
st.sidebar.header("Filters")
selected_regions = st.sidebar.multiselect("Select Regions", df['region_eng'].unique(), default=df['region_eng'].unique())
selected_years = st.sidebar.multiselect("Select Years", sorted(df['year'].unique()), default=sorted(df['year'].unique()))

# Filter data based on selection
filtered_df = df[(df['region_eng'].isin(selected_regions)) & (df['year'].isin(selected_years))]

# Aggregate data by year
yearly_data = filtered_df.groupby('year').agg({
    'no_tourist_all': 'sum',
    'revenue_all': 'sum'
}).reset_index()

# Visualizations
st.header("Overall Trends")

# Tourist Numbers Trend
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=yearly_data, x='year', y='no_tourist_all', marker='o')
ax.set_title("Total Tourist Numbers by Year")
ax.set_ylabel("Number of Tourists")
st.pyplot(fig)

# Revenue Trend
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=yearly_data, x='year', y='revenue_all', marker='o')
ax.set_title("Total Revenue by Year")
ax.set_ylabel("Revenue (Thai Baht)")
st.pyplot(fig)

# Regional Analysis
st.header("Regional Analysis")

# Regional Tourist Numbers
regional_data = filtered_df.groupby(['year', 'region_eng'])['no_tourist_all'].sum().reset_index()
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(data=regional_data, x='year', y='no_tourist_all', hue='region_eng', marker='o')
ax.set_title("Tourist Numbers by Region")
ax.set_ylabel("Number of Tourists")
plt.legend(title="Region", bbox_to_anchor=(1.05, 1), loc='upper left')
st.pyplot(fig)

# Regional Revenue
regional_revenue = filtered_df.groupby(['year', 'region_eng'])['revenue_all'].sum().reset_index()
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(data=regional_revenue, x='year', y='revenue_all', hue='region_eng', marker='o')
ax.set_title("Revenue by Region")
ax.set_ylabel("Revenue (Thai Baht)")
plt.legend(title="Region", bbox_to_anchor=(1.05, 1), loc='upper left')
st.pyplot(fig)

# Top 10 Provinces by Tourist Numbers in the Latest Year
st.header("Top 10 Provinces by Tourist Numbers (Latest Year)")
latest_year = filtered_df['year'].max()
top_provinces = filtered_df[filtered_df['year'] == latest_year].groupby('province_eng')['no_tourist_all'].sum().nlargest(10).reset_index()
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=top_provinces, x='province_eng', y='no_tourist_all')
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
ax.set_title(f"Top 10 Provinces by Tourist Numbers in {latest_year}")
ax.set_ylabel("Number of Tourists")
st.pyplot(fig)

# Recovery Rate Analysis
st.header("Recovery Rate Analysis")
base_year = 2019
recovery_data = filtered_df.groupby(['year', 'region_eng'])['no_tourist_all'].sum().reset_index()
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
