# app.py
from flask import Flask, render_template, request, jsonify
from datetime import datetime
import re  #regular expressions
import validators

app = Flask(__name__)

def validate_inputs(job_details):
    errors = []
    
    if not job_details.get('title') or len(job_details['title']) < 3:
        errors.append("Job title must be at least 3 characters long")
    
    if not job_details.get('company') or len(job_details['company']) < 2:
        errors.append("Company name must be at least 2 characters long")
    
    if not validators.email(job_details.get('email', '')):
        errors.append("Invalid email format")
    
    try:
        salary = float(job_details.get('salary', '0'))
        if salary <= 0:
            errors.append("Salary must be a positive number")
    except:
        errors.append("Invalid salary format")
    return errors

def check_unrealistic_salary(salary):
    salary_value = float(salary)
    print(salary_value)
    return salary_value > 500000 or salary_value < 10000


def check_generic_description(description):
    return len(description) < 100 or description.count('.') < 2

def check_suspicious_email(email):
    suspicious_domains = [
        'temp', 'disposable', 'free', 'temporary', 
        'mailinator', 'guerrillamail', '10minutemail'
    ]
    return any(domain in email.lower() for domain in suspicious_domains) or not email.endswith(('.com', '.org', '.net', '.edu', '.gov'))

def check_minimal_requirements(requirements):
    return len(requirements) < 50 or requirements.count(',') < 2

def check_vague_benefits(description):
    buzzwords = [
        'unlimited earnings', 'be your own boss', 'quick money', 
        'work from anywhere', 'instant profit', 'no experience needed',
        'weekly bonus', 'immediate start', 'flexible hours',
        'ground floor opportunity', 'million dollar'
    ]
    return any(word in description.lower() for word in buzzwords)

def check_company_legitimacy(company, description):
    red_flags = [
        'startup opportunity',
        'ground floor',
        'no office',
        'work from home only',
        'commission only',
        'investment required',
        'training fee'
    ]
    return any(flag in description.lower() for flag in red_flags)

def check_urgency_pressure(description):
    urgency_phrases = [
        'limited time', 'urgent', 'immediate start', 
        'apply now', 'positions filling fast', 'today only',
        'last chance', 'deadline tomorrow'
    ]
    return any(phrase in description.lower() for phrase in urgency_phrases)

def calculate_job_score(risks):
    base_score = 100
    deductions = {
        'Unrealistic salary range': -30,
        'Overly generic or short job description': -20,
        'Suspicious contact email domain': -25,
        'Minimal or vague job requirements': -15,
        'Contains suspicious buzzwords or promises': -25,
        'High-pressure or urgency tactics': -20,
        'Suspicious company indicators': -25
    }
    
    total_deduction = sum(deductions.get(risk, -10) for risk in risks)
    return max(0, base_score + total_deduction)

def analyze_job(job_details):
    risks = []
    risk_level = 'low'
    
    if check_unrealistic_salary(job_details['salary']):
        risks.append('Unrealistic salary')
    
    if check_generic_description(job_details['description']):
        risks.append('Overly generic or short job description')
    
    if check_suspicious_email(job_details['email']):
        risks.append('Suspicious contact email domain')
    
    if check_minimal_requirements(job_details['requirements']):
        risks.append('Minimal or vague job requirements')
    
    if check_vague_benefits(job_details['description']):
        risks.append('Contains suspicious buzzwords or promises')
    
    if check_urgency_pressure(job_details['description']):
        risks.append('High-pressure or urgency tactics')
    
    if check_company_legitimacy(job_details['company'], job_details['description']):
        risks.append('Suspicious company indicators')
    
    # Calculate risk level based on number of risks
    if len(risks) >= 3:
        risk_level = 'high'
    elif len(risks) >= 1:
        risk_level = 'medium'
    
    legitimacy_score = calculate_job_score(risks)
    
    return {
        'risks': risks,
        'risk_level': risk_level,
        'legitimacy_score': legitimacy_score,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    job_details = request.json
    
    # Validate inputs
    validation_errors = validate_inputs(job_details)
    if validation_errors:
        return jsonify({
            'success': False,
            'errors': validation_errors
        }), 400
    
    analysis = analyze_job(job_details)
    return jsonify({
        'success': True,
        'data': analysis
    })

if __name__ == '__main__':
    app.run(debug=True)