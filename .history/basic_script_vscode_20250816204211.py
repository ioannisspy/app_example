import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

# Configure Plotly for VS Code
pio.renderers.default = "vscode"

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

# Print summary data first
print("📊 Investment Portfolio Analysis")
print("=" * 50)

# Display the data table
print("\nPortfolio Growth Data (first 10 years):")
print(df_portfolio_growth.head(10).to_string(index=False, formatters={
    'Lump Sum Only': '${:,.0f}'.format,
    'Lump Sum + Regular Savings': '${:,.0f}'.format
}))

# Calculate summary statistics
final_value_lump_sum_only = df_portfolio_growth['Lump Sum Only'].iloc[-1]
final_value_lump_sum_and_savings = df_portfolio_growth['Lump Sum + Regular Savings'].iloc[-1]
total_contributions_savings = monthly_contribution_lump_sum_and_savings * 12 * time_period_years
difference = final_value_lump_sum_and_savings - final_value_lump_sum_only
roi_on_contributions = ((difference - total_contributions_savings) / total_contributions_savings * 100) if total_contributions_savings > 0 else 0

print(f"\n📈 Final Results after {time_period_years} years:")
print(f"Lump Sum Only Final Value: ${final_value_lump_sum_only:,.0f}")
print(f"Lump Sum + Savings Final Value: ${final_value_lump_sum_and_savings:,.0f}")
print(f"Additional Value from Savings: ${difference:,.0f}")
print(f"Total Additional Contributions: ${total_contributions_savings:,.0f}")
print(f"ROI on Additional Contributions: {roi_on_contributions:.1f}%")

# Reshape the DataFrame for Plotly Express
df_melted = df_portfolio_growth.melt(id_vars=['Year'], var_name='Scenario', value_name='Portfolio Value')

# Create the interactive line chart using Plotly Express
fig = px.line(df_melted, x='Year', y='Portfolio Value', color='Scenario',
              title=f'Investment Portfolio Growth Over {time_period_years} Years')

# Update layout for better formatting
fig.update_layout(
    yaxis_tickprefix='$',
    yaxis_tickformat=',.0f',
    hovermode='x unified',
    template='plotly_white',
    height=600,
    title_font_size=20,
    title_x=0.5
)

# Get the final year for annotation positioning
final_year = df_portfolio_growth['Year'].iloc[-1]

# Add annotations for final values
fig.add_trace(go.Scatter(
    x=[final_year],
    y=[final_value_lump_sum_only],
    mode='markers+text',
    text=[f'${final_value_lump_sum_only:,.0f}'],
    textposition='top center',
    showlegend=False,
    marker=dict(size=10, color='#636EFA')
))

fig.add_trace(go.Scatter(
    x=[final_year],
    y=[final_value_lump_sum_and_savings],
    mode='markers+text',
    text=[f'${final_value_lump_sum_and_savings:,.0f}'],
    textposition='bottom center',
    showlegend=False,
    marker=dict(size=10, color='#EF553B')
))

# Add annotation for total contributions
fig.add_annotation(
    x=final_year / 2,
    y=final_value_lump_sum_and_savings / 4,
    text=f'Total Additional Contributions: ${total_contributions_savings:,.0f}',
    showarrow=True,
    arrowhead=1,
    bgcolor="white",
    bordercolor="black",
    borderwidth=1,
    borderpad=4,
    opacity=0.9
)

# Display the chart with error handling
print(f"\n🎯 Generating interactive chart...")
try:
    fig.show()
    print("✅ Chart displayed successfully!")
except Exception as e:
    print(f"⚠️  Chart display issue: {e}")
    print("💡 Saving chart as HTML file instead...")
    
    # Save as HTML file
    fig.write_html("portfolio_analysis.html")
    print("📁 Chart saved as 'portfolio_analysis.html'")
    print("🌐 Open this file in your browser to view the interactive chart.")
