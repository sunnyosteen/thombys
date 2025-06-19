from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import UserRegistrationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .forms import CustomLoginForm
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.db import IntegrityError
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.contrib.auth import logout as django_logout
from django.shortcuts import redirect
from .forms import UserRegistrationForm
import logging
from django.contrib.auth import authenticate, login as django_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth.decorators import login_required





def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.username = form.cleaned_data['username']  # Use chosen username
                user.set_password(form.cleaned_data['password'])
                user.is_active = False
                user.save()

                # Create or get user profile
                user_profile = user.profile
                user_profile.first_name = form.cleaned_data.get('first_name', '')
                user_profile.last_name = form.cleaned_data.get('last_name', '')
                user_profile.save()

                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))

                current_site = get_current_site(request)
                confirm_url = reverse('userprofile:confirm_email', kwargs={'uidb64': uid, 'token': token})
                full_link = f"http://{current_site.domain}{confirm_url}"

                context = {
                    'user': user,
                    'confirm_link': full_link,
                }

                subject = 'Complete Your Registration'
                from_email = 'noreply@yourdomain.com'
                to_email = user.email

                html_message = render_to_string('userprofile/registration_mail.html', context)
                text_message = render_to_string('userprofile/registration_mail.txt', context)

                email = EmailMultiAlternatives(subject, text_message, from_email, [to_email])
                email.attach_alternative(html_message, "text/html")
                email.send()

                messages.info(request, 'Check your email to confirm your account.')
                return redirect('userprofile:login')  # <-- this prevents re-submission on refresh

            except IntegrityError:
                messages.error(request, 'An account with this email already exists.')
            except Exception as e:
                messages.error(request, 'Something went wrong. Please try again later.')
                print(f"Error during registration: {e}")
    else:
        form = UserRegistrationForm()

    return render(request, 'userprofile/register.html', {'form': form})






def confirm_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.profile.email_verified = True
        user.profile.save()
        return render(request, 'userprofile/email_confirmed.html')
    else:
        return render(request, 'userprofile/email_confirmation_failed.html')






logger = logging.getLogger(__name__)

def login(request):
    # Redirect logged-in users away from login page to avoid forbidden errors or re-login attempts
    if request.user.is_authenticated:
        return redirect('userprofile:dashboard')  # Redirect to dashboard if already logged in

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            input_username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = None

            try:
                # First try to find a User with the username provided
                user = User.objects.get(username=input_username)
            except User.DoesNotExist:
                try:
                    # If no User, try UserProfile with username
                    profile = UserProfile.objects.get(username=input_username)
                    user = profile.user
                except UserProfile.DoesNotExist:
                    user = None

            if user:
                user_auth = authenticate(username=user.username, password=password)
                if user_auth is not None:
                    django_login(request, user_auth)
                    messages.success(request, f"Welcome back, {user_auth.username}!")
                    logger.info(f"User '{user_auth.username}' logged in successfully.")
                    return redirect('userprofile:dashboard')
                else:
                    messages.error(request, "Incorrect password. Please try again.")
                    logger.error(f"Failed login attempt for username: {input_username}. Incorrect password.")
            else:
                messages.error(request, "This username does not exist. Please check your username.")
                logger.error(f"Failed login attempt for username: {input_username}. Username not found.")
        else:
            logger.error(f"Form errors: {form.errors}")
            messages.error(request, "Please correct the errors below.")
    else:
        form = AuthenticationForm()

    return render(request, 'userprofile/login.html', {'form': form})





def logout_view(request):
    django_logout(request)
    return redirect('userprofile:login')  # Redirect to your login page after logout







@login_required
def dashboard_view(request):
    # You can pass any context data you want here
    context = {
        'user': request.user,
        'message': 'Welcome to your dashboard!',
    }
    return render(request, 'userprofile/dashboard.html', context)

