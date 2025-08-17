# Save this code as a Python file (e.g., retirement_app.py)

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Define the function to calculate portfolio growth for two scenarios
def calculate_dual_portfolio_growth(initial_investment, annual_return_rate, monthly_contribution, time_period_years):
    """
    Calculates the annual portfolio value growth for two scenarios:
    Lump Sum Only and Lump Sum + Regular Savings.

    Args:
        initial_investment (float): The initial lump sum investment.
        annual_return_rate (float): The annual return rate as a decimal.
        monthly_contribution (float): The regular monthly contribution amount for the second scenario.
        time_period_years (int): The investment period in years.

    Returns:
        pd.DataFrame: A DataFrame with annual portfolio values for both scenarios.
    """
    annual_values_lump_sum_only = [initial_investment]
    annual_values_lump_sum_and_savings = [initial_investment]

    portfolio_value_lump_sum_only = initial_investment
    portfolio_value_lump_sum_and_savings = initial_investment

    for year in range(1, time_period_years + 1):
        # Lump Sum Only scenario calculation
        portfolio_value_lump_sum_only *= (1 + annual_return_rate)
        annual_values_lump_sum_only.append(portfolio_value_lump_sum_only)

        # Lump Sum + Regular Savings scenario calculation
        annual_contributions = monthly_contribution * 12
        portfolio_value_lump_sum_and_savings += annual_contributions
        portfolio_value_lump_sum_and_savings *= (1 + annual_return_rate)
        annual_values_lump_sum_and_savings.append(portfolio_value_lump_sum_and_savings)

    # Create a dictionary to hold the portfolio growth data for both scenarios and the years
    portfolio_data = {
        'Year': range(time_period_years + 1),
        'Lump Sum Only': annual_values_lump_sum_only,
        'Lump Sum + Regular Savings': annual_values_lump_sum_and_savings
    }

    # Convert the dictionary into a pandas DataFrame for easier handling and plotting
    df_portfolio_growth = pd.DataFrame(portfolio_data)

    # Return the DataFrame containing the growth data for both scenarios
    return df_portfolio_growth

# --- Streamlit App Layout ---

st.title('Retirement Portfolio Growth Calculator')

st.write("""
Use the sliders below to adjust the investment parameters and see how your retirement portfolio could grow under two scenarios:
'Lump Sum Only' and 'Lump Sum + Regular Savings'.
""")

# --- Input Widgets ---

st.sidebar.header('Investment Parameters')

initial_investment = st.sidebar.slider(
    'Initial Investment ($)',
    min_value=10000,
    max_value=1000000,
    step=5000,
    value=100000,
    format='$,.0f'
)

monthly_contribution = st.sidebar.slider(
    'Monthly Contribution ($)',
    min_value=0,
    max_value=5000,
    step=50,
    value=300,
    format='$,.0f'
)

annual_return_rate = st.sidebar.slider(
    'Annual Return Rate (%)',
    min_value=0.01,
    max_value=0.15,
    step=0.005,
    value=0.10,
    format='.1%'
)

time_period_years = st.sidebar.slider(
    'Time Period (Years)',
    min_value=5,
    max_value=40,
    step=1,
    value=30
)

# --- Calculation and Plotting ---

# Calculate portfolio growth based on current inputs
df = calculate_dual_portfolio_growth(initial_investment, annual_return_rate, monthly_contribution, time_period_years)

# Create a Plotly figure
fig = go.Figure()

# Add trace for 'Lump Sum Only' scenario
fig.add_trace(go.Scatter(x=df['Year'], y=df['Lump Sum Only'],
                         mode='lines',
                         name='Lump Sum Only',
                         line=dict(color='blue', width=2)))

# Add trace for 'Lump Sum + Regular Savings' scenario
fig.add_trace(go.Scatter(x=df['Year'], y=df['Lump Sum + Regular Savings'],
                         mode='lines',
                         name='Lump Sum + Regular Savings',
                         line=dict(color='red', width=2)))

# Update layout for better formatting
fig.update_layout(
    title='Retirement Portfolio Growth Comparison',
    xaxis_title='Year',
    yaxis_title='Portfolio Value',
    yaxis_tickprefix='$',
    yaxis_tickformat=',.0f',
    hovermode='x unified',
    template='plotly_white',
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    )
)

# Display the Plotly figure in the Streamlit app
st.plotly_chart(fig, use_container_width=True)

# --- Display Final Values ---
st.subheader('Final Portfolio Values (After {} Years)'.format(time_period_years))

final_value_lump_sum_only = df['Lump Sum Only'].iloc[-1]
final_value_lump_sum_and_savings = df['Lump Sum + Regular Savings'].iloc[-1]

st.write(f"**Lump Sum Only:** ${final_value_lump_sum_only:,.0f}")
st.write(f"**Lump Sum + Regular Savings:** ${final_value_lump_sum_and_savings:,.0f}")

# --- Display Summary Table for Years 10, 20, 30 (Optional) ---
# You can uncomment this section if you also want to show a table
# st.subheader('Portfolio Values at Years 10, 20, and 30')
# df_summary_years = df[df['Year'].isin([10, 20, 30])].copy()
# df_summary_years['Lump Sum Only'] = df_summary_years['Lump Sum Only'].apply(lambda x: f'${x:,.0f}')
# df_summary_years['Lump Sum + Regular Savings'] = df_summary_years['Lump Sum + Regular Savings'].apply(lambda x: f'${x:,.0f}')
# st.dataframe(df_summary_years.set_index('Year'))