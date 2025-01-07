import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns
import matplotlib.ticker as ticker

def billions_formatter(y, pos):
    # return f'{int(y/1e9)}B'
    return "{:,}B".format(int(y/1e9))

def millions_formatter(y, pos):
    return f'{int(y/1e6)}M'

def thousands_formatter(y, pos):
    return f'{int(y/1000)}k'

def hundred_thousands_formatter(y, pos):
    return f'{int(y/1000000)}'


def plot_region_distribution_bak(data,dataheader,graphheader,xlabel,ylabel,xformat = "million"):

    # Display aggregated data in a table
    st.subheader(dataheader)
    st.dataframe(data)

    # Display visualizations
    st.subheader(graphheader)

    fig, axes = plt.subplots()
    bar = sns.barplot(x='display_region', y='value', hue = "display_variable",data=data, ax=axes,palette="tab10")

    bar.set(xlabel = xlabel, ylabel = ylabel)

    if (xformat == "billion"):
        plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(billions_formatter))
        # Add labels to the bars with formatted numbers
        for bar in axes.patches:
            axes.text(
                bar.get_x() + bar.get_width() / 2, # X-coordinate (center of the bar)
                bar.get_height(),                  # Y-coordinate (top of the bar)
                f'{int(bar.get_height()/1e9)}B',   # Format the number with commas
                ha='center', va='bottom',          # Align the text
                fontsize=7                         # Set font size for the label
            )

    else:
        plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(millions_formatter))

        # Add labels to the bars with formatted numbers
        for bar in axes.patches:
            axes.text(
                bar.get_x() + bar.get_width() / 2, # X-coordinate (center of the bar)
                bar.get_height(),                  # Y-coordinate (top of the bar)
                f'{int(bar.get_height()/1e6)}M',   # Format the number with commas
                ha='center', va='bottom',          # Align the text
                fontsize=7                         # Set font size for the label
            )

    plt.legend(title='Legend')

    plt.tight_layout()
    st.pyplot(fig)

# Plot function for tourists and revenue distribution by region
def plot_region_distribution(data_tourist,data_revenue):

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # bar = sns.barplot(x='display_region', y='value', hue = "display_variable",data=data, ax=axes,palette="tab10")

    # Plot total tourists by region
    sns.barplot(x='display_region', y='value', hue = "display_variable",data=data_tourist, ax=axes[0], palette='tab10')
    axes[0].set_title('Regional Distribution by Tourists')
    axes[0].set_ylabel('Total Tourists (Million)')
    axes[0].set_xlabel('Region')
    axes[0].legend(title="Legend")
    axes[0].yaxis.set_major_formatter(ticker.FuncFormatter(millions_formatter))

    # Add labels to the bars with formatted numbers
    for bar in axes[0].patches:
        axes[0].text(
            bar.get_x() + bar.get_width() / 2, # X-coordinate (center of the bar)
            bar.get_height(),                  # Y-coordinate (top of the bar)
            f'{int(bar.get_height()/1e6)}M',   # Format the number with commas
            ha='center', va='bottom',          # Align the text
            fontsize=7                         # Set font size for the label
        )

    # Plot total revenue by region
    sns.barplot(x='display_region', y='value', hue = "display_variable", data=data_revenue, ax=axes[1], palette='pastel')
    axes[1].set_title('Regional Distribution by Revenue')
    axes[1].set_ylabel('Total Revenue (Billion Baht)')
    axes[1].set_xlabel('Region')
    axes[1].legend(title="Legend")
    axes[1].yaxis.set_major_formatter(ticker.FuncFormatter(billions_formatter))

    # Add labels to the bars with formatted numbers
    for bar in axes[1].patches:
        axes[1].text(
            bar.get_x() + bar.get_width() / 2,          # X-coordinate (center of the bar)
            bar.get_height(),                           # Y-coordinate (top of the bar)
            "{:,}B".format(int(bar.get_height()/1e9)),  # Format the number with commas
            ha='center', va='bottom',                   # Align the text
            fontsize=7                                  # Set font size for the label
        )

    plt.tight_layout()
    st.pyplot(fig)

# Plot function for tourists and revenue distribution by province
def plot_province_distribution(data_tourist,data_revenue):

    # Create tabs for Revenue and Tourist Numbers
    tab1, tab2 = st.tabs(["Tourist Numbers","Revenue"])

    with tab1:
        st.header("Top 10 Provinces by Tourist Numbers")
        
        st.write(data_tourist)

        # Create a bar plot using Seaborn
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(x='province_eng', y='value', data=data_tourist, ax=ax,color="blue")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
        ax.set_ylabel('Tourist Numbers')
        ax.set_title('Top 10 Provinces by Tourist Numbers')
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(millions_formatter))

        # Add labels to the bars with formatted numbers
        for bar in ax.patches:
            ax.text(
                bar.get_x() + bar.get_width() / 2, # X-coordinate (center of the bar)
                bar.get_height(),                  # Y-coordinate (top of the bar)
                f'{int(bar.get_height()/1e6)}M',   # Format the number with commas
                ha='center', va='bottom',          # Align the text
                fontsize=7                         # Set font size for the label
            )
        
        # Display the plot
        st.pyplot(fig)

    with tab2:
        st.header("Top 10 Provinces by Revenue")

        st.write(data_revenue)
        
        # Create a bar plot using Seaborn
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(x='province_eng', y='value', data=data_revenue, ax=ax,color="green")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
        ax.set_ylabel('Revenue')
        ax.set_title('Top 10 Provinces by Revenue')
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(billions_formatter))

        # Add labels to the bars with formatted numbers
        for bar in ax.patches:
            ax.text(
                bar.get_x() + bar.get_width() / 2,          # X-coordinate (center of the bar)
                bar.get_height(),                           # Y-coordinate (top of the bar)
                "{:,}B".format(int(bar.get_height()/1e9)),  # Format the number with commas
                ha='center', va='bottom',                   # Align the text
                fontsize=7                                  # Set font size for the label
            )
        
        # Display the plot
        st.pyplot(fig)