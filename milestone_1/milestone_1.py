#Aim--> - scrap the data with the help of beautifulsoup and save in CSV file 
#       - make a forntend with help of stremlit (feature - appliction , page )

#Import the Required Libraries-

import pandas as pd
#pandas (as pd):managing tabular data 

import requests
#requests: make HTTP requests to get the website’s HTML.

from bs4 import BeautifulSoup
#BeautifulSoup (from bs4): To parse and navigate the HTML content.

import streamlit as st
#streamlit (as st):displaying the output in a Streamlit app (forntend)

st.set_page_config(page_title="Deal Hunter - DealsHeaven", page_icon="🛒", layout="wide")
#its show App Header and Introduction content

#-----------------------------------------------------------------------------------------------------

# Frontend Custom CSS for styling the page
st.markdown("""
    <style>
    body {
        background-color: #f0f4f8;
        font-family: 'Helvetica', sans-serif;
    }
    .stButton button {
        background-color: #ff5733;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 12px;
        border: none;
    }
    .stButton button:hover {
        background-color: #c0392b;
    }
    .stSelectbox select {
        background-color: #ffffff;
        border: 2px solid #007BFF;
        border-radius: 5px;
        padding: 10px;
    }
    .deal-title {
        color: #2e4053;
        font-size: 18px;
        font-weight: bold;
    }
    .deal-price {
        color: #27ae60;
        font-size: 16px;
        font-weight: bold;
    }
    .deal-special-price {
        color: #e74c3c;
        font-size: 16px;
        font-weight: bold;
    }
    .stExpanderHeader {
        background-color: #2980b9;
        color: white;
        font-size: 18px;
        font-weight: bold;
    }
    .stExpanderContent {
        background-color: #ecf0f1;
    }
    footer {
        text-align: center;
        font-size: 14px;
        color: #7f8c8d;
    }
    </style>
""", unsafe_allow_html=True)
#css
#------------------------------------------------------------------------------------------------
#Frontend code

st.title("DEAL - HUNTER ")
#titile  

st.markdown("<h3>Way to Grap offers 😃, Just by one Click 🤳!</h3>", unsafe_allow_html=True)
#caption 

st.write("Use the tool to find the best deals from top stores! Select your preferred store and page range to explore the latest discounts.")
#sub caption 

# application selection (ex - amazon , flikart etc)
store_name = st.selectbox(
    "Select a Store",
    options=[
        "Select Application","Amazon", "Airasia", "Aircel", "AmericanSwan", "askmebazar", "Abhibus", "AkbarTravels", "abof", "Airtel",
        "Babyoye", "Bigrock", "Burgerking", "Bigbasket", "bookmyshow", "Bluehost", "cromaretail", "Cleartrip",
        "crownit", "Cinepolis Cinema", "Clovia", "Dominos", "Ebay", "Edukart", "Expedia", "EaseMyTrip", "Flipkart",
        "Firstcry", "Fasttrack", "FashionAndYou", "Fabfurnish", "Fabindia", "Fashionara", "fernsnpetals", "Foodpanda",
        "Freecharge", "Freecultr", "Fasoos", "FitnLook", "Goibibo", "Groupon India", "Grofers", "Greendust", "GoAir",
        "Helpchat", "HomeShop18", "HealthKart", "Hostgator", "Indiatimes", "Infibeam", "ixigo", "IndiGo", "Jabong",
        "Jugnoo", "JustRechargeIt", "Koovs", "KFC", "LensKart", "LittleApp", "MakeMyTrip", "McDonalds", "Mobikwik",
        "Musafir", "Myntra", "Nearbuy", "Netmeds", "NautiNati", "Nykaa", "Others", "Oyorooms", "Ola", "Paytm",
        "PayUMoney", "Pepperfry", "Printvenue", "PayZapp", "Pizzahut", "Photuprint", "pharmeasy", "Redbus", "Rediff",
        "Rewardme", "Reliance Big TV", "Reliance trends", "Snapdeal", "ShopClues", "ShoppersStop", "Sweetsinbox",
        "Styletag", "ShopCJ", "Taxi for Sure", "Travelguru", "Trendin", "ticketnew", "TataCLiQ", "Tata Sky",
        "thyrocare", "udio", "UseMyVoucher", "Uber", "voonik", "Vistaprint", "VLCC", "VideoconD2H", "Vodafone",
        "Woo Hoo", "Woodland", "Yatra", "Yepme", "Zivame", "Zovi", "Zomato", "zoomin", "Zotezo"
    ],
    index=0
)

# page start - end selection
start_page = st.number_input("Enter Start Page", min_value=1, step=1, format="%d", help="Enter the first page number to scrape.")
end_page = st.number_input("Enter End Page", min_value=1, step=1, format="%d", help="Enter the last page number to scrape.")

# Button to accpect the info given by the user ---> Fetch Deals 
if st.button("Fetch Deals", use_container_width=True):
    if end_page < start_page:
        st.error("End Page should be greater than or equal to Start Page.")
    else:
        all_deals = []

        # Loop through the selected page range
        for page in range(start_page, end_page + 1):
            url = f"https://dealsheaven.in/store/{store_name.lower()}?page={page}"
            response = requests.get(url)

            # Check if the page is accessible
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                # Find deal cards
                deal_cards = soup.find_all('div', class_='deatls-inner')

                for deal_card in deal_cards:
                    title = deal_card.find('h3').text.strip() if deal_card.find('h3') else "No title"
                    price = deal_card.find('p', class_='price').text.strip() if deal_card.find('p', class_='price') else "No price"
                    special_price = deal_card.find('p', class_='spacail-price').text.strip() if deal_card.find('p', class_='spacail-price') else "No special price"

                    all_deals.append({
                        "Title": title,
                        "Original Price": price,
                        "Special Price": special_price
                    })
            else:
                st.warning(f"Page {page} could not be accessed. Status code: {response.status_code}")

        # Display the deals in an interactive and visually attractive way
        if all_deals:
            st.write(f"**Displaying deals for {store_name} from page {start_page} to {end_page}:**")
            for deal in all_deals:
                with st.expander(deal['Title'], expanded=False):
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.markdown(f"<div class='deal-title'>{deal['Title']}</div>", unsafe_allow_html=True)
                        st.markdown(f"<div class='deal-price'>Original Price: {deal['Original Price']}</div>", unsafe_allow_html=True)
                        st.markdown(f"<div class='deal-special-price'>Special Price: {deal['Special Price']}</div>", unsafe_allow_html=True)
                    with col2:
                        st.markdown(f"[🔗 View Deal]({deal['Title']})", unsafe_allow_html=True)

        else:
            st.write("No deals found for the selected store and page range.")

# Footer with custom design
st.markdown("""
    <footer>
        <p>Created with ❤️ by DealHunter Team | <a href="https://github.com/Shubhada112" target="_blank">GitHub</a></p>
    </footer>
""", unsafe_allow_html=True)


#to run the code use ----streamlit run file_name(milestone_1.py)
# streamlit run app.py
