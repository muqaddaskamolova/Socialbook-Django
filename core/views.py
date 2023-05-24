from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth import login, logout
from django.views import View

from core.models import Profile
from django.contrib.auth.decorators import login_required
from .forms import *


# Create your views here.


class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'core/index.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully registered! Sign in!')
            return redirect('login')
        for field in form.errors:
            messages.error(request, form.errors[field].as_text())
            return redirect('register')
    else:
        form = RegistrationForm()

        context = {
            'title': 'REGISTER',
            'form': form
        }
        return render(request, 'core/components/register.html', context)


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password2)
                user.save()

                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('signin')
        else:
            messages.info(request, 'Password is not matching!')
            return redirect('signup')
    else:
        return render(request, 'core/components/signup.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Credentials are invalid')
            return redirect('signin')
    else:
        return render(request, 'core/components/signin.html')


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                login(request, user)
                messages.success(request, 'You have successfully logged in!')
                return redirect('index')
            else:
                messages.error(request, 'You have not logged in,  Or  your login or password is wrong!')
                return redirect('login')
        else:
            messages.error(request, 'You have not logged in,  Or  your login or password is wrong!')
            return redirect('login')
    else:
        form = LoginForm()
        context = {
            'title': 'LOGIN',
            'form': form
        }
        return render(request, 'login.html', context)


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.warning(request, 'You have successfully logged out!')
    return redirect('signin')


def header(request):
    context = {}

    return render(request, 'components/settings.html', context)
