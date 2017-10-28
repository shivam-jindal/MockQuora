from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import *
from django.utils import timezone
from django.contrib.auth.models import User
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'MockQuora/index.html', {})

def user_login(request):
    error_msg = ""
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/feed/')
                else:
                    return HttpResponse("your account is disabled.")

            else:
                error_msg = "Invalid Login Details."
                print error_msg

        else:
            error_msg = form.errors

    form = LoginForm()
    context = {
        'errormsg': error_msg,
        'form': form
    }
    return render(request, 'quora/login.html', context)


def register(request):
    error_msg = ""
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.add(*form.cleaned_data["interests"])
            user_profile.save()
            return HttpResponseRedirect('/feed/')
        else:
            error_msg = form.errors

    form = RegisterForm()
    context = {
        'errormsg': error_msg,
        'form': form
    }

    return render(request, 'quora/register.html', context)


@login_required
def feed(request):
    pass
