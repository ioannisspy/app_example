import pandas as pd
import requests
from sec_api import QueryApi, ExtractorApi
from anthropic import Anthropic
import time
import re
from typing import List, Dict, Tuple

class ChinaSupplyChainAnalyzer:
    def __init__(self):
        self.sec_api_key = None
        self.anthropic_api_key = None
        self.anthropic_model = None
        self.query_api = None
        self.extractor_api = None
        self.anthropic_client = None
        
        # Common 10-K sections mapping
        self.tenk_sections = {
            1: "Risk Factors",
            2: "Business",
            3: "Legal Proceedings", 
            4: "Management's Discussion and Analysis",
            5: "Financial Statements and Supplementary Data",
            6: "Controls and Procedures",
            7: "Other Information",
            8: "Directors, Executive Officers and Corporate Governance",
            9: "Executive Compensation",
            10: "Security Ownership",
            11: "Certain Relationships and Related Transactions",
            12: "Principal Accountant Fees and Services",
            13: "Exhibits and Financial Statement Schedules",
            14: "Properties",
            15: "Selected Financial Data",
            16: "Market for Common Equity",
            17: "Unresolved Staff Comments"
        }
        
        # Claude model options
        self.claude_models = {
            1: "claude-3-5-sonnet-20241022",
            2: "claude-3-5-haiku-20241022", 
            3: "claude-3-opus-20240229",
            4: "claude-3-sonnet-20240229",
            5: "claude-3-haiku-20240307"
        }

    def get_user_inputs(self) -> Tuple[List[str], List[int]]:
        """Step 1: Get firm tickers and years from user"""
        print("=== STEP 1: Company Tickers and Years ===")
        
        # Get tickers
        tickers_input = input("Enter company tickers separated by commas (e.g., AAPL,MSFT,GOOGL): ").strip()
        tickers = [ticker.strip().upper() for ticker in tickers_input.split(",")]
        
        # Get years
        years_input = input("Enter years separated by commas (e.g., 2021,2022,2023): ").strip()
        years = [int(year.strip()) for year in years_input.split(",")]
        
        print(f"Selected tickers: {tickers}")
        print(f"Selected years: {years}")
        
        return tickers, years

    def setup_apis(self):
        """Step 2: Get API keys and model selection"""
        print("\n=== STEP 2: API Configuration ===")
        
        # Get SEC API key
        self.sec_api_key = input("Enter your SEC API key: ").strip()
        
        # Get Anthropic API key
        self.anthropic_api_key = input("Enter your Anthropic API key: ").strip()
        
        # Model selection
        print("\nAvailable Claude models:")
        for key, model in self.claude_models.items():
            print(f"{key}. {model}")
        
        model_choice = int(input("Select model (enter number): "))
        self.anthropic_model = self.claude_models[model_choice]
        
        # Initialize API clients
        self.query_api = QueryApi(api_key=self.sec_api_key)
        self.extractor_api = ExtractorApi(api_key=self.sec_api_key)
        self.anthropic_client = Anthropic(api_key=self.anthropic_api_key)
        
        print(f"Selected model: {self.anthropic_model}")

    def select_10k_section(self) -> str:
        """Step 3: Select which 10-K section to analyze"""
        print("\n=== STEP 3: 10-K Section Selection ===")
        print("Available 10-K sections:")
        
        for key, section in self.tenk_sections.items():
            print(f"{key:2d}. {section}")
        
        section_choice = int(input("Select section to analyze (enter number): "))
        selected_section = self.tenk_sections[section_choice]
        
        print(f"Selected section: {selected_section}")
        return selected_section

    def get_10k_filing_url(self, ticker: str, year: int) -> str:
        """Get the URL of the 10-K filing for a specific ticker and year"""
        try:
            query = {
                "query": f"ticker:{ticker} AND formType:\"10-K\" AND filedAt:[{year}-01-01 TO {year}-12-31]",
                "from": "0",
                "size": "1",
                "sort": [{"filedAt": {"order": "desc"}}]
            }
            
            response = self.query_api.get_filings(query)
            
            if response['filings']:
                return response['filings'][0]['linkToFilingDetails']
            else:
                print(f"No 10-K filing found for {ticker} in {year}")
                return None
                
        except Exception as e:
            print(f"Error getting filing URL for {ticker} ({year}): {e}")
            return None

    def extract_section_content(self, filing_url: str, section_name: str) -> str:
        """Extract specific section content from 10-K filing"""
        try:
            # Map section names to extractor API section identifiers
            section_mapping = {
                "Risk Factors": "1A",
                "Business": "1", 
                "Legal Proceedings": "3",
                "Management's Discussion and Analysis": "7",
                "Financial Statements and Supplementary Data": "8",
                "Controls and Procedures": "9A",
                "Properties": "2",
                "Selected Financial Data": "6",
                "Market for Common Equity": "5"
            }
            
            section_id = section_mapping.get(section_name, "1A")  # Default to Risk Factors
            
            section_text = self.extractor_api.get_section(filing_url, section_id, "text")
            
            # Clean up the text
            if section_text:
                # Remove excessive whitespace and clean up
                section_text = re.sub(r'\s+', ' ', section_text).strip()
                # Limit length to avoid token limits (keep first 15000 characters)
                if len(section_text) > 15000:
                    section_text = section_text[:15000] + "..."
                
            return section_text
            
        except Exception as e:
            print(f"Error extracting section content: {e}")
            return None

    def analyze_china_exposure(self, company_name: str, section_content: str) -> int:
        """Use Claude API to analyze China supply chain exposure"""
        try:
            prompt = f"""
            Analyze the following 10-K section content for {company_name} and determine their exposure to China through supply chain relationships (both as suppliers to China and customers in China).

            Please provide a score from 1-5 where:
            1 = Very low/no China supply chain exposure
            2 = Low China supply chain exposure  
            3 = Moderate China supply chain exposure
            4 = High China supply chain exposure
            5 = Very high China supply chain exposure

            Consider factors like:
            - Direct mentions of China operations, suppliers, or customers
            - Manufacturing or sourcing in China
            - Sales revenue from China
            - Supply chain dependencies on Chinese companies
            - Risks related to China trade relationships
            - Joint ventures or partnerships in China

            Section content:
            {section_content}

            Respond with only the numerical score (1-5) followed by a brief 2-sentence explanation.
            """

            message = self.anthropic_client.messages.create(
                model=self.anthropic_model,
                max_tokens=150,
                messages=[{"role": "user", "content": prompt}]
            )
            
            response_text = message.content[0].text.strip()
            
            # Extract the numerical score
            score_match = re.search(r'^(\d)', response_text)
            if score_match:
                return int(score_match.group(1))
            else:
                print(f"Could not parse score from response: {response_text}")
                return 3  # Default to moderate if parsing fails
                
        except Exception as e:
            print(f"Error analyzing China exposure: {e}")
            return 3  # Default to moderate on error

    def run_analysis(self):
        """Main function to run the complete analysis"""
        print("China Supply Chain Exposure Analyzer")
        print("=" * 50)
        
        # Step 1: Get inputs
        tickers, years = self.get_user_inputs()
        
        # Step 2: Setup APIs
        self.setup_apis()
        
        # Step 3: Select section
        section_name = self.select_10k_section()
        
        # Step 4: Process each company/year combination
        print(f"\n=== STEP 4: Analysis Results ===")
        print("Processing filings and analyzing China exposure...")
        
        results = []
        total_combinations = len(tickers) * len(years)
        current_combination = 0
        
        for ticker in tickers:
            for year in years:
                current_combination += 1
                print(f"\nProcessing {ticker} ({year}) - {current_combination}/{total_combinations}")
                
                # Get filing URL
                filing_url = self.get_10k_filing_url(ticker, year)
                if not filing_url:
                    results.append({
                        'Company': ticker,
                        'Year': year,
                        'Score': 'N/A - No filing found'
                    })
                    continue
                
                # Extract section content
                section_content = self.extract_section_content(filing_url, section_name)
                if not section_content:
                    results.append({
                        'Company': ticker,
                        'Year': year,
                        'Score': 'N/A - Section not found'
                    })
                    continue
                
                # Analyze China exposure
                score = self.analyze_china_exposure(ticker, section_content)
                
                results.append({
                    'Company': ticker,
                    'Year': year,
                    'Score': score
                })
                
                print(f"Result: {ticker} ({year}) - Score: {score}")
                
                # Add delay to respect API limits
                time.sleep(2)
        
        # Display results table
        print(f"\n=== FINAL RESULTS ===")
        print(f"Analysis of {section_name} section for China supply chain exposure")
        print("Score: 1=Very Low, 2=Low, 3=Moderate, 4=High, 5=Very High")
        print("-" * 50)
        
        df = pd.DataFrame(results)
        print(df.to_string(index=False))
        
        return df

# Example usage
if __name__ == "__main__":
    analyzer = ChinaSupplyChainAnalyzer()
    results = analyzer.run_analysis()
