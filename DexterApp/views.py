from django.shortcuts import render,  redirect
from django.contrib import messages
from django.http import HttpResponse 
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate,login 
import requests
from bs4 import BeautifulSoup
from django.core.mail import send_mail
from django.conf import settings as conf_settings
from django.conf import settings
import random
from datetime import datetime, timedelta, timezone
from django.http import JsonResponse
import json
from django.contrib.auth.decorators import login_required




@login_required
def websiteScanner(request):
    return render(request, 'websiteScanner.html')
    
def textScanner(request):
    return render(request, 'textScanner.html')


def sidebar(request):
    return render(request, 'sidebar.html')

    
def text(request):
    return render(request, 'text.html')

@login_required
def webResult(request):
    # Get the URL from the GET parameters
    url = request.GET.get('website_url', '')  # Updated to match the input name

    if not url:
        return render(request, 'webResult.html', {'text': 'No URL provided.', 'url': ''})

    try:
        # Fetch the website content
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful

        # Parse the HTML and extract text
        soup = BeautifulSoup(response.text, 'html.parser')

        #if only want to extract p:
        #text = ' '.join([element.get_text() for element in soup.find_all('p')])

        
        text = ' '.join([element.get_text() for element in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]) or 'No content found.'

    except Exception as e:
        # Handle errors like invalid URL or connection issues
        text = f"An error occurred: {e}"

    # Render the results page with the extracted text
    return render(request, 'webResult.html', {'text': text, 'url': url})
    

def text_result(request):
    if request.method == 'POST':
        input_text = request.POST.get('input_text', '')  # Get text from form
        request.session['scanned_text'] = input_text  # Store in session
    else:
        input_text = request.session.get('scanned_text', '')

    # Sample AI analysis (replace with actual AI model results)
    ai_percentage = 62  # Example percentage
    human_percentage = 38

    context = {
        'input_text': input_text,
        'ai_percentage': ai_percentage,
        'human_percentage': human_percentage
    }
    
    return render(request, 'textResult.html', context)

def homepage(request):
    return render(request, 'homepage.html')

def about_us(request):
    return render(request, 'about_us.html')

def contact_us(request):
    return render(request, 'contact_us.html')

def SignUp(request):

    #check id the request methof is POST
    if request.method == 'POST':
        #extract form data
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST["first_name"]
        password = request.POST['password']
        confirmPass = request.POST['confirmPass']

        #check if username already exist
        if User.objects.filter(username=username):
            messages.error(request,"Username already exist", extra_tags='username')
            return render(request, 'SignUp.html')
    
        #check if email already exist
        if User.objects.filter(email=email):
            messages.error(request,"Email already exist", extra_tags='email')
            return render(request, 'SignUp.html')

        #check if username is too long
        if len(username) > 10:
             messages.error(request,"Username is too long", extra_tags='username')
             return render(request, 'SignUp.html')
        
        #check if username alphanumeric
        if not username.isalnum():
             messages.error(request,"Username is too long", extra_tags='username')
             return render(request, 'SignUp.html')
        
        #check if passwords match
        if password!= confirmPass:
            messages.error(request, "Passwords don't match", extra_tags='confirmPass')
            return render(request, 'SignUp.html')
        
        #Generate 5 digit OTP
        otp = str(random.randint(10000,99999))
        otp_expiry = datetime.now() + timedelta(minutes=5)

        request.session['otp'] = otp
        request.session['otp_expiry'] = otp_expiry.strftime('%Y-%m-%d %H:%M:%S')
        request.session['username'] = username
        request.session['email'] = email
        request.session['first_name'] = first_name
        request.session['password'] = password

        #Send OTP email 
        subject = "Your OTP for Dexter"
        message = "Hello " + first_name + "\n\nTo continue setting up your Dexter account, please verify your account with the code below:\n\n"+ otp +"\n\nThis code will expire in 5 minutes.\nPlease do not disclose this code to others.\nIf you did not make this request, please disregard this email."
        from_email = conf_settings.EMAIL_HOST_USER
        to_list = [email]
        send_mail(subject, message, from_email, to_list, fail_silently=False)

        return redirect('Verify_OTP')
    
    #render SignUp page if request method is not POST
    return render(request, 'SignUp.html')

