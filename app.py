from flask import Flask, render_template, request, jsonify, session
from datetime import datetime
import validators
import os
import secrets
import autofill

# Import the prediction service
from prediction_service import JobPredictionService

# Importing supabase
from supabase import create_client

SUPABASE_URL = "https://uvjuxbsqjebecfxrvnso.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV2anV4YnNxamViZWNmeHJ2bnNvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDAwODI3NDcsImV4cCI6MjA1NTY1ODc0N30.Vfc5xclfQdhvYGW8nKVCJnVOdzXO5_DFBNd--YqdJkI"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


app = Flask(__name__)

app.secret_key = secrets.token_hex(16)

# Initialize the prediction service
prediction_service = JobPredictionService()


def validate_inputs(job_details):
    errors = []
    
    if job_details.get('title') and len(job_details['title']) < 3:
        errors.append("Job title must be at least 3 characters long")
    
    if job_details.get('company') and len(job_details['company']) < 2:
        errors.append("Company name must be at least 2 characters long")
    
    if job_details.get('email'):
        if not validators.email(job_details.get('email', '')):
            errors.append("Invalid email format")

    if job_details.get('salary'):
        try:
            salary = float(job_details.get('salary', '0'))
            if salary <= 0:
                errors.append("Salary must be a positive number")
        except:
            errors.append("Invalid salary format")
    
    return errors
    


def check_unrealistic_salary(salary):
    salary_value = float(salary)
    return salary_value > 70000 or salary_value < 5000


def check_generic_description(description):
    return len(description) < 100 or description.count('.') < 2


def check_minimal_requirements(requirements):
    return len(requirements) < 50


def check_suspicious_email(email):
    request = supabase.table("fake_job").select("values").eq("name", "suspicious_email").execute().data[0]["values"]
    suspicious_email = [item.lower() for item in request]
    return any(domain in email.lower() for domain in suspicious_email) or not email.endswith(('.com', '.org', '.net', '.edu', '.gov', '.in'))


def check_vague_benefits(description):
    request = supabase.table("fake_job").select("values").eq("name", "buzzwords").execute().data[0]["values"]
    buzzwords = [item.lower() for item in request]
    return any(word in description.lower() for word in buzzwords)


def check_red_flags(description):
    request = supabase.table("fake_job").select("values").eq("name", "red_flags").execute().data[0]["values"]
    red_flags = [item.lower() for item in request]
    return any(flag in description.lower() for flag in red_flags)

def check_payments(description):
    request = supabase.table("fake_job").select("values").eq("name", "payment").execute().data[0]["values"]
    payment = [item.lower() for item in request]
    return any(pay in description.lower() for pay in payment)

def check_urgency_pressure(description):
    request = supabase.table("fake_job").select("values").eq("name", "urgency_phrases").execute().data[0]["values"]
    urgency_phrases = [item.lower() for item in request]
    return any(phrase in description.lower() for phrase in urgency_phrases)

def check_job_title(title):
    request = supabase.table("fake_job").select("values").eq("name", "title").execute().data[0]["values"]
    suspicious_title = [item.lower() for item in request]
    return any(job_title in title.lower() for job_title in suspicious_title)

def check_job_requirements(requirements):
    request = supabase.table("fake_job").select("values").eq("name", "requirements").execute().data[0]["values"]
    job_requirements = [item.lower() for item in request]
    return any(requirement in requirements.lower() for requirement in job_requirements)


def calculate_job_score(risks):
    base_score = 100
    deductions = {
        'Suspicious job title': -25,
        'Suspicious job requirements': -20,
        'Payment fraud indicators': -30,
        'Unrealistic salary range': -40,
        'Overly generic or short job description': -20,
        'Suspicious contact email domain': -25,
        'Minimal or vague job requirements': -15,
        'Contains suspicious buzzwords or promises': -25,
        'High-pressure or urgency tactics': -10,
        'Suspicious company indicators': -25
    }
    
    total_deduction = sum(deductions.get(risk, -10) for risk in risks)
    return max(0, base_score + total_deduction)


