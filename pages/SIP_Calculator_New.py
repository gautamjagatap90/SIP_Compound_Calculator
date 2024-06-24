import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(layout="wide")

# Function to generate investment data
def generate_investment_data(initial_investment, monthly_investment, return_rate, return_frequency, investment_timing, start_date, num_years, stop_investment_date, min_reinvestment):
    # Initialize lists to store data
    years = []
    months = []
    starting_balance = []
    monthly_sip = []
    monthly_return = []
    carryover_from_prev = []
    additional_amount = []
    reinvestable = []
    reinvestable_amount = []
    carryover_to_next = []
    closing_balance = []
    total_investment = []
    total_return = []
    percentage_return = []

    # Convert start_date string to datetime object
    start_date = datetime.strptime(start_date, "%Y-%m-%d")

    # Calculate the number of months to stop investment
    stop_investment_month = (stop_investment_date.year - start_date.year) * 12 + (stop_investment_date.month - start_date.month)

    # Generate investment data for each month
    current_date = start_date
    carryover = 0
    cumulative_investment = initial_investment
    for i in range(num_years * 12):
        # Append year and month
        years.append(current_date.year)
        months.append(current_date.strftime("%B"))

        # Calculate starting balance
        if i == 0:
            starting_balance.append(initial_investment)
            carryover_from_prev.append(0)
        else:
            starting_balance.append(closing_balance[-1])
            carryover_from_prev.append(carryover_to_next[-1])

        # Calculate monthly SIP
        if i < stop_investment_month:
            monthly_sip.append(monthly_investment)
            cumulative_investment += monthly_investment
        else:
            monthly_sip.append(0)

        # Calculate monthly return
        if return_frequency == 'Monthly':
            monthly_return.append(starting_balance[-1] * (return_rate / 100))
        else:
            monthly_return.append(starting_balance[-1] * ((1 + return_rate / 100) ** (1 / 12) - 1))

        # Calculate additional amount and reinvestment logic
        total_amount = monthly_return[-1] + monthly_sip[-1] + carryover_from_prev[-1]
        additional_amount.append(total_amount)
        
        if total_amount >= min_reinvestment:
            reinvest = (total_amount // min_reinvestment) * min_reinvestment
            carryover = total_amount % min_reinvestment
            reinvestable.append("Yes")
        else:
            reinvest = 0
            carryover = total_amount
            reinvestable.append("No")

        reinvestable_amount.append(reinvest)
        carryover_to_next.append(carryover)
        closing_balance.append(starting_balance[-1] + reinvest)

        # Calculate total investment, total return, and percentage return
        total_investment.append(cumulative_investment)
        total_ret = closing_balance[-1] - cumulative_investment
        total_return.append(total_ret)
        percentage_ret = (total_ret / cumulative_investment) * 100 if cumulative_investment > 0 else 0
        percentage_return.append(f"{round(percentage_ret, 0)}%")

        # Move to next month
        current_date += timedelta(days=30)

    # Create DataFrame
    df = pd.DataFrame({
        'Year': years,
        'Month': months,
        'Starting Balance (Rs)': starting_balance,
        'Monthly Investment (Rs)': monthly_sip,
        'Monthly Return (Rs)': monthly_return,
        'Carryover from Prev (Rs)': carryover_from_prev,
        'Additional Amount (Rs)': additional_amount,
        'Reinvestable (Yes/No)': reinvestable,
        'Reinvestable Amount (Rs)': reinvestable_amount,
        'Carryover to Next (Rs)': carryover_to_next,
        'Closing Balance (Rs)': closing_balance,
        'Total Investment (Rs)': total_investment,
        'Total Return (Rs)': total_return,
        'Percentage Return (%)': percentage_return
    })

    return df

# Streamlit App
st.title('Investment Analysis')

# Input Form
st.subheader('Input Parameters')

st.markdown("---")
st.markdown("### Initial Investment")
col1, col2, col3 = st.columns(3)
with col1:
    initial_investment = st.number_input('Initial Investment (Rs)', min_value=0, step=10000, value=1000000)
with col2:
    num_years = st.number_input('Number of Years', min_value=1, max_value=50, value=5)
with col3:
    start_date = st.date_input('Start Date', value=datetime.now())

# st.markdown("---")
st.markdown("### Monthly SIP Investment")

col1, col2, col3 = st.columns(3)
with col1:
    monthly_investment = st.number_input('Monthly Investment (Rs)', min_value=0, step=1000, value=50000)
with col2:
    investment_timing = st.selectbox('Monthly Investment Timing', ['Start of Month'], index=0)
with col3:
    stop_investment_date = st.date_input('Stop Monthly Investment Date', value=datetime.now() + timedelta(days=30*num_years))

# st.markdown("---")
st.markdown("### Calculation Parameters")

col1, col2, col3 = st.columns(3)
with col1:
    min_reinvestment = st.number_input('Minimum Reinvestment Amount (Rs)', min_value=0, step=1000, value=100000)
with col2:
    return_frequency = st.selectbox('Return Calculation Frequency', ['Monthly', 'Yearly'], index=0)
    return_label = 'Monthly Rate of Return (%)' if return_frequency == 'Monthly' else 'Annual Rate of Return (%)'
with col3:
    return_rate = st.number_input(return_label, min_value=0.0, max_value=100.0, step=0.5, value=4.0, format="%f")

# Generate Investment Data
investment_data = generate_investment_data(initial_investment, monthly_investment, return_rate, return_frequency, investment_timing, start_date.strftime("%Y-%m-%d"), num_years, stop_investment_date, min_reinvestment)
investment_data['Month_Year'] = investment_data['Month'] + ' ' + investment_data['Year'].astype(str)

# Create tabs using st.tabs and display the bar and cumulative graph on each one
tab1, tab2, tab3 = st.tabs(["Monthly Investments and Returns", "Cumulative Investment Growth", "Investment Details"])

with tab1:
    bar_fig = px.bar(investment_data, x='Month_Year', y=['Monthly Investment (Rs)', 'Monthly Return (Rs)', 'Reinvestable Amount (Rs)'], barmode='stack',
                     labels={'value': 'Amount (Rs)'}, title='Monthly Investments and Returns')
    st.plotly_chart(bar_fig, use_container_width=True)

with tab2:
    cumulative_fig = px.line(investment_data, x='Month_Year', y='Closing Balance (Rs)', title='Cumulative Investment Growth',
                             labels={'Closing Balance (Rs)': 'Closing Balance (Rs)', 'Year': 'Year'})
    st.plotly_chart(cumulative_fig, use_container_width=True)

with tab3:
    st.write(investment_data)
