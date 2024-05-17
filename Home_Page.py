import streamlit as st

st.set_page_config(layout="wide") 

def app():
    st.title('WebCrawlPro Documentation')

    documentation_content = """
    ### **How to Use WebCrawlPro: A Non-Coder's Guide**

    Welcome to WebCrawlPro! This guide will walk you through the process of configuring and using our web crawler to extract data from websites, even if you're not a coder. We'll focus on using XPaths for data extraction, with a note on other possibilities for the future.

    ---

    **1. Recognizing Data Patterns**

    Recognizing data patterns is the first step in extracting the information you need from web pages. Here's how to do it:

    - **Inspect the Web Page**: Right-click on the web page and select "Inspect" (or press `F12`) to open the developer tools. This will show you the HTML structure of the page.

    - **Identify Key Elements**: Look for the elements that contain the data you want to extract. These could be text, images, or other content. Note down the XPaths associated with these elements.

    - **Compare Multiple Pages**: Visit multiple pages with similar content and compare the HTML structure. Look for patterns in how the data is presented and how it changes from page to page.

    ---

    **2. Identifying Physician Patterns**

    Let's walk through an example of how to identify physician patterns:

    **XML Examples for Physician Names**:
    ```
    <!-- XML for Physician Names - XML 1 -->
    /html/body/div[3]/div[1]/div/div/div/div[1]/div[2]/div/div/div/div/div/div[1]/div/div/h3

    <!-- XML for Physician Names - XML 2 -->
    /html/body/div[3]/div[1]/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div/div/h3
    ```

    In these examples, we have two XML paths representing the location of physician names on the webpage. Let's assume the sample names extracted from these XMLs are "Dr. John Doe" and "Dr. Jane Smith".

    - **Identifying Sample Names**: By inspecting the web page, we find that the names "Dr. John Doe" and "Dr. Jane Smith" exist in the provided XMLs.

    - **Creating a Generic XML Path**: We can create a generic XML path with a variable to be changed for looping through physician names. For example:
    ```xml
    <!-- Generic XML Path with Variable -->
    /html/body/div[3]/div[1]/div/div/div/div[1]/div[2]/div/div/div/div/div/div[{phyloop}]/div/div/h3
    ```
    
    - **Automatic Looping and Extraction**: With the generic XML path configured, WebCrawlPro will automatically loop through different physician entries and extract the corresponding names. These names can then be displayed in a datatable format for easy analysis.

    ---

    **3. Understanding and Configuring URLs**

    URLs play a crucial role in navigating through different pages on a website. Here's what you need to know:

    - **Identify URL Patterns**: Notice how the URL changes when you navigate through the website. Look for patterns such as query parameters (`?page=2`) or keywords (`?search=keyword`).

    - **Modify URL Parameters**: If pages are accessed through specific keywords or parameters, identify which part of the URL changes. This will help you configure the crawler to navigate to different pages.

    ---

    **4. Handling Pagination and Variable Paths**

    Many websites use pagination to display content across multiple pages. Here's how to handle it:

    - **Recognize Pagination Patterns**: Identify how the page number is reflected in the URL or page buttons. This could be a simple increment in the URL parameter or a script-based change.

    - **Configure Loop Variables**: Specify the variable position for the page number in the URL. This will allow the crawler to navigate through all pages automatically.

    - **Understand Maximal Paths**: Recognize the deepest level you can go on a website without looping back or reaching a dead end. This will help you navigate efficiently.

    ---

    **Note**: While this guide focuses on using XPaths for data extraction, WebCrawlPro may support other methods such as CSS selectors and HTML tags in the future.

    ---

    **Conclusion**

    With these steps, you can configure WebCrawlPro to extract data from websites without writing any code. Take your time to explore different websites, identify patterns, and configure the crawler accordingly. Happy crawling!

    ---

    """
    
    # Render the markdown content in the app
    st.markdown(documentation_content)

if __name__ == '__main__':
    app()
