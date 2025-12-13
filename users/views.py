from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from datetime import datetime
import re # Import the Regular Expressions module

# Models
from users.models import AccountRequest

db_name = 'appdb' 

# We add a validation function that returns the first error message found
def validate_request_data(FULLNAME, PASSWORD, REP_PASSWORD):
    errors = []

    # Full Name Validation (FULLNAME)
    # Must be more than 10 characters
    if len(FULLNAME) <= 10:
        errors.append('The Full Name must be longer than 10 characters.')
    
    # Must contain only letters (A-Z) and spaces
    # r'^[A-Za-z\s]+$' allows only letters (upper/lower case) and spaces.
    if not re.match(r'^[A-Za-z\s]+$', FULLNAME):
        errors.append('The Full Name must contain only letters and spaces.')

    # Password Validation
    # Coincidence Validation
    if PASSWORD != REP_PASSWORD:
        errors.append('Passwords do not match. Please repeat the password correctly.')
    
    # Password Requirements Validation (Minimum 8 characters, 1 special, 1 upper, 1 lower, 1 number)
    if len(PASSWORD) < 8:
        errors.append('The password must be at least 8 characters long.')

    # Checks if the password meets all requirements using lookaheads (Regular Expressions)
    password_regex = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    
    if not re.match(password_regex, PASSWORD):
        errors.append('The password must be at least 8 characters long, including at least 1 uppercase letter, 1 lowercase letter, 1 number, and 1 special character (@$!%*?&).')
    
    return errors


def login(request):
    return render(request, 'login.html')

def request(request):
    if request.method == "GET":
        # Checks for success messages (for post-submission redirection)
        success_message = request.session.pop('success_message', None)
        context = {'success': success_message} if success_message else {}
        return render(request, 'request.html', context)
    
    else: # request.method == "POST"
        # If it's POST, process the data
        FULLNAME = request.POST.get('req_fullname').strip()
        EMAIL = request.POST.get('req_email').strip()
        PASSWORD = request.POST.get('req_password')
        REP_PASSWORD = request.POST.get('rep_password') # Get the repeated password
        COMPANY_NAME = request.POST.get('req_client_name')

        # 1. DATA VALIDATION (New Step)
        validation_errors = validate_request_data(FULLNAME, PASSWORD, REP_PASSWORD)
        
        if validation_errors:
            context = {'error': validation_errors[0]} # Show the first error found
            return render(request, 'request.html', context)
        
        # 2. DATABASE VALIDATION: SELECT (Check if email already exists)
        try:
            # Check if the email already has a pending request
            if AccountRequest.objects.using(db_name).filter(EMAIL=EMAIL).exists():
                context = {'error': 'This email already has a pending or in-review account request. Please wait.'}
                return render(request, 'request.html', context)
        
        except Exception as e:
            # If there is a connection or DB error
            print(f"Error querying the external database ({db_name}): {e}")
            context = {'error': 'An internal error occurred while verifying the account. Please try again later.'}
            return render(request, 'request.html', context)
        
        # 3. RECORD CREATION
        hashed_password = make_password(PASSWORD)
        
        try:
            # Create and Save the new AccountRequest object
            AccountRequest.objects.using(db_name).create(
                FULLNAME=FULLNAME,
                EMAIL=EMAIL,
                PASSWORD=hashed_password,
                COMPANY_NAME=COMPANY_NAME,
                STATUS="Pending" # REQ_DATE is auto_now_add
            )
            
            # 4. Successful Redirection with Message (for green pop-up)
            request.session['success_message'] = "Request successfully placed. Please wait for an email from the support team."
            return redirect('request') # Redirects to the same page (GET) to display the pop-up
            
        except Exception as e:
            # If there is an error trying to save the new record
            print(f"Error saving the account request in the external DB ({db_name}): {e}")
            context = {'error': 'An internal error occurred while registering your request. Please try again later.'}
            return render(request, 'request.html', context)