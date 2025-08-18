import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FuncFormatter

def calculate_portfolio_growth(initial_amount, monthly_contribution, annual_return_rate, years):
    """
    Calculate portfolio growth over time with compound interest.
    
    Args:
        initial_amount (float): Initial lump sum investment
        monthly_contribution (float): Monthly contribution amount
        annual_return_rate (float): Annual return rate (as decimal, e.g., 0.10 for 10%)
        years (int): Number of years to calculate
    
    Returns:
        tuple: (portfolio_values, total_contributions)
    """
    monthly_rate = annual_return_rate / 12
    months = years * 12
    
    portfolio_values = []
    total_contributions = []
    
    # Start with initial investment
    current_value = initial_amount
    total_contrib = initial_amount
    
    for month in range(months + 1):
        portfolio_values.append(current_value)
        total_contributions.append(total_contrib)
        
        if month < months:  # Don't add contribution after the last month
            # Add monthly contribution
            current_value += monthly_contribution
            total_contrib += monthly_contribution
            
            # Apply monthly growth
            current_value *= (1 + monthly_rate)
    
    return np.array(portfolio_values), np.array(total_contributions)

def format_currency(x, pos):
    """Format numbers as currency for matplotlib axes."""
    if x >= 1e6:
        return f'${x/1e6:.1f}M'
    elif x >= 1e3:
        return f'${x/1e3:.0f}K'
    else:
        return f'${x:.0f}'

def main():
    # Investment parameters
    initial_investment = 100000  # $100,000
    annual_return = 0.10        # 10% annual return
    years = 30                  # 30 years
    
    # Scenario 1: Lump Sum Only
    scenario1_monthly = 0       # No monthly contributions
    
    # Scenario 2: Lump Sum + Regular Savings
    scenario2_monthly = 300     # $300 monthly contributions
    
    # Calculate portfolio growth for both scenarios
    print("Calculating portfolio growth scenarios...")
    
    portfolio1, contributions1 = calculate_portfolio_growth(
        initial_investment, scenario1_monthly, annual_return, years
    )
    
    portfolio2, contributions2 = calculate_portfolio_growth(
        initial_investment, scenario2_monthly, annual_return, years
    )
    
    # Create time array (in years)
    time_years = np.linspace(0, years, len(portfolio1))
    
    # Create the visualization
    plt.figure(figsize=(14, 10))
    
    # Main plot
    plt.subplot(2, 1, 1)
    
    # Plot both scenarios
    line1 = plt.plot(time_years, portfolio1, 'b-', linewidth=3, 
                     label='Lump Sum Only', alpha=0.8)
    line2 = plt.plot(time_years, portfolio2, 'r-', linewidth=3, 
                     label='Lump Sum + Regular Savings', alpha=0.8)
    
    # Formatting
    plt.title('Retirement Portfolio Growth Comparison\n30-Year Investment with 10% Annual Return', 
              fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Years', fontsize=12, fontweight='bold')
    plt.ylabel('Portfolio Value', fontsize=12, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=12, loc='upper left')
    
    # Format y-axis as currency
    plt.gca().yaxis.set_major_formatter(FuncFormatter(format_currency))
    
    # Add annotations for final values
    final_value1 = portfolio1[-1]
    final_value2 = portfolio2[-1]
    final_contrib1 = contributions1[-1]
    final_contrib2 = contributions2[-1]
    
    # Annotation for Scenario 1
    plt.annotate(f'Final Value: ${final_value1:,.0f}\nTotal Invested: ${final_contrib1:,.0f}',
                xy=(years, final_value1), xytext=(years-8, final_value1+200000),
                fontsize=10, ha='center', va='bottom',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='lightblue', alpha=0.8),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.2'))
    
    # Annotation for Scenario 2
    plt.annotate(f'Final Value: ${final_value2:,.0f}\nTotal Invested: ${final_contrib2:,.0f}',
                xy=(years, final_value2), xytext=(years-8, final_value2-300000),
                fontsize=10, ha='center', va='top',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='lightcoral', alpha=0.8),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=-0.2'))
    
    # Create data table
    plt.subplot(2, 1, 2)
    plt.axis('off')
    
    # Extract values for specific years
    years_to_show = [10, 20, 30]
    table_data = []
    
    for year in years_to_show:
        idx = int(year * 12)  # Convert to month index
        table_data.append([
            f'Year {year}',
            f'${portfolio1[idx]:,.0f}',
            f'${contributions1[idx]:,.0f}',
            f'${portfolio2[idx]:,.0f}',
            f'${contributions2[idx]:,.0f}'
        ])
    
    # Create table
    table = plt.table(cellText=table_data,
                     colLabels=['Time Period', 'Lump Sum\nPortfolio Value', 'Lump Sum\nTotal Invested',
                               'Lump Sum + Savings\nPortfolio Value', 'Lump Sum + Savings\nTotal Invested'],
                     cellLoc='center',
                     loc='center',
                     bbox=[0, 0.3, 1, 0.4])
    
    # Format table
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 2)
    
    # Style header row
    for i in range(5):
        table[(0, i)].set_facecolor('#4CAF50')
        table[(0, i)].set_text_props(weight='bold', color='white')
    
    # Style data rows with alternating colors
    colors = ['#f2f2f2', '#ffffff']
    for i in range(1, 4):
        for j in range(5):
            table[(i, j)].set_facecolor(colors[i % 2])
    
    plt.title('Portfolio Values at Key Milestones', fontsize=14, fontweight='bold', y=0.85)
    
    # Add summary statistics
    difference = final_value2 - final_value1
    extra_invested = final_contrib2 - final_contrib1
    
    summary_text = f"""
    Summary After 30 Years:
    • Difference in final portfolio value: ${difference:,.0f}
    • Additional amount invested in Scenario 2: ${extra_invested:,.0f}
    • Return on additional investment: {((difference/extra_invested) - 1)*100:.1f}%
    • Monthly savings of $300 resulted in ${difference:,.0f} more wealth
    """
    
    plt.text(0.02, 0.15, summary_text, transform=plt.gca().transAxes, fontsize=11,
             bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', alpha=0.8),
             verticalalignment='top')
    
    plt.tight_layout()
    plt.show()
    
    # Print detailed results
    print("\n" + "="*60)
    print("RETIREMENT PORTFOLIO ANALYSIS RESULTS")
    print("="*60)
    print(f"Investment Period: {years} years")
    print(f"Annual Return Rate: {annual_return*100}%")
    print(f"Initial Investment: ${initial_investment:,}")
    print("\nSCENARIO 1 - LUMP SUM ONLY:")
    print(f"  Monthly Contributions: ${scenario1_monthly}")
    print(f"  Final Portfolio Value: ${final_value1:,.2f}")
    print(f"  Total Amount Invested: ${final_contrib1:,.2f}")
    print(f"  Total Growth: ${final_value1 - final_contrib1:,.2f}")
    
    print("\nSCENARIO 2 - LUMP SUM + REGULAR SAVINGS:")
    print(f"  Monthly Contributions: ${scenario2_monthly}")
    print(f"  Final Portfolio Value: ${final_value2:,.2f}")
    print(f"  Total Amount Invested: ${final_contrib2:,.2f}")
    print(f"  Total Growth: ${final_value2 - final_contrib2:,.2f}")
    
    print(f"\nDIFFERENCE:")
    print(f"  Additional Portfolio Value: ${difference:,.2f}")
    print(f"  Additional Investment: ${extra_invested:,.2f}")
    print(f"  Effective Return on Additional Investment: {((difference/extra_invested) - 1)*100:.2f}%")

if __name__ == "__main__":
    main()
