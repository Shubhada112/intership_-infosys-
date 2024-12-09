import streamlit as st
import pandas as pd
from main import scrape_deals, get_deals
import time
import os

# Streamlit app configuration
st.set_page_config(page_title="Deals Heaven", layout="wide")

# Custom CSS for a stylish dark theme
st.markdown(
    """
    <style>
    body {
        background-color: #121212; /* Dark background */
        color: #ffffff; /* White text */
        font-family: "Roboto", sans-serif;
    }
    .stButton > button {
        background-color: #FF1493 !important; /* Vibrant pink button */
        color: white !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        font-weight: bold;
        font-size: 14px;
        transition: transform 0.2s ease;
        border: 2px solid #ff69b4 !important; /* Pink border for hover effect */
    }
    .stButton > button:hover {
        transform: scale(1.05);
        background-color: #ff69b4 !important; /* Brighter pink on hover */
    }
    .stSidebar {
        background-color: #282c34; /* Dark grey for sidebar */
        color: #ffffff;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #ff69b4; /* Pink headers */
    }
    .deal-card {
        border: 1px solid #444; 
        border-radius: 10px; 
        padding: 15px; 
        margin-bottom: 20px; 
        background: linear-gradient(145deg, #1e1e1e, #2a2a2a); /* Gradient black */
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.8);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        text-align: center;
    }
    .deal-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(255, 105, 180, 0.8); /* Pink shadow on hover */
    }
    .deal-card img {
        width: 100%; 
        height: auto; 
        border-radius: 5px;
    }
    .deal-card h4 {
        font-size: 16px;
        font-weight: bold;
        margin: 10px 0;
        color: #ff69b4; /* Pink title */
    }
    .deal-card p {
        font-size: 14px;
        color: #b0c4de; /* Light blue for details */
        margin: 5px 0;
    }
    .deal-card a {
        display: inline-block;
        margin-top: 10px;
        padding: 8px 15px;
        color: white;
        background-color: #8a2be2; /* Violet blue */
        border-radius: 5px;
        text-decoration: none;
        font-weight: bold;
        border: 2px solid #ba55d3; /* Light violet border */
    }
    .deal-card a:hover {
        background-color: #ba55d3; /* Lighter violet on hover */
    }
    .deal-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        gap: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# App title
st.title("🌌 Deals Heaven Scraper")

# Store and category dropdowns in columns
col1, col2 = st.columns(2)

with col1:
    stores = ["Flipkart", "Amazon", "Paytm", "Foodpanda", "Freecharge", "Paytmmall"]
    store_name = st.selectbox("Choose a Store", stores)

with col2:
    categories = [
        "All Categories",
        "Beauty And Personal Care",
        "Clothing Fashion & Apparels",
        "Electronics",
        "Grocery",
        "Mobiles & Mobile Accessories",
        "Recharge",
        "Travel Bus & Flight"
    ]
    category_name = st.selectbox("Choose a Category", categories)

# Sidebar for page range input
st.sidebar.header("🔢 Page Range")
start_page = st.sidebar.text_input("Start Page", "1")
end_page = st.sidebar.text_input("End Page", "1")

# File to store scraped data
csv_filename = "product_deals.csv"

try:
    start = int(start_page)
    end = int(end_page)

    if start <= 0 or end <= 0:
        st.error("Page numbers must be greater than zero.")
    elif start > end:
        st.error("Starting page must be less than or equal to ending page.")
    elif end > 1703:
        st.error("The DealsHeaven Website has only 1703 Pages!")
    else:
        with st.spinner("Fetching data, please wait..."):
            scrape_deals(store_name, category_name, start, end, csv_filename)
            time.sleep(2)

        st.success("✅ Data scraping and saving completed.")

        if os.path.exists(csv_filename):
            data = get_deals(csv_filename)
            st.write("## Scraped Deals")

            # Display products in a flexible grid
            st.markdown('<div class="deal-container">', unsafe_allow_html=True)
            for _, row in data.iterrows():
                st.markdown(
                    f"""
                    <div class="deal-card">
                        <img src="{row['Image']}" alt="Product Image">
                        <h4>{row['Title']}</h4>
                        <p><strong>Price:</strong> {row['Price']}</p>
                        <p><strong>Special Price:</strong> {row['Special Price']}</p>
                        <p><strong>Discount:</strong> {row['Discount']}</p>
                        <p><strong>Rating:</strong> {row['Rating']} ⭐</p>
                        <a href="{row['Link']}" target="_blank">View Deal</a>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            st.markdown('</div>', unsafe_allow_html=True)

            # Add download button to the sidebar
            with open(csv_filename, "r", encoding="utf-8") as file:
                st.sidebar.download_button(
                    label="📥 Download CSV",
                    data=file,
                    file_name=csv_filename,
                    mime="text/csv",
                )
        else:
            st.error("No data found. Please try scraping again.")

except ValueError:
    st.error("Please enter valid integers for the starting and ending page.")