def combine_scores(rule_based_score, ml_score, num_risks):
    """
    Combine rule-based score and ML model score based on the number of detected risks
    
    Arguments:
        rule_based_score (float): Score from the rule-based system (0-100)
        ml_score (float): Score from the ML model (0-100)
        num_risks (int): Number of detected risks
    
    Returns:
        float: Combined score (0-100)
    """
    # Ensure scores are within valid range
    rule_based_score = max(0, min(100, float(rule_based_score)))
    ml_score = max(0, min(100, float(ml_score)))
    
    # Dynamic weight adjustment based on number of risks
    if num_risks >= 3:
        rule_weight = 0.6  # Higher weight on rule-based system for many risks
        ml_weight = 0.4
    elif num_risks >= 1:
        rule_weight = 0.4  # Balanced weights for moderate risks
        ml_weight = 0.6
    else:
        rule_weight = 0.3  # Higher weight on ML model for few/no risks
        ml_weight = 0.7
    
    # Calculate weighted average
    combined_score = (rule_based_score * rule_weight) + (ml_score * ml_weight)
    
    # Apply confidence adjustment based on risk count
    confidence_factor = max(0.7, 1 - (num_risks * 0.1))  # Reduces score more with more risks
    combined_score *= confidence_factor
    
    return round(max(0, min(100, combined_score)), 1)


