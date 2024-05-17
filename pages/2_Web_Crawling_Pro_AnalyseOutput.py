import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.graph_objects as go
import json
import plotly.express as px

# Load required datasets
def load_data():
    data = pd.read_excel('dependencies/output.xlsx')
    lat_long_data = pd.read_excel('dependencies/LAT_LONG_GERMANY_PLZs.xlsx')
    population_data = pd.read_excel('dependencies/germany_population.xlsx')
    germany_states = gpd.read_file('dependencies/Germany Shape File/DEU_adm1.shp')
    return data, lat_long_data, population_data, germany_states

# Merge datasets for geospatial analysis
def prepare_data(data, lat_long_data, population_data, germany_states):
    data['PLZ'] = data['PLZ'].astype(str)
    lat_long_data['Postal Code'] = lat_long_data['Postal Code'].astype(str)
    merged_data = pd.merge(data, lat_long_data[['Postal Code', 'lat', 'long']], left_on='PLZ', right_on='Postal Code', how='left')
    germany_states = germany_states.merge(population_data, left_on='NAME_1', right_on='State Name')
    
    # Create hover text by concatenating 'vorname_list' and 'nachname_list'
    merged_data['hover_text'] = merged_data['vorname_list'] + ' ' + merged_data['nachname_list']
    
    return merged_data, germany_states

# Creating the geospatial plot
def create_fig(merged_data, germany_states):
    fig = go.Figure()

    # State/Region Coloring - Choroplethmapbox for state boundaries
    fig.add_trace(go.Choroplethmapbox(
        geojson=germany_states.geometry.__geo_interface__,
        locations=germany_states.index,
        z=germany_states['Population'],
        text=germany_states['State Name'],
        colorscale="blues",
        marker_opacity=0.5,
        marker_line_width=2,
        marker_line_color='gray'
    ))

    # PHY Positions - A Segment
    fig.add_trace(go.Scattermapbox(
        lat=merged_data[merged_data['Phy Number']>=5]['lat'],
        lon=merged_data[merged_data['Phy Number']>=5]['long'],
        mode='markers',
        marker=go.scattermapbox.Marker(size=8, color='orange', opacity=1),
        text=merged_data[merged_data['Phy Number']>=5]['hover_text'],
        hoverinfo='text'
    ))

    # PHY Positions - B segment
    fig.add_trace(go.Scattermapbox(
        lat=merged_data[merged_data['Phy Number']<5]['lat'],
        lon=merged_data[merged_data['Phy Number']<5]['long'],
        mode='markers',
        marker=go.scattermapbox.Marker(size=8, color='Brown', opacity=1),
        text=merged_data[merged_data['Phy Number']<5]['hover_text'],
        hoverinfo='text'
    ))

    # National Boundary
    germany_national = gpd.read_file('dependencies/Germany Shape File/DEU_adm0.shp')
    geojson_national = json.loads(germany_national.to_json())
    coords = geojson_national['features'][0]['geometry']['coordinates']
    lon, lat = [], []
    for part in coords:
        if isinstance(part[0][0], list):
            for segment in part:
                lon += [p[0] for p in segment] + [None]
                lat += [p[1] for p in segment] + [None]
        else:
            lon += [p[0] for p in part] + [None]
            lat += [p[1] for p in part] + [None]

    national_border = go.Scattermapbox(
        lon=lon,
        lat=lat,
        mode='lines',
        line=go.scattermapbox.Line(color='black', width=1),
        hoverinfo='none'
    )
    fig.add_trace(national_border)

    # Map Setting
    fig.update_layout(
        mapbox_style="open-street-map",
        mapbox_zoom=5,
        mapbox_center={"lat": 51.1657, "lon": 10.4515},
        title_text="Germany Map: States with National Border, Major Cities, and Physician Locations",
        margin={"r":0, "t":50, "l":0, "b":0},
        height=600  # Set the height to 800 pixels
    )

    map_html = fig.to_html(full_html=False)
    
    return fig, map_html


