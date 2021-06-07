from django.shortcuts import render

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from app.models import UserAuthKey
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from  baseApp.settings import ALLOWED_HOSTS
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
# Create your views here.
from .models import *
from app.forms.auth.createUser import CreateUserForm
from app.forms.auth.resetPassword  import ForgotPasswordForm, ResetPasswordForm
import secrets


def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = User.objects.get(username=form.data['username'])

                secret = secrets.token_hex(16)
                authToken = UserAuthKey.objects.create(user=user, auth_key=secret)

                subject = 'Your account was created successfully!'
                message = ''
                if settings.ENV == 'development':
                    secret = 'http://'+settings.ALLOWED_HOSTS[0] + ':8000/activate/' + secret
                    domain_name = 'http://'+settings.ALLOWED_HOSTS[0]+':8000'
                if settings.ENV == 'production':
                    secret = 'http://'+settings.ALLOWED_HOSTS[0] + '/activate/' + secret
                    domain_name = 'http://' + settings.ALLOWED_HOSTS[0]
                html_message = render_to_string('auth/emails/signup_email.html',{
                    'url': "{}".format(ALLOWED_HOSTS[0]),
                    'secret': secret,
                    'user':user,
                    'domain_name': domain_name
                })

                email_from = settings.EMAIL_SENDER
                # recipients is a list
                recipient_list = [user.email]
                send_mail(subject, message, from_email=email_from, recipient_list=recipient_list,
                          html_message=html_message)


                messages.success(request, 'Account was created for ' + user.first_name + ' . An email has been sent to the registered email. Please check your inbox')

                return redirect('login')

        context = {'form': form}
        return render(request, 'auth/signup.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            returnWithMessage = False

            try:
                user = User.objects.get(email=username).username
            except Exception as ex:
                user = None
            try:
                user = User.objects.get(username=username).username
            except Exception as ex:
                user = None

            if user is not None:
                username = authenticate(request, username=user, password=password)
                if returnWithMessage is False:
                    if username is not None:
                        login(request, username)
                        return redirect('home')
                    else:
                        messages.error(request, 'Invalid credentials')
            else:
                messages.error(request, 'Invalid credentials')

        context = {'form': request.POST}
        return render(request, 'auth/login.html', context)

def activateUser(request, id):
    try:
        auth_key = UserAuthKey.objects.get(auth_key=id)
        user = User.objects.get(username=auth_key.user.username)
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated! Please login to continue.')
        login(request, user,backend='django.contrib.auth.backends.ModelBackend')
        return redirect('home')
    except Exception as ex:
        print("Auth ID does not exist.")
        messages.error(request, 'Unique token for this new account does not exist. Please contact Administrator.')
        return redirect('login')


def logoutUser(request):
    logout(request)
    return redirect('login')


def forgotPassword(request):
    form = ForgotPasswordForm()
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(username=form.data['username'])
            except Exception as ex:
                user = None
                print("Username does not exist")

            if user is None:
                try:
                    user = User.objects.get(email=form.data['username'])
                except Exception as ex:
                    print("Username does not exist")
                    user = None
            if user is not None:
                secret = secrets.token_hex(16)
                authToken = UserAuthKey.objects.create(user=user, reset_password_key=secret)

                subject = 'Reset your password!'
                message = ''
                if settings.ENV == 'development':
                    secret = 'http://' + settings.ALLOWED_HOSTS[0] + ':8000/resetPassword/' + secret
                    domain_name = 'http://' + settings.ALLOWED_HOSTS[0] + ':8000'
                if settings.ENV == 'production':
                    secret = 'http://' + settings.ALLOWED_HOSTS[0] + '/resetPassword/' + secret
                    domain_name = 'http://' + settings.ALLOWED_HOSTS[0]
                html_message = render_to_string('auth/emails/resetPassword_email.html', {
                    'url': "{}".format(ALLOWED_HOSTS[0]),
                    'secret': secret,
                    'user': user,
                    'domain_name': domain_name
                })

                email_from = settings.EMAIL_SENDER
                # recipients is a list
                recipient_list = [user.email]
                send_mail(subject, message, from_email=email_from, recipient_list=recipient_list,
                          html_message=html_message)

            print("Validation passed")
        else:
            print("Username does not exist")
        messages.success(request,
            "If the entered email is valid, you will receive and email with the link to reset password shortly.")
    context = {'form': form}
    return render(request, 'auth/forgotPassword.html', context)

def resetPassword(request, id):
    try:
        user = UserAuthKey.objects.get(reset_password_key=id).user
    except Exception as ex:
        messages.error(request,
                         "Unique reset password key is invalid!")
        return redirect('login')

    form = ResetPasswordForm()
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            messages.success(request,
                             "Success! Your password is updated now.")
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')

    context = {'form': form}
    return render(request, 'auth/resetPassword.html', context)

@login_required(login_url='login')
def home(request):
    context = {}
    return render(request, 'home.html', context)

@login_required(login_url='login')
def about(request):
    context = {}
    return render(request, 'menu/about.html', context)

def products(request):
    context = {}
    return render(request, 'menu/products.html', context)

def contact(request):
    context = {}
    return render(request, 'menu/contact.html', context)
