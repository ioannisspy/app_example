from flask import Flask, render_template, request, jsonify
import pandas as pd
import webbrowser
import threading
import time

app = Flask(__name__)

def calculate_portfolio_growth(initial_investment, annual_return_rate, monthly_contribution, time_period_years):
    """
    Calculates the annual portfolio value growth over a specified time period.
    """
    annual_values = [initial_investment]
    portfolio_value = initial_investment

    for year in range(1, time_period_years + 1):
        annual_contributions = monthly_contribution * 12
        portfolio_value += annual_contributions
        portfolio_value *= (1 + annual_return_rate)
        annual_values.append(portfolio_value)

    return annual_values

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    
    # Extract parameters from the form
    initial_investment = float(data['initial_investment'])
    annual_return_rate = float(data['annual_return_rate']) / 100  # Convert percentage to decimal
    time_period_years = int(data['time_period_years'])
    monthly_contribution_scenario2 = float(data['monthly_contribution'])
    
    # Calculate portfolio growth for both scenarios
    portfolio_values_lump_sum_only = calculate_portfolio_growth(
        initial_investment, annual_return_rate, 0, time_period_years
    )
    
    portfolio_values_lump_sum_and_savings = calculate_portfolio_growth(
        initial_investment, annual_return_rate, monthly_contribution_scenario2, time_period_years
    )
    
    # Create DataFrame
    portfolio_data = {
        'Lump Sum Only': portfolio_values_lump_sum_only,
        'Lump Sum + Regular Savings': portfolio_values_lump_sum_and_savings
    }
    
    df_portfolio_growth = pd.DataFrame(portfolio_data)
    df_portfolio_growth['Year'] = range(time_period_years + 1)
    
    # Get final values
    final_value_lump_sum_only = df_portfolio_growth['Lump Sum Only'].iloc[-1]
    final_value_lump_sum_and_savings = df_portfolio_growth['Lump Sum + Regular Savings'].iloc[-1]
    final_year = df_portfolio_growth['Year'].iloc[-1]
    
    # Calculate total contributions
    total_contributions_savings = monthly_contribution_scenario2 * 12 * time_period_years
    
    # Prepare Chart.js data
    chartData = {
        'years': df_portfolio_growth['Year'].tolist(),
        'lumpSumValues': df_portfolio_growth['Lump Sum Only'].tolist(),
        'combinedValues': df_portfolio_growth['Lump Sum + Regular Savings'].tolist()
    }
    
    # Calculate some summary statistics
    difference = final_value_lump_sum_and_savings - final_value_lump_sum_only
    roi_on_contributions = ((difference - total_contributions_savings) / total_contributions_savings * 100) if total_contributions_savings > 0 else 0
    
    summary = {
        'final_lump_sum': final_value_lump_sum_only,
        'final_combined': final_value_lump_sum_and_savings,
        'difference': difference,
        'total_contributions': total_contributions_savings,
        'roi_on_contributions': roi_on_contributions
    }
    
    return jsonify({'chartData': chartData, 'summary': summary})

def open_browser():
    time.sleep(1.5)  # Wait for the server to start
    webbrowser.open('http://127.0.0.1:5000/')

if __name__ == '__main__':
    # Open browser in a separate thread
    threading.Thread(target=open_browser).start()
    # Run the Flask app
    app.run(debug=False, port=5000)