def plot_missing_data(data):
    # Calculate the number of missing values in each column
    missing_values = data.isnull().sum().reset_index()
    missing_values.columns = ['column', 'missing_count']

    # Create an interactive bar plot with Plotly Express
    fig = px.bar(missing_values, x='missing_count', y='column', orientation='h',
                 title="Number of Missing Values Per Column",
                 labels={'column': 'Columns', 'missing_count': 'Number of Missing Values'},
                 color='missing_count',
                 color_continuous_scale='Viridis',
                 text='missing_count')  # Show missing count as text

    # Adjust the layout to ensure the text fits and is visible
    fig.update_traces(texttemplate='%{text}', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    fig.update_layout(xaxis_title="Number of Missing Values",
                      yaxis_title="Columns")

    # Display the plot in the Streamlit app
    st.plotly_chart(fig, use_container_width=True)


import streamlit as st

def Analytics_KPI_top_display(data, plz_column, PLZ_Searched):
    # Dynamic calculations from your data
    PLZ_Searched_count = len(data[PLZ_Searched].unique())
    Unique_PLZs_count = len(data[plz_column].unique())
    records_extracted_count = len(data)
    unique_records_count = data.drop_duplicates().shape[0]
    
    # Define enhanced CSS for the KPI boxes with center alignment
    css = """
    <style>
        .kpi_box {
            border: 2px solid #1E90FF; /* Blue border */
            background-color: #ADD8E6; /* Light Blue background */
            padding: 10px; /* Space inside the box */
            border-radius: 5px; /* Rounded corners */
            margin: 10px; /* Space outside the box */
            text-align: center; /* Center align text */
            color: white; /* White color for the text */
            font-size: 20px; /* Size of the text */
            font-weight: bold; /* Make text bold */
        }
    </style>
    """

    # Create columns for each KPI
    total1, total2, total3, total4 = st.columns(4)

    with total1:
        st.markdown(css, unsafe_allow_html=True)
        st.markdown(f"<div class='kpi_box'>Total Records<br>{records_extracted_count}</div>", unsafe_allow_html=True)

    with total2:
        st.markdown(css, unsafe_allow_html=True)
        st.markdown(f"<div class='kpi_box'>Unique Records<br>{unique_records_count}</div>", unsafe_allow_html=True)

    with total3:
        st.markdown(css, unsafe_allow_html=True)
        st.markdown(f"<div class='kpi_box'>Total PLZ Searched<br>{PLZ_Searched_count}</div>", unsafe_allow_html=True)

    with total4:
        st.markdown(css, unsafe_allow_html=True)
        st.markdown(f"<div class='kpi_box'>Unique PLZs in Search Radius<br>{Unique_PLZs_count}</div>", unsafe_allow_html=True)


# Streamlit app

def app():
    st.title("Webcrawler Output Diagnostics and Geospatial Analysis")

    


    # File uploader allows user to upload their own Excel file
    uploaded_file = st.sidebar.file_uploader("Upload your data file (.xlsx)", type="xlsx")
    if uploaded_file:
        data = pd.read_excel(uploaded_file)
    else:
        st.header("##")
        with st.spinner("Loading Sample data..."):
            data, lat_long_data, population_data, germany_states = load_data()

    st.sidebar.title("Configuration")
    if 'data' in locals():  # Check if data is loaded
        # Dropdown menu to select PLZ column for Geo mapping on the sidebar
        plz_column = st.sidebar.selectbox(
            "Select PLZ/ Zip Code Column for Geo mapping:",
            data.columns.tolist(),
            index=data.columns.tolist().index("PLZ") if "PLZ" in data.columns else 0
        )
        PLZ_Searched = st.sidebar.selectbox(
            "Select Serached PLZ/ Zip Code for corresponding entry:",
            data.columns.tolist(),
            index=data.columns.tolist().index("PLZ_Serached") if "PLZ_Serached" in data.columns else 0
        )

        # Submit button on the sidebar
        Analytics_KPI_top_display(data, plz_column=plz_column, PLZ_Searched=PLZ_Searched)
        
        with st.expander("Web Crawler Output Diagnostics:", expanded=False):
            plot_missing_data(data)

        with st.spinner("Generating Geospatial Map..."):
            with st.expander("Geographical Distribution Map:", expanded=False):
                merged_data, germany_states = prepare_data(data, lat_long_data, population_data, germany_states)
                fig, map_html = create_fig(merged_data, germany_states)
                st.plotly_chart(fig, use_container_width=True)

                st.download_button(
                    label="Download Map (HTML)",
                    data=map_html,
                    file_name="geospatial_map.html",
                    mime="text/html",
                    help="Click here to download the geospatial map as an HTML file"
                )

        # Data table and download button
        with st.expander("Data Table"):
            st.dataframe(data)  # Display the data table
            csv = data.to_csv(index=False).encode('utf-8')
            st.download_button(
                "Download Data",
                data=csv,
                file_name="Crawled_Data.csv",
                mime="text/csv",
                help='Click here to download the data as a CSV file'
            )


    # st.title("Streamlit Tabs Example")

    # # Create tabs
    # tabs = ["Tab 1", "Tab 2"]
    # selected_tab = st.tabs(tabs)

    # # Display content based on selected tab
    # if selected_tab == "Tab 1":
    #     st.write("Content of Tab 1")
    # elif selected_tab == "Tab 2":
    #     st.write("Content of Tab 2")


if __name__ == "__main__":
    app()
