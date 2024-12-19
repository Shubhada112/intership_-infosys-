import streamlit as st
import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
from webdriver_manager.chrome import ChromeDriverManager

# Define a function to map category names to URL-compatible formats
def format_category_url(category):
    special_cases = {
        "Fonts & Typography": "fonts-typography",
        "UI/UX Design": "ui-ux-design",
        "Architecture & Interior Design": "architecture-interior-design",
        "T-Shirt & Merchandise": "t-shirt-merchandise",
        "Flyer & Brochure Design": "flyer-brochure-design",
        "Image Editing & Retouching": "image-editing-retouching",
        "Mentorship & Career Advice": "mentorship-and-career-advice",
        "Music Composition & Production": "music-composition-and-production",
        "Video Production & Editing": "video-production-and-editing",
    }
    return special_cases.get(category, category.lower().replace(' ', '-'))

# Define a function to scrape job data
def scrape_jobs(category):
    # Set up the WebDriver with the correct Service object
    service = Service(ChromeDriverManager().install())  # Initialize Service with the path to the chromedriver
    driver = webdriver.Chrome(service=service)

    try:
        # Open the Behance job listing page for the selected category
        if category == "ALL":
            driver.get("https://www.behance.net/joblist")
        else:
            category_url = format_category_url(category)
            driver.get(f"https://www.behance.net/joblist?category={category_url}")
        time.sleep(2)

        # Find the scrollable container (use 'body' as fallback)
        scrollable_container = driver.find_element(By.TAG_NAME, "body")

        # Initialize the list to store jobs and a set to track already scraped job links
        scraped_jobs = []
        scraped_job_links = set()  # To store unique job links

        # Perform scrolling and scrape jobs
        for _ in range(6):  # Scroll 6 times
            scrollable_container.send_keys(Keys.PAGE_DOWN)
            time.sleep(1.5)  # Adjust delay to ensure content loads

            # Wait for job cards to load dynamically
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "JobCard-jobCard-mzZ"))
            )

            # Extract job cards
            job_cards = driver.find_elements(By.CLASS_NAME, 'JobCard-jobCard-mzZ')
            for job in job_cards:
                try:
                    job_link = job.find_element(By.CLASS_NAME, 'JobCard-jobCardLink-Ywm').get_attribute("href")
                    
                    # Skip job if it's already been scraped
                    if job_link in scraped_job_links:
                        continue

                    # Add the job link to the set to avoid duplicates
                    scraped_job_links.add(job_link)

                    # Extract job details
                    title = job.find_element(By.CLASS_NAME, 'JobCard-jobTitle-LS4').text
                    company = job.find_element(By.CLASS_NAME, 'JobCard-company-GQS').text
                    location = job.find_element(By.CLASS_NAME, 'JobCard-jobLocation-sjd').text
                    description = job.find_element(By.CLASS_NAME, 'JobCard-jobDescription-SYp').text

                    # Extract logo if available
                    try:
                        logo = job.find_element(By.CLASS_NAME, 'AvatarImage-avatarImage-PUL').get_attribute("src")
                    except:
                        logo = None

                    # Append the job to the list
                    scraped_jobs.append({
                        "title": title,
                        "company": company,
                        "location": location,
                        "description": description,
                        "logo": logo,
                        "link": job_link,
                    })
                except Exception as e:
                    print("Error extracting job details:", e)

        return scraped_jobs

    finally:
        driver.quit()

# Streamlit Frontend
st.title("🏢 Behance Job Scraper 🏢")