def Verify_OTP(request):
    
     #check id the request methof is POST
    if request.method == 'POST':

        user_otp = (
            request.POST.get('otp1', '') +
            request.POST.get('otp2', '') +
            request.POST.get('otp3', '') +
            request.POST.get('otp4', '') +
            request.POST.get('otp5', '')
        )

        stored_otp = request.session['otp'] #otp sent to the user and stored in the sesion
        otp_expiry = datetime.strptime(request.session['otp_expiry'], '%Y-%m-%d %H:%M:%S')

        #check if the OTP expired
        if datetime.now() > otp_expiry:
            messages.error(request, "OTP expired, Please try again")
            return render(request, 'Verify_OTP.html')
        
        #check if the entered otp and stored otp doesn't match
        if user_otp == stored_otp:

            #OTP is valid, retrieve user data
            username = request.session['username'] 
            email = request.session['email'] 
            first_name = request.session['first_name']
            password = request.session['password']
            
            #create new user
            Person = User.objects.create_user(username, email, password)
            Person.first_name = first_name
            Person.is_active = True
            Person.save()

            #Clear session data
            request.session.flush()

            return redirect('welcome')
        
        else:
            messages.error(request, "Invalid OTP, Please try again")
            return render(request, 'Verify_OTP.html')
        
    return render (request, 'Verify_OTP.html')

def Resend_OTP(request):

    #Check if the session data exists
    if not request.session['email']:
        messages.error(request, "Session expired, Please signup again")
        return redirect('SignUp')
    
    #Generate a new OTP
    new_otp = str(random.randint(10000,99999))

    email = request.session['email']
    #Update the OTP and expiry time
    request.session['otp'] = new_otp
    
    #send an email with the new OTP
    subject = "Your OTP for Dexter"
    message = "Hello " + request.session['first_name'] + "\n\nTo continue setting up your Dexter account, please verify your account with the code below:\n\n"+ new_otp +"\n\nThis code will expire in 5 minutes.\nPlease do not disclose this code to others.\nIf you did not make this request, please disregard this email." 
    from_email = conf_settings.EMAIL_HOST_USER
    to_list = [email]
    send_mail(subject, message, from_email, to_list, fail_silently=False) 

    messages.success(request, "A new OTP has been sent to your email")
    return redirect('Verify_OTP')

def Login(request):

      #check id the request methof is POST
    if request.method == 'POST':
        #extract email and password from POST request
        username = request.POST['username']
        password = request.POST['password']
        #authenticate user credentials
        person = authenticate(username=username, password=password)

        if person is not None:
            #if person is a regular user, login and redirect to home page
            if not person.is_staff:
                login(request, person)
                return redirect('home')
            
        #if authentication fails, display error message
        else:
            messages.error(request, 'Invalid password or username')

    #render Login page if request method is not POST
    return render(request, 'Login.html')

def ForgotPassword(request):
    return render(request, 'ForgotPassword.html')

def emailsent(request):
    return render(request, 'emailsent.html')

def ResetPassword(request):
    return render(request, 'ResetPassword.html')

def welcome(request):
    return render(request, 'welcome.html')

def AccDel(request):
    return render(request, 'AccDel.html')

def PassUpd(request):
    return render(request, 'PassUpd.html')

def account_settings(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'delete_account':
            # Handle account deletion
            request.user.delete()
            messages.success(request, "Account deleted successfully!")
            return redirect('AccDel')
    return render(request, 'setings.html')


@login_required
def extension_view(request):
    result = None

    if request.method == 'POST':
        text = request.POST.get('text', '')

        if text:
            # Placeholder logic (AI detection will be added later)
            result = {
                'text': text,
                'ai_generated': None,
                'confidence': None
            }

    return render(request, 'extension/extension_page.html', {'result': result})