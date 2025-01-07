import streamlit as st
import streamlit as st
from annotated_text import annotated_text

import func_common
import exploratory
import forecast
import insights
import aiintegration

# Main function to run the analysis and get insights from Gemini API
def main():

    # Load the CSV file
    data = func_common.load_domestic_tourist_org_csv()
    data_cleansing = func_common.load_domestic_tourist_csv()

    with st.sidebar:
        st.title("Menu")
        page = st.radio("", ["Dataset", "Regional Distribution", 
                             "Top Performing Provinces","Covid Analysis Insights (2019-2023)", 
                             "Covid Recovery: Tourism Trends and Forecast",
                             "OpenAI Integration"])

    match page:
        case "Dataset":
            # Set up the Streamlit app
            st.title('Thailand Domestic Tourism 2019-2022')
            st.write(data)
            st.subheader("Insight")
            annotated_text(
                ("Foreign vs. Domestic Tourists ","Dataset"), 
                "The presence of separate columns for foreign and Thai tourists indicates the importance of both markets to Thailand's tourism indoustry.")
            
        case "Regional Distribution":
            st.title('Regional Distribution')
            exploratory.visualize_region(data)

        case "Top Performing Provinces":
            st.title('Top Performing Provinces')
            exploratory.visualize_top_province(data)

        case "Covid Analysis Insights (2019-2023)":
            insights.insights_covid(data_cleansing)

        case "Covid Recovery: Tourism Trends and Forecast":
            forecast.forecast_covid(data_cleansing)

        case "OpenAI Integration":
            aiintegration.integrate_openai(data_cleansing)

if __name__ == "__main__":
    main()