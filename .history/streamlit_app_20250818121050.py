import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set page configuration
st.set_page_config(
    page_title="Portfolio Analyzer",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Function to calculate portfolio growth
def calculate_portfolio_growth(initial_investment, annual_return_rate, monthly_contribution, time_period_years):
    """
    Calculates the annual portfolio value growth over a specified time period.
    This assumes monthly contributions are made at the end of each year after growth is applied.
    """
    annual_values = [initial_investment]
    portfolio_value = initial_investment

    for year in range(1, time_period_years + 1):
        # Apply growth to current portfolio value first
        portfolio_value *= (1 + annual_return_rate)
        # Then add annual contributions (assumes contributions made at year-end)
        annual_contributions = monthly_contribution * 12
        portfolio_value += annual_contributions
        annual_values.append(portfolio_value)

    return annual_values

# Main app
def main():
    st.title("💰 Investment Portfolio Analyzer")
    st.markdown("### Compare investment strategies with professional analysis")
    
    # Sidebar for inputs
    st.sidebar.header("Investment Parameters")
    
    # Input widgets
    initial_investment = st.sidebar.number_input(
        "Initial Investment ($)",
        min_value=1,
        value=100000,
        step=1000,
        help="Enter your initial lump sum investment amount"
    )
    
    annual_return_rate = st.sidebar.slider(
        "Expected Annual Return (%)",
        min_value=0.0,
        max_value=30.0,
        value=10.0,
        step=0.1,
        help="Expected annual return rate as a percentage"
    )
    
    time_period_years = st.sidebar.number_input(
        "Investment Period (Years)",
        min_value=1,
        max_value=100,
        value=30,
        step=1,
        help="How many years will you invest for?"
    )
    
    monthly_contribution = st.sidebar.number_input(
        "Monthly Contribution ($)",
        min_value=0,
        value=300,
        step=25,
        help="Additional monthly contribution for scenario 2"
    )
    
    # Calculate button
    if st.sidebar.button("Analyze Portfolio", type="primary"):
        # Convert percentage to decimal
        annual_return_rate_decimal = annual_return_rate / 100
        
        # Calculate portfolio growth for both scenarios
        portfolio_values_lump_sum_only = calculate_portfolio_growth(
            initial_investment, annual_return_rate_decimal, 0, time_period_years
        )
        
        portfolio_values_lump_sum_and_savings = calculate_portfolio_growth(
            initial_investment, annual_return_rate_decimal, monthly_contribution, time_period_years
        )
        
        # Create DataFrame
        portfolio_data = {
            'Lump Sum Only': portfolio_values_lump_sum_only,
            'Lump Sum + Regular Savings': portfolio_values_lump_sum_and_savings
        }
        
        df_portfolio_growth = pd.DataFrame(portfolio_data)
        df_portfolio_growth['Year'] = range(time_period_years + 1)
        
        # Create two columns for layout
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("📈 Portfolio Growth Visualization")
            
            # Set up professional matplotlib style
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
            ax.set_title(f'Investment Portfolio Growth Over {time_period_years} Years', 
                         fontsize=16, fontweight='bold', pad=20)
            
            # Add legend
            ax.legend(fontsize=12, loc='upper left')
            
            # Add grid for better readability
            ax.grid(True, alpha=0.3)
            ax.set_facecolor('#fafafa')
            
            # Get final values
            final_value_lump_sum_only = df_portfolio_growth['Lump Sum Only'].iloc[-1]
            final_value_lump_sum_and_savings = df_portfolio_growth['Lump Sum + Regular Savings'].iloc[-1]
            final_year = df_portfolio_growth['Year'].iloc[-1]
            
            # Calculate total contributions
            total_contributions_savings = monthly_contribution * 12 * time_period_years
            
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
            
            # Adjust layout and display in Streamlit
            plt.tight_layout()
            st.pyplot(fig)
            
        with col2:
            st.subheader("📊 Investment Summary")
            
            # Calculate metrics
            difference = final_value_lump_sum_and_savings - final_value_lump_sum_only
            additional_return = difference - total_contributions_savings
            roi_on_contributions = (additional_return / total_contributions_savings * 100) if total_contributions_savings > 0 else 0
            
            # Display metrics
            st.metric(
                "Lump Sum Only Final Value",
                f"${final_value_lump_sum_only:,.0f}",
                help="Portfolio value with only the initial investment"
            )
            
            st.metric(
                "Lump Sum + Savings Final Value",
                f"${final_value_lump_sum_and_savings:,.0f}",
                delta=f"${difference:,.0f}",
                help="Portfolio value with initial investment plus monthly contributions"
            )
            
            st.metric(
                "Total Additional Contributions",
                f"${total_contributions_savings:,.0f}",
                help="Total amount of monthly contributions over the investment period"
            )
            
            st.metric(
                "Additional Return from Savings",
                f"${additional_return:,.0f}",
                help="Extra gains from compound growth on monthly contributions"
            )
            
            st.metric(
                "ROI on Additional Contributions",
                f"{roi_on_contributions:.1f}%",
                help="Return on investment for the monthly contributions"
            )
            
            # Show data table
            st.subheader("📋 Year-by-Year Breakdown")
            
            # Create a more readable version of the data
            display_df = df_portfolio_growth.copy()
            display_df['Lump Sum Only'] = display_df['Lump Sum Only'].apply(lambda x: f"${x:,.0f}")
            display_df['Lump Sum + Regular Savings'] = display_df['Lump Sum + Regular Savings'].apply(lambda x: f"${x:,.0f}")
            
            # Show every 5th year for readability, plus first and last
            if time_period_years <= 10:
                years_to_show = display_df.index
            else:
                years_to_show = list(range(0, time_period_years + 1, 5))
                if time_period_years not in years_to_show:
                    years_to_show.append(time_period_years)
            
            st.dataframe(
                display_df.iloc[years_to_show],
                use_container_width=True,
                height=300
            )

if __name__ == "__main__":
    main()