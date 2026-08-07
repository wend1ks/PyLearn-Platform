from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .decorators import admin_required
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from .models import CustomUser
from courses.models import Course, Module, Lesson


def landing(request):
    course_count = Course.objects.count()
    module_count = Module.objects.count()
    lesson_count = Lesson.objects.count()
    project_count = max(4, course_count)

    return render(request, 'landing.html', {
        'course_count': course_count,
        'module_count': module_count,
        'lesson_count': lesson_count,
        'project_count': project_count,
    })

def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("students:course_list")
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

from django.contrib import messages
from django.contrib.auth import authenticate, login

def signin(request):
    if request.method == "POST":
        form = SignInForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(
                request,
                username=username,
                password=password,
            )

            if user is not None:
                login(request, user)
                return redirect("students:course_list")

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


@login_required
def profile_edit(request):
    form = ProfileForm(request.POST or None, request.FILES or None, instance=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("users:profile")
    return render(request, "profile_edit.html", {"form": form})
    








