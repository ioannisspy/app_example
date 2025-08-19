#!/usr/bin/env python3
"""
China Supply Chain Exposure Analyzer for 10-K Filings
Analyzes company exposure to China through supply chain using SEC filings and Anthropic AI
"""

import os
import json
import pandas as pd
from datetime import datetime
from typing import List, Dict, Tuple
import time

try:
    from sec_api import QueryApi, ExtractorApi
    import anthropic
except ImportError as e:
    print("Missing required packages. Please install:")
    print("pip install sec-api anthropic pandas")
    exit(1)


class ChinaExposureAnalyzer:
    
    # Available Anthropic models with selection options
    ANTHROPIC_MODELS = {
        "1": "claude-3-5-haiku-20241022",
        "2": "claude-3-5-sonnet-20241022", 
        "3": "claude-3-opus-20240229",
        "4": "claude-3-sonnet-20240229",
        "5": "claude-3-haiku-20240307"
    }
    
    # 10-K sections with selection options
    FILING_SECTIONS = {
        "1": ("1", "Business"),
        "2": ("1A", "Risk Factors"),
        "3": ("1B", "Unresolved Staff Comments"),
        "4": ("2", "Properties"),
        "5": ("3", "Legal Proceedings"),
        "6": ("4", "Mine Safety Disclosures"),
        "7": ("5", "Market for Registrant's Common Equity"),
        "8": ("6", "Consolidated Financial Data"),
        "9": ("7", "Management's Discussion and Analysis"),
        "10": ("7A", "Quantitative and Qualitative Disclosures About Market Risk"),
        "11": ("8", "Financial Statements and Supplementary Data"),
        "12": ("9", "Changes in and Disagreements with Accountants"),
        "13": ("9A", "Controls and Procedures"),
        "14": ("9B", "Other Information"),
        "15": ("9C", "Disclosure Regarding Foreign Jurisdictions"),
        "16": ("10", "Directors, Executive Officers and Corporate Governance"),
        "17": ("11", "Executive Compensation"),
        "18": ("12", "Security Ownership"),
        "19": ("13", "Certain Relationships and Related Transactions"),
        "20": ("14", "Principal Accounting Fees and Services"),
        "21": ("15", "Exhibits, Financial Statement Schedules")
    }
    
    def __init__(self):
        self.sec_query_api = None
        self.sec_extractor_api = None
        self.anthropic_client = None
        self.selected_model = None
        self.selected_section = None
        self.results = []
    
    def get_user_inputs(self) -> Tuple[List[str], List[int]]:
        """Step 1: Get firm tickers and years from user"""
        print("=" * 60)
        print("CHINA SUPPLY CHAIN EXPOSURE ANALYZER")
        print("=" * 60)
        print()
        
        # Get tickers
        print("Step 1: Enter company information")
        print("-" * 30)
        tickers_input = input("Enter company tickers (comma-separated, e.g., AAPL,MSFT,GOOGL): ").strip()
        tickers = [ticker.strip().upper() for ticker in tickers_input.split(",") if ticker.strip()]
        
        if not tickers:
            print("Error: No tickers provided!")
            exit(1)
        
        # Get years
        years_input = input("Enter years to analyze (comma-separated, e.g., 2021,2022,2023): ").strip()
        try:
            years = [int(year.strip()) for year in years_input.split(",") if year.strip()]
        except ValueError:
            print("Error: Invalid year format!")
            exit(1)
        
        if not years:
            print("Error: No years provided!")
            exit(1)
        
        print(f"\nAnalyzing {len(tickers)} companies for {len(years)} years...")
        print(f"Companies: {', '.join(tickers)}")
        print(f"Years: {', '.join(map(str, years))}")
        
        return tickers, years
    
    def setup_apis(self):
        """Step 2: Setup APIs with user credentials"""
        print("\n" + "=" * 60)
        print("Step 2: API Configuration")
        print("-" * 30)
        
        # SEC API setup
        sec_api_key = input("Enter your SEC API key: ").strip()
        if not sec_api_key:
            print("Error: SEC API key is required!")
            exit(1)
        
        try:
            self.sec_query_api = QueryApi(api_key=sec_api_key)
            self.sec_extractor_api = ExtractorApi(api_key=sec_api_key)
            print("✓ SEC API configured successfully")
        except Exception as e:
            print(f"Error configuring SEC API: {e}")
            exit(1)
        
        # Anthropic API setup
        anthropic_api_key = input("Enter your Anthropic API key: ").strip()
        if not anthropic_api_key:
            print("Error: Anthropic API key is required!")
            exit(1)
        
        try:
            self.anthropic_client = anthropic.Anthropic(api_key=anthropic_api_key)
            print("✓ Anthropic API configured successfully")
        except Exception as e:
            print(f"Error configuring Anthropic API: {e}")
            exit(1)
        
        # Model selection
        print("\nAvailable Anthropic models:")
        for key, model in self.ANTHROPIC_MODELS.items():
            print(f"  {key}. {model}")
        
        model_choice = input("Select model (enter number): ").strip()
        if model_choice not in self.ANTHROPIC_MODELS:
            print("Error: Invalid model selection!")
            exit(1)
        
        self.selected_model = self.ANTHROPIC_MODELS[model_choice]
        print(f"✓ Selected model: {self.selected_model}")
    
    def select_filing_section(self):
        """Step 3: Select which section of 10-K to analyze"""
        print("\n" + "=" * 60)
        print("Step 3: Select 10-K Section to Analyze")
        print("-" * 30)
        
        print("Available 10-K sections:")
        for key, (section_num, section_name) in self.FILING_SECTIONS.items():
            print(f"  {key:2}. Item {section_num}: {section_name}")
        
        section_choice = input("\nSelect section to analyze (enter number): ").strip()
        if section_choice not in self.FILING_SECTIONS:
            print("Error: Invalid section selection!")
            exit(1)
        
        self.selected_section = self.FILING_SECTIONS[section_choice]
        section_num, section_name = self.selected_section
        print(f"✓ Selected section: Item {section_num} - {section_name}")
    
    def get_10k_filing(self, ticker: str, year: int) -> str:
        """Download and extract specific section from 10-K filing"""
        try:
            # Query for 10-K filing
            query = {
                "query": f"ticker:{ticker} AND filedAt:[{year}-01-01 TO {year}-12-31] AND formType:\"10-K\"",
                "from": "0",
                "size": "1",
                "sort": [{"filedAt": {"order": "desc"}}]
            }
            
            print(f"  Searching for {ticker} 10-K filing for {year}...")
            filings = self.sec_query_api.get_filings(query)
            
            if not filings['filings']:
                print(f"  Warning: No 10-K filing found for {ticker} in {year}")
                return None
            
            filing_url = filings['filings'][0]['linkToFilingDetails']
            section_num, section_name = self.selected_section
            
            print(f"  Extracting Item {section_num} ({section_name})...")
            
            # Extract the specific section
            section_text = self.sec_extractor_api.get_section(filing_url, section_num, "text")
            
            if not section_text:
                print(f"  Warning: Could not extract Item {section_num} for {ticker}")
                return None
            
            return section_text
            
        except Exception as e:
            print(f"  Error getting filing for {ticker}: {e}")
            return None
    
    def analyze_china_exposure(self, company_name: str, filing_text: str) -> int:
        """Analyze China exposure using Anthropic API"""
        if not filing_text:
            return 0
        
        # Truncate text if too long (Anthropic has token limits)
        max_chars = 50000  # Approximately 12,500 tokens
        if len(filing_text) > max_chars:
            filing_text = filing_text[:max_chars] + "\n[Text truncated due to length]"
        
        prompt = f"""
        Please analyze the following 10-K filing section for {company_name} and determine their exposure to China through the supply chain.

        Consider both:
        1. China as a supplier (sourcing materials, components, manufacturing from China)
        2. China as a customer (selling products/services to Chinese market)

        Rate the exposure on a scale of 1-5:
        1 = Very Low/No exposure to China
        2 = Low exposure (minimal mentions or indirect exposure)
        3 = Moderate exposure (some clear connections to China)
        4 = High exposure (significant business relationships with China)
        5 = Very High exposure (heavily dependent on China for supply chain or revenue)

        Focus on:
        - Supply chain dependencies
        - Manufacturing locations
        - Key suppliers or customers in China
        - Revenue from Chinese operations
        - Strategic importance of China to the business
        - Risk factors related to China

        Filing text:
        {filing_text}

        Please respond with only a number from 1-5, followed by a brief 1-2 sentence explanation.
        """
        
        try:
            print(f"  Analyzing China exposure using {self.selected_model}...")
            
            response = self.anthropic_client.messages.create(
                model=self.selected_model,
                max_tokens=200,
                messages=[{"role": "user", "content": prompt}]
            )
            
            response_text = response.content[0].text.strip()
            
            # Extract score (first number in response)
            score_line = response_text.split('\n')[0]
            score = int(score_line.split()[0])
            
            if score < 1 or score > 5:
                print(f"  Warning: Invalid score {score}, defaulting to 3")
                score = 3
            
            explanation = response_text.replace(str(score), '').strip()
            print(f"  Score: {score}/5 - {explanation[:100]}...")
            
            return score
            
        except Exception as e:
            print(f"  Error analyzing with Anthropic: {e}")
            return 3  # Default to moderate if analysis fails
    
    def process_companies(self, tickers: List[str], years: List[int]):
        """Step 4: Process all companies and generate results"""
        print("\n" + "=" * 60)
        print("Step 4: Processing Companies")
        print("-" * 30)
        
        total_analyses = len(tickers) * len(years)
        current_analysis = 0
        
        for ticker in tickers:
            print(f"\nProcessing {ticker}:")
            
            for year in years:
                current_analysis += 1
                print(f"\n[{current_analysis}/{total_analyses}] Analyzing {ticker} for {year}:")
                
                # Get 10-K filing
                filing_text = self.get_10k_filing(ticker, year)
                
                # Analyze China exposure
                score = self.analyze_china_exposure(ticker, filing_text)
                
                # Store result
                self.results.append({
                    'Company': ticker,
                    'Year': year,
                    'Score': score
                })
                
                # Small delay to be respectful to APIs
                time.sleep(1)
        
        self.display_results()
    
    def display_results(self):
        """Display final results table"""
        print("\n" + "=" * 60)
        print("ANALYSIS RESULTS")
        print("=" * 60)
        
        if not self.results:
            print("No results to display.")
            return
        
        # Create DataFrame
        df = pd.DataFrame(self.results)
        
        # Display table
        print("\nChina Supply Chain Exposure Scores (1=Low, 5=High):")
        print("-" * 50)
        print(df.to_string(index=False))
        
        # Summary statistics
        print(f"\nSummary:")
        print(f"Total companies analyzed: {df['Company'].nunique()}")
        print(f"Total years analyzed: {df['Year'].nunique()}")
        print(f"Average exposure score: {df['Score'].mean():.2f}")
        print(f"Highest exposure score: {df['Score'].max()}")
        print(f"Lowest exposure score: {df['Score'].min()}")
        
        # Save to CSV
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"china_exposure_analysis_{timestamp}.csv"
        df.to_csv(filename, index=False)
        print(f"\nResults saved to: {filename}")
    
    def run(self):
        """Main execution flow"""
        try:
            # Step 1: Get user inputs
            tickers, years = self.get_user_inputs()
            
            # Step 2: Setup APIs
            self.setup_apis()
            
            # Step 3: Select filing section
            self.select_filing_section()
            
            # Step 4: Process companies
            self.process_companies(tickers, years)
            
        except KeyboardInterrupt:
            print("\n\nAnalysis interrupted by user.")
        except Exception as e:
            print(f"\nError during analysis: {e}")


def main():
    """Main function"""
    analyzer = ChinaExposureAnalyzer()
    analyzer.run()


if __name__ == "__main__":
    main()
