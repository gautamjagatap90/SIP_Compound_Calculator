import streamlit as st
import pandas as pd
# import matplotlib.pyplot as plt
from datetime import datetime
import time
# import seaborn as sns

def load_data():
    try:
        return pd.read_excel("crawler_config.xlsx")
    except FileNotFoundError:
        return pd.DataFrame()

def crawl_data():
    # Dummy code to simulate a crawling process
    for i in range(5):
        # Simulating some delay
        time.sleep(1)
    return "Crawl completed successfully! Please go to Output section to Analyse Data "



def Analytics_KPI_top_display():
    # Define enhanced CSS for the KPI boxes with center alignment
    css = """
    <style>
        .kpi_box1 {
            border: 2px solid #1E90FF; /* Light Blue border */
            background-color: #ADD8E6; /* Light Blue background */
            padding: 10px; /* Space inside the box */
            border-radius: 5px; /* Rounded corners */
            margin: 10px 0px; /* Space outside the box */
            text-align: center; /* Center align text */
        }
        .kpi_box2 {
            border: 2px solid #4682B4; /* Steel Blue border */
            background-color: #87CEEB; /* Sky Blue background */
            padding: 10px; /* Space inside the box */
            border-radius: 5px; /* Rounded corners */
            margin: 10px 0px; /* Space outside the box */
            text-align: center; /* Center align text */
        }
        .kpi_box3 {
            border: 2px solid #0000CD; /* Medium Blue border */
            background-color: #1E90FF; /* Dodger Blue background */
            padding: 10px; /* Space inside the box */
            border-radius: 5px; /* Rounded corners */
            margin: 10px 0px; /* Space outside the box */
            text-align: center; /* Center align text */
        }
        .kpi_header {
            color: white; /* White color for the header text */
            font-size: 20px; /* Size of the header text */
            font-weight: bold; /* Make header text bold */
        }
        .kpi_value {
            color: white; /* White color for the value text */
            font-size: 24px; /* Size of the value text */
        }
    </style>
    """


    # Create columns for each KPI
    total1, total2, total3 = st.columns(3)

    with total1:
        st.markdown(css, unsafe_allow_html=True)
        st.markdown(f"<div class='kpi_box1'><span class='kpi_header'>Websites Crawled</span><br><span class='kpi_value'>100+</span></div>", unsafe_allow_html=True)

    with total2:
        st.markdown(css, unsafe_allow_html=True)
        st.markdown(f"<div class='kpi_box2'><span class='kpi_header'>Records Extracted</span><br><span class='kpi_value'>30,000+</span></div>", unsafe_allow_html=True)

    with total3:
        st.markdown(css, unsafe_allow_html=True)
        st.markdown(f"<div class='kpi_box3'><span class='kpi_header'>Expert Members</span><br><span class='kpi_value'>4+</span></div>", unsafe_allow_html=True)




