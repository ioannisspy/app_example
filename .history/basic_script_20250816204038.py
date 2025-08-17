import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Define investment parameters
initial_investment = 100000  # Initial lump sum investment amount
annual_return_rate = 0.10    # Annual expected return rate (10%)
time_period_years = 30       # Investment period in years

# Define monthly contributions for each scenario
# Scenario 1: Lump Sum Only (no monthly contributions)
monthly_contribution_lump_sum_only = 0
# Scenario 2: Lump Sum + Regular Savings (with $300 monthly contributions)
monthly_contribution_lump_sum_and_savings = 300

# Function to calculate the annual growth of a portfolio
def calculate_portfolio_growth(initial_investment, annual_return_rate, monthly_contribution, time_period_years):
    """
    Calculates the annual portfolio value growth over a specified time period.

    Args:
        initial_investment (float): The initial lump sum investment.
        annual_return_rate (float): The annual return rate as a decimal (e.g., 0.10 for 10%).
        monthly_contribution (float): The regular monthly contribution amount.
        time_period_years (int): The investment period in years.

    Returns:
        list: A list of annual portfolio values, including the initial investment at Year 0.
    """
    # Initialize a list to store annual portfolio values, starting with the initial investment
    annual_values = [initial_investment]
    # Set the initial portfolio value for calculations
    portfolio_value = initial_investment

    # Loop through each year in the investment period
    for year in range(1, time_period_years + 1):
        # Calculate the total contributions made during the current year
        annual_contributions = monthly_contribution * 12

        # Add the annual contributions to the current portfolio value
        portfolio_value += annual_contributions

        # Apply the annual return
        # The return is applied to the total value (initial + contributions)
        portfolio_value *= (1 + annual_return_rate)

        # Append the calculated year-end portfolio value to the list
        annual_values.append(portfolio_value)

    # Return the list of annual portfolio values
    return annual_values

# Calculate portfolio growth for the 'Lump Sum Only' scenario
portfolio_values_lump_sum_only = calculate_portfolio_growth(
    initial_investment,
    annual_return_rate,
    monthly_contribution_lump_sum_only,
    time_period_years
)

# Calculate portfolio growth for the 'Lump Sum + Regular Savings' scenario
portfolio_values_lump_sum_and_savings = calculate_portfolio_growth(
    initial_investment,
    annual_return_rate,
    monthly_contribution_lump_sum_and_savings,
    time_period_years
)

# Create a dictionary to hold the portfolio growth data for both scenarios
portfolio_data = {
    'Lump Sum Only': portfolio_values_lump_sum_only,
    'Lump Sum + Regular Savings': portfolio_values_lump_sum_and_savings
}

# Convert the dictionary into a pandas DataFrame for easier handling and analysis
df_portfolio_growth = pd.DataFrame(portfolio_data)

# Add a 'Year' column to the DataFrame, representing the years from 0 to 30
df_portfolio_growth['Year'] = range(time_period_years + 1)

# Reshape the DataFrame for Plotly Express. This is needed to have a single column for 'Portfolio Value' and 'Scenario'.
df_melted = df_portfolio_growth.melt(id_vars=['Year'], var_name='Scenario', value_name='Portfolio Value')

# Create the interactive line chart using Plotly Express
fig = px.line(df_melted, x='Year', y='Portfolio Value', color='Scenario',
              title='Retirement Portfolio Growth: Lump Sum vs. Lump Sum + Regular Savings')

# Update layout for better formatting, including currency format for the y-axis and hover behavior
fig.update_layout(
    yaxis_tickprefix='$', # Add '$' prefix to y-axis ticks
    yaxis_tickformat=',.0f', # Format y-axis ticks as currency without decimals
    hovermode='x unified' # Shows hover information for both lines at a specific year
)

# Get the final portfolio values for annotation from the last row of the original DataFrame
final_value_lump_sum_only = df_portfolio_growth['Lump Sum Only'].iloc[-1]
final_value_lump_sum_and_savings = df_portfolio_growth['Lump Sum + Regular Savings'].iloc[-1]
# Get the final year for annotation positioning
final_year = df_portfolio_growth['Year'].iloc[-1]

# Calculate the total contributions made in the 'Lump Sum + Regular Savings' scenario
# Ensure 'time_period_years' and 'monthly_contribution_lump_sum_and_savings' are accessible
# These variables are defined at the beginning of this cell, so they are accessible here.
total_contributions_savings = monthly_contribution_lump_sum_and_savings * 12 * time_period_years

# Add annotations for final values using Plotly Graph Objects for more control over positioning and appearance
# Add annotation for the final value of the 'Lump Sum Only' scenario
fig.add_trace(go.Scatter(
    x=[final_year], # X-coordinate for the annotation point (the last year)
    y=[final_value_lump_sum_only], # Y-coordinate for the annotation point (the final value)
    mode='markers+text', # Display a marker and text
    text=[f'${final_value_lump_sum_only:,.0f}'], # The text to display (formatted final value)
    textposition='top center', # Position of the text relative to the marker
    showlegend=False, # Do not show this annotation in the legend
    marker=dict(size=8, color='blue') # Style the marker
))

# Add annotation for the final value of the 'Lump Sum + Regular Savings' scenario
fig.add_trace(go.Scatter(
    x=[final_year], # X-coordinate for the annotation point (the last year)
    y=[final_value_lump_sum_and_savings], # Y-coordinate for the annotation point (the final value)
    mode='markers+text', # Display a marker and text
    text=[f'${final_value_lump_sum_and_savings:,.0f}'], # The text to display (formatted final value)
    textposition='bottom center', # Position of the text relative to the marker
    showlegend=False, # Do not show this annotation in the legend
    marker=dict(size=8, color='red') # Style the marker
))

# Add an annotation for the total contributions in the 'Lump Sum + Regular Savings' scenario
fig.add_annotation(
    x=final_year / 2, # X-coordinate for the annotation text (midway through the years)
    y=final_value_lump_sum_and_savings / 4, # Y-coordinate for the annotation text (adjust position as needed)
    text=f'Total Contributions (Scenario 2): ${total_contributions_savings:,.0f}', # The text to display (formatted total contributions)
    showarrow=True, # Show an arrow pointing from the text to a point (although not strictly necessary for this text annotation)
    arrowhead=1, # Style of the arrowhead
    bgcolor="white", # Background color of the annotation box
    bordercolor="black", # Border color of the annotation box
    borderwidth=1, # Border width of the annotation box
    borderpad=4, # Padding around the text in the annotation box
    opacity=0.8 # Opacity of the annotation box
)

# Display the generated Plotly figure
# For VS Code Interactive window, use different renderer options
import plotly.io as pio

# Try different renderers for VS Code compatibility
try:
    # First try the default VS Code renderer
    pio.renderers.default = "vscode"
    fig.show()
except:
    try:
        # If that fails, try browser renderer
        pio.renderers.default = "browser"
        fig.show()
    except:
        # If all else fails, save as HTML and display path
        fig.write_html("portfolio_analysis.html")
        print("Chart saved as 'portfolio_analysis.html' - open this file in your browser to view the chart.")
        
        # Also print the summary data
        print(f"\n📊 Investment Summary:")
        print(f"Lump Sum Only Final Value: ${final_value_lump_sum_only:,.0f}")
        print(f"Lump Sum + Savings Final Value: ${final_value_lump_sum_and_savings:,.0f}")
        print(f"Additional Value from Savings: ${final_value_lump_sum_and_savings - final_value_lump_sum_only:,.0f}")
        print(f"Total Additional Contributions: ${total_contributions_savings:,.0f}")