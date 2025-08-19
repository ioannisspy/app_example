# China Supply Chain Exposure Analyzer

## Overview
This tool analyzes company exposure to China through supply chains by examining SEC 10-K filings using AI analysis.

## Installation

1. Install required packages:
```bash
pip install -r requirements_china_analyzer.txt
```

## Required API Keys

### SEC API
- Sign up at: https://sec-api.io/
- Get your API key from the dashboard

### Anthropic API
- Sign up at: https://console.anthropic.com/
- Create an API key in your account settings

## Usage

1. Run the script:
```bash
python china_exposure_analyzer.py
```

2. Follow the prompts:
   - **Step 1**: Enter company tickers (e.g., AAPL,MSFT,GOOGL) and years (e.g., 2021,2022,2023)
   - **Step 2**: Enter your SEC API key and Anthropic API key, select AI model
   - **Step 3**: Choose which section of 10-K to analyze (recommended: "Risk Factors" or "Business")
   - **Step 4**: Wait for analysis and review results

## Output

The tool generates:
- Console output with progress updates
- Final results table showing Company, Year, and China Exposure Score (1-5)
- CSV file with timestamped results

## Scoring System

- **1**: Very Low/No exposure to China
- **2**: Low exposure (minimal mentions or indirect exposure)  
- **3**: Moderate exposure (some clear connections to China)
- **4**: High exposure (significant business relationships with China)
- **5**: Very High exposure (heavily dependent on China for supply chain or revenue)

## Example Usage

```
Enter company tickers: AAPL,TSLA,NKE
Enter years to analyze: 2022,2023
Enter your SEC API key: [your-sec-api-key]
Enter your Anthropic API key: [your-anthropic-key]
Select model: 1 (for claude-3-5-haiku-20241022)
Select section: 2 (for Risk Factors)
```

## Notes

- Analysis takes time due to API calls and document processing
- Large 10-K sections may be truncated to fit AI model limits
- Results are saved automatically with timestamp
- Rate limiting is implemented to be respectful to APIs
