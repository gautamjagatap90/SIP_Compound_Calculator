import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(layout="wide")
# Function to generate investment data
def generate_investment_data(initial_investment, monthly_investment, return_rate, return_frequency, investment_timing, start_date, num_years, stop_investment_date):
    # Initialize lists to store data
    years = []
    months = []
    opening_balance = []
    monthly_sip = []
    opening_balance_investment = []
    monthly_return = []
    closing_balance = []
    
    # Convert start_date string to datetime object
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    
    # Calculate the number of months to stop investment
    stop_investment_month = (stop_investment_date.year - start_date.year) * 12 + (stop_investment_date.month - start_date.month)
    
    # Generate investment data for each month
    current_date = start_date
    for i in range(num_years * 12):
        # Append year and month
        years.append(current_date.year)
        months.append(current_date.strftime("%B"))
        
        # Calculate opening balance
        if i == 0:
            opening_balance.append(initial_investment)
        else:
            opening_balance.append(closing_balance[-1])
        
        # Calculate monthly SIP
        if investment_timing == 'Start of Month':
            if i < stop_investment_month:
                monthly_sip.append(monthly_investment)
            else:
                monthly_sip.append(0)
        else:  # investment_timing == 'End of Month'
            if i == 0:
                previous_month_closing_balance = initial_investment
            else:
                previous_month_closing_balance = closing_balance[-1]
            if i < stop_investment_month:
                monthly_sip.append(previous_month_closing_balance + monthly_investment)
            else:
                monthly_sip.append(0)
        
        # Calculate opening balance for investment
        if i == 0:
            opening_balance_investment.append(initial_investment + monthly_sip[-1])
        else:
            opening_balance_investment.append(closing_balance[-1] + monthly_sip[-1])
        
        # Calculate monthly return
        if return_frequency == 'Monthly':
            monthly_return.append(int(opening_balance_investment[-1] * (return_rate / 100) / 1))
        else:
            monthly_return.append(int(opening_balance_investment[-1] * ((1 + return_rate / 100) ** (1/12) - 1)))

        # Calculate closing balance
        closing_balance.append(opening_balance_investment[-1] + monthly_return[-1])
        
        # Move to next month
        current_date += timedelta(days=30)
    
    # Create DataFrame
    df = pd.DataFrame({
        'Year': years,
        'Month': months,
        'Starting Balance (Rs)': opening_balance,
        'Monthly Investment (Rs)': monthly_sip,
        'Opening Balance for Investment (Rs)': opening_balance_investment,
        'Monthly Return (Rs)': monthly_return,
        'Closing Balance (Rs)': closing_balance
    })

    # Calculate Total Investment
    df['Total Investment (Rs)'] = initial_investment + df['Monthly Investment (Rs)'].cumsum()

    # Calculate Return
    df['Return (Rs)'] = df['Closing Balance (Rs)'] - df['Total Investment (Rs)']

    # Calculate Percentage Return
    df['Percentage Return (%)'] = (df['Return (Rs)'] / df['Total Investment (Rs)']) * 100
    
    return df


# Streamlit App
st.title('Investment Analysis')

# Input Form
st.subheader('Input Parameters')

col1, col2, col3 = st.columns(3)
with col1:
    initial_investment = st.number_input('Initial Investment (Rs)', min_value=0, step=10000, value=1000000)
with col2:
    num_years = st.number_input('Number of Years', min_value=1, max_value=50, value=5)
with col3:
    start_date = st.date_input('Start Date', value=datetime.now())

col1, col2,col3 = st.columns(3)

with col1:
    monthly_investment = st.number_input('Monthly Investment (Rs)', min_value=0, step=1000, value=100000)
with col2:
    investment_timing = st.selectbox('Monthly Investment Timing', ['Start of Month'], index=0)
with col3:
    stop_investment_date = st.date_input('Stop Monthly Investment Date', value=datetime.now() + timedelta(days=30*num_years))


st.subheader('Return Rate')
col1, col2 = st.columns(2)

with col1:
    return_frequency = st.selectbox('Return Calculation Frequency', ['Monthly', 'Yearly'], index=0)
with col2:
    if return_frequency == 'Monthly':
        return_label = 'Monthly Rate of Return (%)'
    else:
        return_label = 'Annual Rate of Return (%)'
    
    return_rate = st.number_input(return_label, min_value=0.0, max_value=100.0, step=0.1, value=4.0, format="%f")


# Generate Investment Data
investment_data = generate_investment_data(initial_investment, monthly_investment, return_rate, return_frequency, investment_timing, start_date.strftime("%Y-%m-%d"), num_years, stop_investment_date)
investment_data['Month_Year'] = investment_data['Month'] + ' ' + investment_data['Year'].astype(str)
# Format the 'Year' column as integers
investment_data['Year'] = investment_data['Year'].astype(int)



# Create tabs using st.tabs and display the bar and cumulative graph on each one
tab1, tab2, tab3 = st.tabs(["Monthly Investments and Returns", "Cumulative Investment Growth", "Investment Details"])

with tab1:
    st.write('Tab1 Content')
    bar_fig = px.bar(investment_data, x='Month_Year', y=['Monthly Investment (Rs)', 'Monthly Return (Rs)'], barmode='stack',
                    labels={'value': 'Amount (Rs)'}, title='Monthly Investments and Returns')
    st.plotly_chart(bar_fig, use_container_width=True)

with tab2:
    st.write('Tab2 Content')
    cumulative_fig = px.line(investment_data, x='Month_Year', y='Closing Balance (Rs)', title='Cumulative Investment Growth',
                            labels={'Closing Balance (Rs)': 'Closing Balance (Rs)', 'Year': 'Year'})
    st.plotly_chart(cumulative_fig, use_container_width=True)

with tab3:
    # Display Table
    st.write('Tab3 Content')
    st.write(investment_data)
