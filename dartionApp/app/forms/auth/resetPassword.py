from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from random import randint
from app.models import UserAuthKey

class ForgotPasswordForm(forms.Form):
	username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-field form-element',
                                                                               'placeholder': ' ',
                                                                               'id': 'username',
                                                                               'name': 'j_username',
                                                                               'type': 'text',
                                                                               'autocorrect': 'off',
                                                                               'autocapitalize': 'none',
                                                                               'value': ''
                                                                               }
                                                                        )
                               )

	def clean(self, *args, **kwargs):
		username = self.cleaned_data.get('username')
		if username == "":
			raise forms.ValidationError("Please enter your username or email to reset your password.")
		return self.cleaned_data

class ResetPasswordForm(forms.Form):
	password1 = forms.CharField()

	password2 = forms.CharField()

	def clean(self, *args, **kwargs):
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')
		if len(password1) < 8 :
			raise forms.ValidationError("Password must be atleast of 8 characters long."
										" It can include alpha-numeric-special characters")
		if password1 != password2:
			raise forms.ValidationError("Password 1 and Password 2 must match")
		return self.cleaned_data
