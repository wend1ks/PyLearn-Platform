from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth import login,authenticate, logout
from django.contrib import messages
from .decorators import admin_required
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from .models import CustomUser

def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("users:signin")
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def signin(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)

        if form.is_valid(): 
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                return redirect('students:course_list')
            else:
                messages.error(request, "Неверный логин или пароль.")
    else:
        form = SignInForm()

    return render(request, "signin.html", {"form": form})

def signout(request):
    logout(request)
    return redirect('users:signin')


class ProfileView(LoginRequiredMixin, DetailView):
    template_name = "profile.html"
    context_object_name = "user_obj"
    def get_object(self):
        return self.request.user
    





