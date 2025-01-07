import numpy as np
import streamlit as st
import pandas as pd

def query_tourist_data(data):
    query_data = data[(data["variable"] == "no_tourist_all") | (data["variable"] == "no_tourist_foreign") | (data["variable"] == "no_tourist_thai")]
    return query_data

def query_revenue_date(data):
    query_data = data[(data["variable"] == "revenue_all") | (data["variable"] == "revenue_foreign") | (data["variable"] == "revenue_thai")]
    return query_data

def sum_value_by_region(data):
    regional_data = data.groupby(['region_eng','variable']).agg({
        'value': 'sum'
    }).reset_index()
    return regional_data

def sum_value_by_province(data):
    regional_data = data.groupby(['province_eng','variable']).agg({
        'value': 'sum'
    }).reset_index()
    return regional_data

# Preprocess data for regional aggregation
def sum_by_region(data):
    regional_data = data.groupby('region_eng').agg({
        'no_tourist_all': 'sum',
        'no_tourist_foreign': 'sum',
        'no_tourist_thai': 'sum',
        'revenue_all': 'sum',
        'revenue_foreign': 'sum',
        'revenue_thai': 'sum'
    }).reset_index()
    return regional_data

def add_display_region_column(data):
    # Change region name to be display name
    data["display_region"] = np.where(data['region_eng'] == "central","Central", data['region_eng'])
    data["display_region"] = np.where(data['region_eng'] == "east","East", data['display_region'])
    data["display_region"] = np.where(data['region_eng'] == "east_northeast","Northeast", data['display_region'])
    data["display_region"] = np.where(data['region_eng'] == "north","North", data['display_region'])
    data["display_region"] = np.where(data['region_eng'] == "south","South", data['display_region'])
    return data

def add_order_type_column(data):
    data["order_type"] = np.where(data['variable'] == "revenue_all", 3, np.where(data['variable'] == "revenue_thai", 1, 2))
    return data

def add_display_tourist_variable_column(data):
    data["display_variable"] = np.where(data['variable'] == "no_tourist_all", 'All tourists', np.where(data['variable'] == "no_tourist_thai", 'Thai tourists', 'Foreign tourists'))
    return data

def add_display_revenue_variable_column(data):
    data["display_variable"] = np.where(data['variable'] == "revenue_all", 'Revenue from all tourists', np.where(data['variable'] == "revenue_thai", 'Revenue from Thai tourists', 'Revenue from foreign tourists'))
    return data

def sum_by_region_tourist(data):

    query_data = query_tourist_data(data)
    regional_data = sum_value_by_region(query_data)

    regional_data = add_order_type_column(regional_data)
    regional_data = add_display_tourist_variable_column(regional_data)

    # Change region name to be display name
    regional_data = add_display_region_column(regional_data)

    regional_data = regional_data.sort_values(["region_eng","order_type"])

    # Drop unnenessary columns
    regional_data.drop(['variable','order_type','region_eng'],axis='columns', inplace=True)
    
    # Reorder column
    regional_data = regional_data.loc[:, ['display_region', 'display_variable', 'value']]

    return regional_data

def sum_by_region_revenue(data):

    query_data = query_revenue_date(data)
    regional_data = sum_value_by_region(query_data)

    regional_data = add_order_type_column(regional_data)
    # regional_data["display_variable"] = np.where(regional_data['variable'] == "revenue_all", 'Revenue from all tourists', np.where(regional_data['variable'] == "revenue_thai", 'Revenue from Thai tourists', 'Revenue from foreign tourists'))
    regional_data = add_display_revenue_variable_column(regional_data)

    # Change region name to be display name
    regional_data = add_display_region_column(regional_data)

    regional_data = regional_data.sort_values(["region_eng","order_type"])

    # Drop unnenessary columns
    regional_data.drop(['variable','order_type','region_eng'],axis='columns', inplace=True)
    
    # Reorder column
    regional_data = regional_data.loc[:, ['display_region', 'display_variable', 'value']]
    
    return regional_data

def sum_by_province_tourist(data):

    query_data = query_tourist_data(data)
    province_data = sum_value_by_province(query_data)
    return province_data

def sum_by_province_revenue(data):

    query_data = query_revenue_date(data)
    province_data = sum_value_by_province(query_data)
    return province_data

def sum_by_province_top_tourist(data,top):
    query_data = data[(data["variable"] == "no_tourist_all")]
    province_data = sum_value_by_province(query_data)
    province_data = province_data.nlargest(top, 'value')
    return province_data

def sum_by_province_top_revenue(data,top):

    query_data = data[(data["variable"] == "revenue_all")]
    province_data = sum_value_by_province(query_data)
    province_data = province_data.nlargest(top, 'value')
    return province_data

def melted_tourist_revenue(merged_data,key_column):
    melted_data = pd.melt(merged_data, id_vars=[key_column], var_name='variable', value_name='value')
    return melted_data

def merge_province_by_top_tourist(data,top):

    # Manipulate no tourist all data frame with top records
    tourist_data = data[(data["variable"] == "no_tourist_all")]
    tourist_data = sum_value_by_province(tourist_data)
    tourist_data = tourist_data.nlargest(top, 'value')
    tourist_data = tourist_data.rename(columns={'value':'no_tourist_all'})
    tourist_data = tourist_data.drop(columns=['variable'])

    # Manipulate tourist all data frame all records
    revenue_data = data[(data["variable"] == "revenue_all")]
    revenue_data = sum_value_by_province(revenue_data)
    revenue_data = revenue_data.rename(columns={'value':'revenue_all'})
    revenue_data = revenue_data.drop(columns=['variable'])

    merged_data = pd.merge(tourist_data, revenue_data, on='province_eng', how='inner')
    melted_data = melted_tourist_revenue(merged_data,'province_eng')

    st.write(melted_data)
    melted_data["display_variable"] = np.where(melted_data['variable'] == "no_tourist_all", 'Tourist numbers', 'Revenue')

    return melted_data