def analyze_job(job_details):
    risks = []
    risk_level = 'low'

    # Rule-based checks
    if job_details.get('title'):
        if check_job_title(job_details['title']):
            risks.append('Suspicious job title')

    if job_details.get('salary'):
        if check_unrealistic_salary(job_details['salary']):
            risks.append('Unrealistic salary range')

    if job_details.get('email'):
        if check_suspicious_email(job_details['email']):
            risks.append('Suspicious contact email domain')
    
    if job_details.get('requirements'):
        if check_job_requirements(job_details['requirements']):
            risks.append('Suspicious job requirements')
        
        if check_minimal_requirements(job_details['requirements']):
            risks.append('Minimal or vague job requirements')

    if job_details.get('description'):
        if check_payments(job_details['description']):
            risks.append('Payment fraud indicators')
        
        if check_generic_description(job_details['description']):
            risks.append('Overly generic or short job description')
        
        if check_vague_benefits(job_details['description']):
            risks.append('Contains suspicious buzzwords or promises')
        
        if check_urgency_pressure(job_details['description']):
            risks.append('High-pressure or urgency tactics')
        
        if check_red_flags(job_details['description']):
            risks.append('Suspicious company indicators')
    
    # ML prediction
    ml_prediction = prediction_service.predict(job_details)
    ml_score = ml_prediction.get('legitimacy_score', 50)  # Default to 50 if prediction fails
    
    # Rule-based score
    rule_based_score = calculate_job_score(risks)
    
    # Combine scores
    combined_score = combine_scores(rule_based_score, ml_score, len(risks))
    
    # Determine risk level based on combined score
    if combined_score < 40:
        risk_level = 'high'
    elif combined_score < 70:
        risk_level = 'medium'
    else:
        risk_level = 'low'
    
    return {
        'risks': risks,
        'risk_level': risk_level,
        'legitimacy_score': combined_score,
        'ml_score': ml_score,
        'rule_based_score': rule_based_score,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/import-job-text', methods=['POST'])
def import_job_text():
    """
    Process the imported job listing text and extract structured information
    using the OpenRouter API.
    """
    data = request.json
    text = data.get('text')
    

    if not text or len(text.strip()) < 50:
        return jsonify({
            'success': False,
            'message': 'Please provide a longer job description for accurate parsing.'
        }), 400
    
    if text[:4]== 'http':
        return jsonify({
            'success': False,
            'message': 'Url Web scraping not allowed. Please paste raw text.'
        }), 400

    # Process the text with OpenRouter API
    result = autofill.parse_job_listing(text)
    
    if result['success']:
        return jsonify({
            'data': result['data'],
            'success': True
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Failed to parse job listing',
            'error': result.get('error', 'Unknown error')
        }), 500


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

# Admin Authentication route
@app.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({
            'success': False,
            'message': 'Username and password are required'
        }), 400
    
    try:
        # Query the admin credentials from Supabase
        response = supabase.table("admin_credentials").select("*").eq("username", username).execute()
        
        if not response.data or len(response.data) == 0:
            return jsonify({
                'success': False,
                'message': 'Invalid username or password'
            }), 401
        
        # Compare the password (in a real app, you'd use password hashing)
        admin_user = response.data[0]
        if admin_user['password'] != password:
            return jsonify({
                'success': False,
                'message': 'Invalid username or password'
            }), 401
        
        # Set a session variable to indicate the user is logged in
        session['admin_logged_in'] = True
        session['admin_username'] = username
        
        return jsonify({
            'success': True,
            'message': 'Login successful'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Login error: {str(e)}'
        }), 500

# Admin logout route
@app.route('/admin/logout', methods=['POST'])
def admin_logout():
    session.pop('admin_logged_in', None)
    session.pop('admin_username', None)
    return jsonify({
        'success': True,
        'message': 'Logout successful'
    })

# Admin routes
@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/admin/get-category', methods=['POST'])
def get_category():
    # Check if user is logged in
    if not session.get('admin_logged_in'):
        return jsonify({
            'success': False,
            'message': 'Authentication required'
        }), 401
    
    data = request.json
    category = data.get('category')
    
    if not category or category not in ['title', 'payment', 'requirements','buzzwords', 'red_flags', 'suspicious_email', 'urgency_phrases']:
        return jsonify({
            'success': False,
            'message': 'Invalid category'
        }), 400
    
    try:
        response = supabase.table("fake_job").select("values").eq("name", category).execute()
        if response.data and len(response.data) > 0:
            return jsonify({
                'success': True,
                'data': response.data[0]["values"]
                
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Category not found'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/admin/update-category', methods=['POST'])
def update_category():
    # Check if user is logged in
    if not session.get('admin_logged_in'):
        return jsonify({
            'success': False,
            'message': 'Authentication required'
        }), 401
    
    data = request.json
    category = data.get('category')
    items = data.get('items', [])
    
    if not category or category not in ['title', 'payment', 'requirements','buzzwords', 'red_flags', 'suspicious_email', 'urgency_phrases']:
        return jsonify({
            'success': False,
            'message': 'Invalid category'
        }), 400
    
    if not items or not isinstance(items, list):
        return jsonify({
            'success': False,
            'message': 'No items provided'
        }), 400
    
    try:
        # Get existing items
        response = supabase.table("fake_job").select("values").eq("name", category).execute()
        if not response.data or len(response.data) == 0:
            return jsonify({
                'success': False,
                'message': 'Category not found'
            }), 404
        
        existing_items = response.data[0]["values"] or []
        
        # Filter out items that already exist
        new_items = [item.lower().strip() for item in items if item.strip()]
        items_to_add = [item for item in new_items if item not in existing_items]
        
        if not items_to_add:
            return jsonify({
                'success': False,
                'message': 'Already exists',
                'added_count': 0
            })
        
        # Update the database
        updated_items = items_to_add + existing_items
        supabase.table("fake_job").update({"values": updated_items}).eq("name", category).execute()
        
        return jsonify({
            'success': True,
            'message': f'Added {len(items_to_add)} items to {category}',
            'added_count': len(items_to_add)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/admin/remove-items', methods=['POST'])
def remove_items():
    # Check if user is logged in
    if not session.get('admin_logged_in'):
        return jsonify({
            'success': False,
            'message': 'Authentication required'
        }), 401
    
    data = request.json
    category = data.get('category')
    items_to_remove = data.get('items', [])
    
    if not category or category not in ['title', 'payment', 'requirements','buzzwords', 'red_flags', 'suspicious_email', 'urgency_phrases']:
        return jsonify({
            'success': False,
            'message': 'Invalid category'
        }), 400
    
    if not items_to_remove or not isinstance(items_to_remove, list):
        return jsonify({
            'success': False,
            'message': 'No items provided for removal'
        }), 400
    
    try:
        # Get existing items
        response = supabase.table("fake_job").select("values").eq("name", category).execute()
        if not response.data or len(response.data) == 0:
            return jsonify({
                'success': False,
                'message': 'Category not found'
            }), 404
        
        existing_items = response.data[0]["values"] or []
        
        # Create a new list excluding the items to remove
        updated_items = [item for item in existing_items if item not in items_to_remove]
        
        # Count how many items were actually removed
        removed_count = len(existing_items) - len(updated_items)
        
        if removed_count == 0:
            return jsonify({
                'success': True,
                'message': 'No items were removed',
                'removed_count': 0
            })
        
        # Update the database with the new list
        supabase.table("fake_job").update({"values": updated_items}).eq("name", category).execute()
        
        return jsonify({
            'success': True,
            'message': f'Removed {removed_count} items from {category}',
            'removed_count': removed_count
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/admin/check-session', methods=['GET'])
def check_session():
    if session.get('admin_logged_in'):
        return jsonify({
            'success': True,
            'isLoggedIn': True,
            'username': session.get('admin_username')
        })
    else:
        return jsonify({
            'success': True,
            'isLoggedIn': False
        })
    
# Add this new route to app.py
@app.route('/check-email', methods=['POST'])
def check_email():
    data = request.json
    email = data.get('email')
    
    if not email or '@' not in email:
        return jsonify({
            'success': False,
            'message': 'Invalid email format'
        }), 400
    
    # Use the existing check_suspicious_email function
    is_suspicious = check_suspicious_email(email)
    
    return jsonify({
        'success': True,
        'suspicious': is_suspicious
    })

if __name__ == '__main__':
    app.run(debug=True)