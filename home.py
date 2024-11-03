import streamlit as st
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import time

def stream_data():
    for word in TEXT.split(" "):
        yield word + " "
        time.sleep(0.1)

# Set up the Streamlit page configuration and hide menu, footer, header
st.set_page_config(page_icon="💜", page_title="TTIDFL", layout="centered")
st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

# Title of the Streamlit app
st.title("🫰🏻 TTIDFL")

st.sidebar.title("🫰🏻 TTIDFL")
st.sidebar.write("&nbsp;")
st.sidebar.image("https://korean-binge.com/wp-content/uploads/2024/04/2024-lovely-runner-tvn8951564812516606301.jpg")
st.sidebar.write("Made for sunnim 💜")
st.sidebar.write("&nbsp;")
st.sidebar.info("List credits: [kfangurl](https://thefangirlverdict.com/)")

st.write("&nbsp;")
update_button = st.button("🧣 Sunnim, click here to update!", type="primary")
st.write("&nbsp;")

if not update_button:
    with st.container(border=True):
        st.image("https://kenh14cdn.com/2020/4/21/3-1587406977110257273402.jpg")
else:
    # Step 1: Scrape the data from the website
    url = "https://thefangirlverdict.com/index/all-reviews/full-list-of-shows/"
    
    # Send a GET request
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    # Clean up the soup
    for p in soup.find_all("p", style="text-align:justify"):
        p.decompose()

    # Create lists to store the extracted data
    names = []
    urls = []
    grades = []

    # Initialize the progress bar
    progress_bar = st.progress(0)

    # Step 2: Process the data (n_steps items)
    TEXT = "Wait so patiently I won't even know you were waiting..."
    st.write(stream_data)
    with st.container(border=True):
        st.video("https://youtu.be/xUfNIZym6vE?si=V_0o5rigCZzUMfFk")
    st.snow()

    n_steps = 900
    for x in range(n_steps):
        element = soup.select_one(f"#post-7658 > div > p:nth-child({x})")
        if element is None:
            continue

        kdrama = element.findChildren("a", recursive=False)
        grade = element.findChildren("strong", recursive=False)

        if kdrama:
            names.append(kdrama[0].contents[0])
            urls.append(kdrama[0].get("href"))
            grades.append(grade[0].text if grade else "NA")

        # Update the progress bar and status text
        progress_bar.progress((x + 1) / n_steps)

    # Step 3: Create the DataFrame
    st.balloons()
    df = pd.DataFrame({"source": names, "url": urls, "rating": grades})
    
    # Step 4: Data cleaning
    df = df.replace("NA", np.nan)
    df.dropna(inplace=True)
    df["year"] = df.apply(lambda row: re.search(r"\d+", row["url"]).group() if re.search(r"\d+", row["url"]) else None, axis=1)

    # Save the current date as a column
    current_date = datetime.now().strftime("%d %B %Y")
    df["last_update"] = current_date

    # Extract the last update date
    last_update = current_date
    st.write(f"Updated: {last_update}")

    # Drop unnecessary columns
    df = df.drop(columns=["last_update"])

    # Add the clickable hyperlink in 'source' column
    df["source"] = df.apply(lambda row: f'<a href="{row["url"]}" target="_blank">{row["source"]}</a>', axis=1)

    # Relevel the 'rating' column (following your R code logic)
    rating_order = ['A++', 'A+', 'A', 'A-', 'B++', 'B+', 'B', 'B-', 'C++', 'C+', 'C', 'C-', 'D++', 'D+', 'D', 'D-']
    df["rating"] = pd.Categorical(df["rating"], categories=rating_order, ordered=True)

    # Convert 'year' to integer
    df["year"] = pd.to_numeric(df["year"], errors='coerce')  # Safely convert to integer
    df = df.dropna(subset=["year"])  # Drop rows where 'year' couldn't be converted
    df["year"] = df["year"].astype(int)

    # Data processing based on your R-like logic
    df = df.dropna(subset=["rating"])  # Drop rows where 'rating' is NA

    # Drop rows with duplicate 'url'
    df = df.drop_duplicates(subset=['url'])

    # Sort the DataFrame by 'Year' (descending) and 'Rating' (descending)
    df = df.sort_values(by=["year", "rating"], ascending=[False, True])

    # Select relevant columns and rename them
    df = df[["source", "rating", "year"]].rename(columns={"source": "Show", "rating": "Rating", "year": "Year"})

    # Display the DataFrame
    html = df.to_html(escape=False, index=False)
    st.markdown(html, unsafe_allow_html=True)