# Input/select box for job categories
job_categories = [
    "Select job ",
    "Logo Design",
    "Stationery Design",
    "Fonts & Typography",
    "Branding Services",
    "Book Design",
    "Packaging Design",
    "Album Cover Design",
    "Signage Design",
    "Invitation Design",
    "T-Shirt & Merchandise",
    "Flyer & Brochure Design",
    "Poster Design",
    "Identity Design",
    "Website Design",
    "App Design",
    "UI/UX Design",
    "Landing Page Design",
    "Icon Design",
    "Illustrations",
    "Portraits",
    "Comics & Character Design",
    "Fashion Design",
    "Pattern Design",
    "Storyboards",
    "Tattoo Design",
    "NFT Art",
    "3D Illustration",
    "Children's Illustration",
    "Social Media Design",
    "Presentation Design",
    "Infographic Design",
    "Resume Design",
    "Copywriting",
    "Product Photography",
    "Landscape Photography",
    "Image Editing & Retouching",
    "Portrait Photography",
    "Architecture & Interior Design",
    "Landscape Design",
    "Industrial Design",
    "Graphics for Streamers",
    "Game Design",
    "Creative Tool Coaching",
    "Mentorship & Career Advice",
    "Modeling Projects",
    "Architecture Renderings",
    "Music Composition & Production",
    "Sound Design",
    "Animated Gifs",
    "Logo Animation",
    "Motion Graphics",
    "Video Production & Editing",
    "Explainer Videos",
    "Short Video Ads",
]

selected_category = st.selectbox("Select a Job Category", job_categories)

# Run button
if st.button("Submit"):
    with st.spinner("Scraping jobs, please wait..."):
        if selected_category:
            jobs = scrape_jobs(selected_category)
            st.session_state["jobs"] = jobs
            st.success(f"Data for category '{selected_category}' scraped successfully.")
        else:
            st.warning("Please select a job category.")

# CSS styling for dark background and enhanced UI
st.markdown(
    """
    <style>
    /* Base styles */
    body {
        background-color: #2E2E2E;
        color: #0ff;
        font-family: 'Arial', sans-serif;
        margin: 0;
        padding: 0;
    }

    .stApp {
        max-width: 100%;
        width: 100%;
        margin: 0;
        padding: 20px;
    }

    /* Title styles */
    .title {
        text-align: center;
        color: #00aaff;
    }

    /* Selectbox styles */
    .selectbox {
        background-color: #444;
        color: #0ff;
        border: 1px solid #555;
        border-radius: 5px;
    }

    /* Button styles */
    .button {
        background-color: #00ffff;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        padding: 10px 20px;
        border: none;
    }

    .button:hover {
        background-color: #007acc;
    }

    /* Card styles */
    .card {
        background-color: #444;
        border: 1px solid #555;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }

    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
    }

    .job-title {
        font-size: 18px;
        font-weight: bold;
        color: #00aaff;
        margin-bottom: 10px;
    }

    .job-company, .job-location {
        font-size: 14px;
        color: #ccc;
        margin: 5px 0;
    }

    .job-description {
        font-size: 14px;
        color: #bbb;
        margin: 10px 0;
    }

    .apply-button {
        background-color: #00e5ff;
        color: #fff;
        padding: 10px 15px;
        text-align: center;
        border: 2px solid #00aaff;
        border-radius: 5px;
        text-decoration: none;
        font-size: 14px;
    }

    .apply-button:hover {
        background-color: #007acc;
        color: black;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# Show Jobs button
if st.button("Show scrap Jobs"):
    jobs = st.session_state.get("jobs", [])
    if jobs:
        # Split jobs into rows of 3
        rows = [jobs[i:i+3] for i in range(0, len(jobs), 3)]
        
        for row in rows:
            cols = st.columns(3)  # Create 3 columns for each row
            for col, job in zip(cols, row):
                with col:
                    st.markdown(f"<div class='card'>", unsafe_allow_html=True)
                    if job["logo"]:
                        st.image(job["logo"], width=50)
                    st.markdown(f"<div class='job-title'>{job['title']}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='job-company'>{job['company']}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='job-location'>{job['location']}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='job-description'>{job['description']}</div>", unsafe_allow_html=True)
                    if job['link']:
                        st.markdown(f"<a href='{job['link']}' class='apply-button' target='_blank'>Apply Now</a>", unsafe_allow_html=True)
                    st.markdown(f"</div>", unsafe_allow_html=True)
    else:
        st.warning("No jobs available to display.")


#to run --> streamlit run app.py
