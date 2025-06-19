from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import RegexValidator
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth import authenticate


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput, 
        label="Password", 
        required=True  # Make password required
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput, 
        label="Confirm Password", 
        required=True  # Make password confirmation required
    )
    
    # Add username field with validation to allow only letters and numbers
    username = forms.CharField(
        max_length=30,
        validators=[RegexValidator(regex=r'^[a-zA-Z0-9]+$', message="Username can only contain letters and numbers.")],
        label="Username",
        required=True  # Make username required
    )

    class Meta:
        model = User
        fields = ['username', 'email']  # Add username along with email for registration

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise ValidationError("Passwords do not match.")
        return password_confirm

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email address is already registered.")
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username







class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username",
        max_length=150,
        widget=forms.TextInput(attrs={
            'autofocus': True
        })
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput()
    )