# 💰 Portfolio Analyzer

A professional investment portfolio analysis tool that compares lump sum vs. lump sum + regular contributions investment strategies.

## 🚀 Live Demo

**Streamlit Cloud:** [Deploy to Streamlit Cloud](https://streamlit.io/cloud)

## 📱 Available Versions

1. **Streamlit Web App** (`streamlit_app.py`) - Interactive web interface
2. **Flask Web App** (`app.py`) - Professional web application with Chart.js
3. **Python Script** (`basic_script.py`) - Standalone analysis script

## 🛠️ Deployment Instructions

### Streamlit Cloud Deployment

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Add Streamlit portfolio analyzer"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Select `streamlit_app.py` as the main file
   - The `requirements.txt` will be automatically detected

### Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Streamlit app:**
   ```bash
   streamlit run streamlit_app.py
   ```

3. **Run Flask app:**
   ```bash
   python app.py
   ```

4. **Run standalone script:**
   ```bash
   python basic_script.py
   ```

## 📦 Requirements

All dependencies are listed in `requirements.txt`:
- streamlit>=1.28.0
- pandas>=2.0.0
- matplotlib>=3.7.0
- seaborn>=0.12.0
- numpy>=1.24.0

## 🎯 Features

### Streamlit App Features:
- **Interactive Input Controls:** Sliders and number inputs for all parameters
- **Real-time Analysis:** Instant portfolio calculations and visualization
- **Professional Charts:** Matplotlib with seaborn styling
- **Detailed Metrics:** ROI, final values, and year-by-year breakdown
- **Responsive Design:** Works on desktop and mobile devices

### Analysis Capabilities:
- Compare lump sum only vs. lump sum + monthly contributions
- Visualize portfolio growth over time
- Calculate total returns and ROI on additional contributions
- Year-by-year portfolio value breakdown
- Professional financial chart styling

## 🎨 Chart Features

- **Professional Styling:** Clean, publication-ready charts
- **Interactive Elements:** Hover information and annotations
- **Currency Formatting:** Proper financial number formatting
- **Responsive Design:** Charts adapt to screen size
- **Color-coded Lines:** Distinct colors for each investment strategy

## 📊 Input Parameters

- **Initial Investment:** Starting lump sum amount
- **Annual Return Rate:** Expected yearly return (0-30%)
- **Investment Period:** Number of years to invest
- **Monthly Contribution:** Additional monthly savings amount

## 🔧 Troubleshooting

### Common Streamlit Cloud Issues:

1. **ModuleNotFoundError:** Ensure `requirements.txt` is in the root directory
2. **Chart Display Issues:** Matplotlib charts work well with `st.pyplot()`
3. **Memory Issues:** Use caching with `@st.cache_data` for large datasets

### Local Development Issues:

1. **Virtual Environment:** Always activate your virtual environment
2. **Port Conflicts:** Streamlit uses port 8501, Flask uses 5000
3. **Display Issues:** Use headless mode for servers: `--server.headless true`

## 📈 Example Usage

```python
# Example calculation
initial_investment = 100000
annual_return_rate = 0.10  # 10%
monthly_contribution = 300
time_period_years = 30

# Results in approximately:
# Lump Sum Only: $1,744,940
# Lump Sum + Savings: $2,280,790
# Additional Return: $427,850 (on $108,000 contributions)
```

## 🚀 Next Steps

1. Push your repository to GitHub
2. Deploy on Streamlit Cloud using the GitHub integration
3. Share your live app URL!

---

Built with ❤️ using Streamlit, pandas, and matplotlib.