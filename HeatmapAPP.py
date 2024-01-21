# import streamlit as st
# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt
# import fathon
# from fathon import fathonUtils as fu

# # Function to filter DataFrame based on start and end date
# def filter_dataframe_by_date(df, start_date, end_date):
#     return df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

# # Function to compute correlation matrix
# def compute_correlation_matrix(df):
#     df_filtered = df.drop(columns=['Date'])
#     rho_corr = []
#     for i in df_filtered.columns:
#         rho_corr_temp = []
#         for j in df_filtered.columns:
#             if i != j:
#                 a = df_filtered[i]
#                 b = df_filtered[j]
#                 # zero-mean cumulative sum
#                 a = fu.toAggregated(a)
#                 b = fu.toAggregated(b)
#                 # initialize non-empty dcca object
#                 pydcca = fathon.DCCA(a, b)
#                 # compute rho index
#                 n, rho = pydcca.computeRho(fu.linRangeByStep(20, 21, step=1))
#                 rho_corr_temp.append(rho[0])
#             if i == j:
#                 rho_corr_temp.append(1)
#         rho_corr.append(rho_corr_temp)
#     return rho_corr

# # Streamlit App
# def main():
#     st.title("Correlation Heatmap")

#     # Load data
#     df_dat = pd.read_excel('CommodityC.xlsx', sheet_name="Data")
#     df_dat['Date'] = pd.to_datetime(df_dat['Date'], format='%d-%m-%Y')

#     # Sidebar inputs
#     st.sidebar.subheader("Select Date Range")
#     start_date_input = st.sidebar.date_input("Start Date", value=df_dat['Date'].min())
#     end_date_input = st.sidebar.date_input("End Date", value=df_dat['Date'].max())

#     # Convert Streamlit date input to pandas Timestamp
#     start_date = pd.Timestamp(start_date_input)
#     end_date = pd.Timestamp(end_date_input)

#     # Filter data based on selected date range
#     df_filtered = filter_dataframe_by_date(df_dat, start_date, end_date)

#     # Compute correlation matrix
#     rho_corr = compute_correlation_matrix(df_filtered)

#     # Create heatmap
#     plt.figure(figsize=(18, 18))
#     x_labels = df_filtered.drop(columns=['Date']).columns
#     y_labels = df_filtered.drop(columns=['Date']).columns
#     ax = sns.heatmap(rho_corr, annot=True, cmap=sns.color_palette("cubehelix", as_cmap=True), xticklabels=x_labels, yticklabels=y_labels)

#     for text in ax.texts:
#         if float(text.get_text()) < 0.0:
#             text.set_color('crimson')
#             text.set_weight('bold')

#     # Display heatmap
#     st.pyplot(plt)

# if __name__ == "__main__":
#     main()

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import fathon
from fathon import fathonUtils as fu

# Function to filter DataFrame based on start and end date
def filter_dataframe_by_date(df, start_date, end_date):
    return df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

# Function to compute correlation matrix
def compute_correlation_matrix(df):
    df_filtered = df.drop(columns=['Date'])
    rho_corr = []
    for i in df_filtered.columns:
        rho_corr_temp = []
        for j in df_filtered.columns:
            if i != j:
                a = df_filtered[i]
                b = df_filtered[j]
                # zero-mean cumulative sum
                a = fu.toAggregated(a)
                b = fu.toAggregated(b)
                # initialize non-empty dcca object
                pydcca = fathon.DCCA(a, b)
                # compute rho index
                n, rho = pydcca.computeRho(fu.linRangeByStep(20, 21, step=1))
                rho_corr_temp.append(rho[0])
            if i == j:
                rho_corr_temp.append(1)
        rho_corr.append(rho_corr_temp)
    return rho_corr

# Streamlit App
def main():
    st.title("Correlation Heatmap")

    # Load data
    df_dat = pd.read_excel('CommodityC.xlsx', sheet_name="Data")
    df_dat['Date'] = pd.to_datetime(df_dat['Date'], format='%d-%m-%Y')

    # Sidebar inputs with date range limits
    st.sidebar.subheader("Select Date Range")
    start_date_input = st.sidebar.date_input("Start Date", value=pd.to_datetime('1-1-2018', format='%d-%m-%Y'), min_value=pd.to_datetime('1-1-1988', format='%d-%m-%Y'), max_value=pd.to_datetime('1-1-2048', format='%d-%m-%Y'))
    end_date_input = st.sidebar.date_input("End Date", value=pd.to_datetime('1-1-2020', format='%d-%m-%Y'), min_value=pd.to_datetime('1-1-1988', format='%d-%m-%Y'), max_value=pd.to_datetime('1-1-2048', format='%d-%m-%Y'))

    # Convert Streamlit date input to pandas Timestamp
    start_date = pd.Timestamp(start_date_input)
    end_date = pd.Timestamp(end_date_input)

    # Filter data based on selected date range
    df_filtered = filter_dataframe_by_date(df_dat, start_date, end_date)

    # Compute correlation matrix
    rho_corr = compute_correlation_matrix(df_filtered)

    # Create heatmap
    plt.figure(figsize=(18, 18))
    x_labels = df_filtered.drop(columns=['Date']).columns
    y_labels = df_filtered.drop(columns=['Date']).columns
    ax = sns.heatmap(rho_corr, annot=True, cmap=sns.color_palette("cubehelix", as_cmap=True), xticklabels=x_labels, yticklabels=y_labels)

    for text in ax.texts:
        if float(text.get_text()) < 0.0:
            text.set_color('crimson')
            text.set_weight('bold')

    # Display heatmap
    st.pyplot(plt)

if __name__ == "__main__":
    main()
