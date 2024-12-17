import streamlit as st
import pandas as pd
import plotly.express as px

# Load the recommendation and customer data
@st.cache_data
def load_data():
    # Load datasets
    customer_data_cleaned = pd.read_csv("models/customer_data_cleaned.csv")
    recommendations = pd.read_csv("models/customer_recommendations.csv")
    return customer_data_cleaned, recommendations

# Load data
customer_data_cleaned, recommendations = load_data()

# Title of the dashboard
st.title("Customer Recommendation System Dashboard")

# Sidebar Filters
st.sidebar.header("Filter Options")
clusters = sorted(recommendations['cluster'].unique())
selected_cluster = st.sidebar.selectbox("Select Cluster", clusters)

# Filtered data for the selected cluster
cluster_data = recommendations[recommendations['cluster'] == selected_cluster]

# Display cluster summary
st.subheader(f"Cluster {selected_cluster} Summary")
st.write(f"Number of customers in Cluster {selected_cluster}: {len(cluster_data)}")

# Allow input of Customer ID
selected_customer = st.sidebar.text_input("Enter Customer ID (Optional):")

if selected_customer:
    try:
        selected_customer = float(selected_customer)  # Convert input to float
        customer_recommendation = cluster_data[cluster_data['CustomerID'] == selected_customer]
        if not customer_recommendation.empty:
            st.subheader(f"Recommendations for Customer ID: {selected_customer}")
            st.write("**Top 3 Recommended Products:**")
            st.write(f"1. {customer_recommendation['Rec1_Description'].values[0]} "
                     f"(StockCode: {customer_recommendation['Rec1_StockCode'].values[0]})")
            st.write(f"2. {customer_recommendation['Rec2_Description'].values[0]} "
                     f"(StockCode: {customer_recommendation['Rec2_StockCode'].values[0]})")
            st.write(f"3. {customer_recommendation['Rec3_Description'].values[0]} "
                     f"(StockCode: {customer_recommendation['Rec3_StockCode'].values[0]})")
        else:
            st.warning("No recommendations found for this Customer ID.")
    except ValueError:
        st.error("Invalid Customer ID. Please enter a valid number.")
else:
    st.write("Enter a Customer ID to get personalized recommendations.")

# Display top recommendations for the selected cluster
st.subheader(f"Top Recommendations for Cluster {selected_cluster}")
top_products = cluster_data[['Rec1_Description', 'Rec2_Description', 'Rec3_Description']].melt(
    var_name='Recommendation', value_name='Product'
)
top_products_count = top_products['Product'].value_counts().reset_index()
top_products_count.columns = ['Product', 'Count']

# Bar chart for top products
fig = px.bar(top_products_count.head(10), x='Count', y='Product', orientation='h', title="Top Recommended Products")
st.plotly_chart(fig)
