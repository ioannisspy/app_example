import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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

# Add a 'Year' column to the DataFrame, representing the years from 0 to time_period_years
df_portfolio_growth['Year'] = range(time_period_years + 1)

# Set up the professional matplotlib style
sns.set_style("whitegrid")
sns.set_palette("husl")

# Create the figure and axis
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the two scenarios
ax.plot(df_portfolio_growth['Year'], df_portfolio_growth['Lump Sum Only'], 
        marker='o', linewidth=3, markersize=6, label='Lump Sum Only', color='#1f77b4')
ax.plot(df_portfolio_growth['Year'], df_portfolio_growth['Lump Sum + Regular Savings'], 
        marker='s', linewidth=3, markersize=6, label='Lump Sum + Regular Savings', color='#ff7f0e')

# Format the y-axis to show currency
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, pos: f'${x:,.0f}'))

# Set labels and title
ax.set_xlabel('Years', fontsize=14, fontweight='bold')
ax.set_ylabel('Portfolio Value', fontsize=14, fontweight='bold')
ax.set_title('Investment Portfolio Growth: Lump Sum vs. Lump Sum + Regular Savings', 
             fontsize=16, fontweight='bold', pad=20)

# Add legend
ax.legend(fontsize=12, loc='upper left')

# Add grid for better readability
ax.grid(True, alpha=0.3)
ax.set_facecolor('#fafafa')

# Get the final portfolio values and year
final_value_lump_sum_only = df_portfolio_growth['Lump Sum Only'].iloc[-1]
final_value_lump_sum_and_savings = df_portfolio_growth['Lump Sum + Regular Savings'].iloc[-1]
final_year = df_portfolio_growth['Year'].iloc[-1]

# Calculate the total contributions
total_contributions_savings = monthly_contribution_lump_sum_and_savings * 12 * time_period_years

# Add annotations for final values
ax.annotate(f'${final_value_lump_sum_only:,.0f}', 
            xy=(final_year, final_value_lump_sum_only), 
            xytext=(10, 10), textcoords='offset points',
            fontsize=11, fontweight='bold', color='#1f77b4',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='#1f77b4', alpha=0.8))

ax.annotate(f'${final_value_lump_sum_and_savings:,.0f}', 
            xy=(final_year, final_value_lump_sum_and_savings), 
            xytext=(10, -20), textcoords='offset points',
            fontsize=11, fontweight='bold', color='#ff7f0e',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='#ff7f0e', alpha=0.8))

# Add a text box with summary information
summary_text = f'Total Additional Contributions: ${total_contributions_savings:,.0f}\n'
summary_text += f'Additional Return: ${final_value_lump_sum_and_savings - final_value_lump_sum_only - total_contributions_savings:,.0f}'
ax.text(0.02, 0.98, summary_text, transform=ax.transAxes, fontsize=10,
        verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))

# Adjust layout and display
plt.tight_layout()

# Try to show the plot
try:
    plt.show()
except:
    # If display fails, save as PNG and print summary
    plt.savefig('portfolio_analysis.png', dpi=300, bbox_inches='tight')
    print("Chart saved as 'portfolio_analysis.png'")
    
# Print summary data
print(f"\n📊 Investment Summary:")
print(f"Lump Sum Only Final Value: ${final_value_lump_sum_only:,.0f}")
print(f"Lump Sum + Savings Final Value: ${final_value_lump_sum_and_savings:,.0f}")
print(f"Additional Value from Savings: ${final_value_lump_sum_and_savings - final_value_lump_sum_only:,.0f}")
print(f"Total Additional Contributions: ${total_contributions_savings:,.0f}")
print(f"ROI on Additional Contributions: {((final_value_lump_sum_and_savings - final_value_lump_sum_only - total_contributions_savings) / total_contributions_savings * 100):.1f}%")