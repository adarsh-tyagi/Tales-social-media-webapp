from django import forms
from django.contrib.auth import models
from .models import Post, Profile, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta():
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta():
        model = User
        fields = ['email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta():
        model = Profile
        fields = ['image', 'status']
    
class UserPostForm(forms.ModelForm):
    class Meta():
        model = Post
        fields = ['message']

class UserCommentForm(forms.ModelForm):
    class Meta():
        model = Comment
        fields = ['comment']