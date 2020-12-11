import random
from django import forms
from .models import User, WithdrawRequest, Comment
from django.contrib.auth.forms import UserCreationForm

class UserSignUpForm(UserCreationForm):
    refid = forms.CharField(initial='class', max_length=100, widget = forms.HiddenInput())
    # phone_number = forms.CharField(label='Phone number', max_length=100)
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "phone_number", "gender", "country"]

class WithdrawRequestForm(forms.ModelForm):
    class Meta:
        model = WithdrawRequest
        exclude = ["user", "status"]

class ContactForm(forms.Form):
    username = forms.CharField(label='Your Username', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Enter your username'}))
    email = forms.EmailField(label='Your Email', max_length=100, widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}))
    message = forms.CharField(label='Your Message', max_length=1000,
    widget=forms.Textarea(attrs={'placeholder': 'Enter your message'}))

class BlogCommentForm(forms.ModelForm):
    blog_slug = forms.CharField(initial='class', max_length=100, widget = forms.HiddenInput())

    class Meta:
        model = Comment
        fields = ["comment"]

class PasswordResetEmailForm(forms.Form):
    email = forms.EmailField(label='Enter Your Email', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Email'}))

class ResetPasswordForm(forms.Form):
    password1 = forms.CharField(label="Enter new password", widget=forms.PasswordInput())
    password2   = forms.CharField(label="Confirm new password", widget=forms.PasswordInput())