def main_ui():

    now = datetime.now() 
    st.title("Web Crawling Pro Configuration")

    Analytics_KPI_top_display()

    st.header("##")

    st.write("Please fill in the details below to configure the web crawler. Fields marked with a * are required.")

    df = load_data()

    with st.form(key='crawler_form'):
        with st.expander("Website Access Configuration",expanded=True):
            url = st.text_input("Website URL *", 'https://aeda.de/allergologen-suche/?location=Berlin,%20Germany&radius=700',
                                help="Enter the full URL of the website you want to crawl. This should include 'http://' or 'https://'. Example: https://www.example.com")
            cookies_xpath = st.text_input("Cookies Acknowledgment XPath", '/html/body/div[4]/div[2]/div[2]/div[1]/a[1]',
                                          help="Provide the XPath to the cookie acceptance button. This allows the crawler to interact with the website after accepting cookies. Example: /html/body/div[4]/div[2]/div/button")
            website_description = st.text_input("Website Description", 'This website is a directory of allergologists in Germany.', help="Enter a brief description of the website you are crawling with filter description.")

            col1, col2 = st.columns(2)
            with col1:
                User_name = st.text_input("User Name *", 'admin', help="Enter the User Name")
            with col2:
                date_added = st.text_input("Run Date", value=now.strftime("%Y-%m-%d %H:%M:%S"), disabled=True)

            # PLZ XPath and Lookup Type
        with st.expander("Location Search Configuration",expanded=False):
            plz_xpath = st.text_input("ZIP or City Search Box XPath", '',
                                        help="Enter the XPath for the input field where ZIP or city information needs to be entered. This is required if your crawling involves searching through different regions or ZIP codes.")
            lookup_type = st.selectbox("Lookup Type", ["City Lookup", "ZIP Lookup", "None"], index=2,
                                        help="Choose how the search should be performed: 'City Lookup' for city-based searches, 'ZIP Lookup' for ZIP code searches, or 'None' if the search doesn't require city or ZIP inputs.")

        # Page Navigation
        with st.expander("Page Navigation Configuration and Ranges",expanded=False):
            page_url = st.text_input("Page URL Pattern", '',
                                        help="Specify the patterned URL for pages to crawl, especially if the URL changes with each page. Use placeholders for dynamic parts, e.g., https://www.example.com/page={page}")
            start_page = st.number_input("Start Page", min_value=1, format="%d", value=1,
                                            help="Enter the starting page number from which the crawler should begin. For instance, if pagination starts from page 1, enter 1.")
            end_page = st.number_input("End Page", min_value=1, format="%d", value=1,
                                        help="Enter the last page number that the crawler should process. Ensure that this number does not exceed the total number of available pages.")

        # Physician Extraction Ranges
        with st.expander("Physician Level Data Extraction Ranges",expanded=False):
            phys_xpath = st.text_input("Physician XPath", '/html/body/div[3]/div[1]/div/div/div/div[1]/div[2]/div/div/div/div/div/div[{phyloop}]/div/div/h3',
                                        help="Enter the XPath that leads to the physician's name on the webpage. This should be precise to ensure accurate data extraction.")
            start_range = st.number_input("Start Range for Physician Extraction", min_value=0, format="%d", value=1,
                                            help="Set the starting index for physician data extraction on each page. Typically, this starts from 1 or the first relevant data point on the page.")
            end_range = st.number_input("End Range for Physician Extraction", min_value=0, format="%d", value=20,
                                        help="Set the ending index for physician data extraction on each page. This should not exceed the total number of entries per page.")

        # Other XPath configurations
        with st.expander("Additional Physician level XPath Configuration",expanded=False):
            inst_xpath = st.text_input("Institution XPath", '',
                                        help="Provide the XPath for extracting the institution name associated with each physician, if applicable.")
            addr_xpath = st.text_input("Address Content XPath", '/html/body/div[3]/div[1]/div/div/div/div[1]/div[2]/div/div/div/div/div/div[{phyloop}]/div/div/p[2]',
                                        help="Provide the XPath for extracting the address information of each listed physician or institution.")


        # Submit button for the form
        submitted = st.form_submit_button("Submit Configuration")
        if submitted:
            new_data = {
                'User_name': User_name,
                'date_added': date_added,
                'url': url,
                'website_description': website_description,
                'cookies_xpath': cookies_xpath,
                'plz_xpath': plz_xpath,
                'lookup_type': lookup_type,
                'start_page': start_page,
                'end_page': end_page,
                'page_url': page_url,
                'start_range': start_range,
                'end_range': end_range,
                'phys_xpath': phys_xpath,
                'inst_xpath': inst_xpath,
                'addr_xpath': addr_xpath
            }
            # Append new data to the DataFrame
            new_df = pd.DataFrame([new_data])
            df = pd.concat([df, new_df], ignore_index=True)
            try:
                df.to_excel("crawler_config.xlsx", index=False)
                st.session_state['df'] = df  # Update session state
                st.success("Configuration saved and appended successfully!")
            except Exception as e:
                st.error("Failed to save configuration: {}".format(e))

    # Displaying the DataFrame in an expander
    if 'df' in st.session_state:
        df = st.session_state['df']
        with st.expander("Re-View Configuration Records",expanded=True):
            shwdata = st.multiselect('Filter:', df.columns, default=df.columns.tolist())
            st.dataframe(df[shwdata], use_container_width=True)

    if st.button("Start Crawl"):
        with st.spinner("Crawling in progress..."):
            result = crawl_data()
            st.success(result)
            
if __name__ == "__main__":
    main_ui()
