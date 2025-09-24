from django import forms
from django.contrib.auth.models import User
from neo.models import UserProfileInfo
from django.forms import TextInput, EmailInput




class UserForm(forms.ModelForm):

    password = forms.CharField(widget = forms.PasswordInput(attrs={'placeholder' :'Email', 'style': 'width: 300px;','class': 'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'User Name', 'style': 'width: 300px;','class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder' :'Email', 'style': 'width: 300px;','class': 'form-control'}))


    class Meta():
        model = User
        fields = ('username', 'email', 'password')



# class UserProfileInfo(forms.ModelForm):
#     class Meta():
#         model = UserProfileInfo
#         fields = ('portfolio_site','profile_pic')