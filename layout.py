import streamlit as st

# Function to set up the initial page configuration
def set_layout():
    """Set the initial configuration of the Streamlit page including title, layout, and icon."""
    st.set_page_config(
        page_title="WebcrawlerPro Dashboard",
        page_icon="🌐",
        layout="wide",
        initial_sidebar_state="expanded"
    )

# Function to apply custom CSS to enhance the appearance of the Streamlit app
def apply_custom_css():
    """Apply custom CSS to modify the Streamlit default styles."""
    background_image_url = 'url("C:/Users/u46859/Pictures/Screenshots/IQVIA_SLIDE.jpg")'  # Replace with your image path or URL
    custom_css = f"""
    <style>
        /* Full screen background */
        body {{
            background-image: {background_image_url};
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        
        /* Full height for the root container */
        #root {{
            display: flex;
            flex-direction: column;
            height: 100vh;
        }}

        /* Style adjustments for footer */
        footer {{
            margin-top: auto;
            background-color: rgba(255, 255, 255, 0.8);  /* Light background for footer for readability */
            text-align: center;
            border-top: 1px solid #ccc;
        }}

        /* Custom styles for buttons and text input */
        .stButton>button {{
            border-radius: 20px;
            background-color: rgba(255, 255, 255, 0.8);  /* Light background for button for readability */
        }}
        .stTextInput>div>div>input {{
            border-radius: 10px;
            background-color: rgba(255, 255, 255, 0.8);  /* Light background for input for readability */
        }}

        /* Hide the header for a cleaner look */
        /*header {{visibility: hidden;}}*/

        /* Ensure text is visible on the potentially busy background */
        .reportview-container .markdown-text-container, .reportview-container .streamlit-expanderHeader {{
            color: #000; /* Dark text for contrast */
        }}
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

# header {visibility: hidden;}
# Function to create a header in the main area of the Streamlit app
def create_header(title):
    """Create a header for the Streamlit page."""
    st.markdown(f"# {title}")

# Function to create a footer that appears at the bottom of the Streamlit app
def create_footer():
    st.markdown(""" """)
    """Create a footer for the Streamlit page."""
    st.markdown("""
        <footer>
            <p>Powering data extraction by Navigating the web for healthcare insights | IQVIA’s EUHUB webcrawling experts © 2024</p>
        </footer>
    """, unsafe_allow_html=True)

# Function to add a sidebar with various interactive elements
def setup_sidebar():
    """Setup sidebar with different input options and a button."""
    st.sidebar.title("Settings Panel")
    url = st.sidebar.text_input('Enter the URL to crawl', 'http://example.com',key='url1')
    depth = st.sidebar.number_input('Set the depth of crawling', min_value=1, max_value=10, value=1)
    if st.sidebar.button('Start Crawling',key='crawl0'):
        st.sidebar.write('Crawling initiated...')

# Function to create responsive columns based on the screen size
def responsive_columns(n_columns: int):
    """Create responsive columns based on the window width."""
    if st.session_state.window_width > 1400:
        return st.columns(n_columns)
    else:
        return [st] * n_columns  # Use the main container as a single column on smaller screens


def hide_streamlit_interface():
    hide_st_style = """
    <style>
    /*header {visibility: hidden;}*/
    footer {visibility: hidden;}
    </style>
    """
    st.markdown(hide_st_style, unsafe_allow_html=True)