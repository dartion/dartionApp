from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
# from django.forms import ModelForm
# from .models import Order

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

	def clean(self, *args, **kwargs):
		username = self.cleaned_data.get('username')
		first_name=self.cleaned_data.get('first_name')
		last_name = self.cleaned_data.get('last_name')
		username_qs = User.objects.filter(username=username)
		if username_qs.exists():
			raise forms.ValidationError("Username is already registered")
		email = self.cleaned_data.get('email')
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')

		if first_name =="":
			raise forms.ValidationError("Please enter your firstname")
		if last_name =="":
			raise forms.ValidationError("Please enter your lastname")
		if username == "":
			raise forms.ValidationError("Please enter a valid username")
		if email == "":
			raise forms.ValidationError("Please enter a valid email")

		email_qs = User.objects.filter(email=email)
		if email_qs.exists():
			raise forms.ValidationError("This email is already registered")

		return self.cleaned_data