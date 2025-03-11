# autofill.py
import requests
import json
import os
from dotenv import load_dotenv
import re

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "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")

def parse_job_listing(text):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://localhost:5000"  # Replace with your actual domain
    }
    
    prompt = f"""
    Parse the following job listing url and extract structured information in JSON format.
    Include the following fields if present:
    - title: The job title
    - company: The company name
    - description: Full job description
    - salary: Monthly salary amount (just the number)
    - email: Contact email address
    - requirements: Job requirements or qualifications

    Use proper digit instead of K or M letters.
    If salary is in USD convert it in INR.
    If salary is in  LPA convert it in per month and remove decimals.
    If salary is in per hour convert it in per month considering daily working hour is 6 hr.
    if salary given in range then take average of the range.

    Only respond with valid JSON with these exact fields, nothing else.
    
    Job listing url:
    {text}
    """
    
    payload = {
        "model": "google/gemini-2.0-flash-exp:free",  # You can change to preferred model
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1,
        "max_tokens": 10000
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload
        )
        
        if response.status_code == 200:
            response_data = response.json()
            generated_text = response_data["choices"][0]["message"]["content"]
            
            # Extract JSON from the response
            try:
                # Look for JSON pattern in the response
                json_match = re.search(r'({.*})', generated_text, re.DOTALL)
                if json_match:
                    json_str = json_match.group(1)
                    parsed_data = json.loads(json_str)
                else:
                    parsed_data = json.loads(generated_text)
                
                # Ensure all required fields exist
                required_fields = ['title', 'company', 'description', 'salary', 'email', 'requirements']
                for field in required_fields:
                    if field not in parsed_data:
                        parsed_data[field] = ""
                
                # Ensure salary is numeric
                if parsed_data['salary'] and not isinstance(parsed_data['salary'], (int, float)):
                    # Try to extract numeric value
                    salary_str = parsed_data['salary']
                    numeric_matches = re.findall(r'\d+(?:,\d+)*(?:\.\d+)?', salary_str)
                    if numeric_matches:
                        # Take the first numeric match and remove commas
                        parsed_data['salary'] = float(numeric_matches[0].replace(',', ''))
                    else:
                        parsed_data['salary'] = 0
                        
                return {
                    'success': True,
                    'data': parsed_data
                }
            except json.JSONDecodeError as e:
                return {
                    'success': False,
                    'error': f"Failed to parse API response as JSON: {str(e)}",
                    'raw_response': generated_text
                }
        else:
            return {
                'success': False,
                'error': f"API request failed with status code {response.status_code}",
                'details': response.text
            }
    except Exception as e:
        return {
            'success': False,
            'error': f"Request failed: {str(e)}"
        }

def clean_salary(salary_text):
    """
    Extract numeric salary value from text.
    
    Args:
        salary_text (str): Text containing salary information
        
    Returns:
        float: Extracted salary amount
    """
    if not salary_text:
        return 0
        
    # Remove currency symbols and non-numeric characters
    numeric_pattern = r'[\d,.]+'
    matches = re.findall(numeric_pattern, str(salary_text))
    
    if matches:
        # Take the first match and convert to float
        salary_str = matches[0].replace(',', '')
        try:
            return float(salary_str)
        except ValueError:
            return 0
    return 0