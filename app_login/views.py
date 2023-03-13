from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .models import Profile
from .forms import ProfileForm, SignUpforms
from django.contrib import messages


def signup(request):
    form = SignUpforms()
    if request.method == 'POST':
        form = SignUpforms(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully.")
            return HttpResponseRedirect(reverse('app_login:login'))
        else:
            messages.warning(request, "Something went wrong")
    return render(request,'app_login/signup.html', context={'form':form})

def login_user(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username, password = password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("app_shop:home"))
        messages.warning(request, "Wrong Email or Password")
    return render(request, 'app_login/login.html', context={'form': form})

@login_required
def logout_user(request):
    logout(request)
    messages.warning(request, "you are logged out")
    return HttpResponseRedirect(reverse("app_shop:home"))

@login_required
def user_profile(request):
    profile = Profile.objects.get(user = request.user)

    form = ProfileForm(request.POST, instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST,instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Changes Saved!")
            form = ProfileForm(instance=profile)

    return render(request, 'app_login/change_profile.html', context={'form':form})
