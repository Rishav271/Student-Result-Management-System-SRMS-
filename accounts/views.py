from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from students.models import Student
from .forms import StudentRegisterForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from students.models import Student
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from results.models import Result
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def home(request):
    return render(request, "home.html")


def register(request):
    if request.method == "POST":
        form = StudentRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('login') 
        else:
            print(form.errors) 
    else:
        form = StudentRegisterForm()
    return render(request, "accounts/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome {username}!")
                return redirect("dashboard")
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, "accounts/login.html", {"form": form})



def logout_view(request):
    logout(request)
    messages.info(request, "You have logged out.")
    return redirect("home")


@login_required
def dashboard(request):
    return render(request, "dashboard.html")

@login_required
def dashboard(request):
    return render(request, "accounts/dashboard.html")

def dashboard(request):
    try:
        student = Student.objects.get(user=request.user)  
        results = Result.objects.filter(student=student)
    except Student.DoesNotExist:
        student = None
        results = []

    return render(request, 'accounts/dashboard.html', {
        'student': student,
        'results': results
    })

@staff_member_required
def all_students(request):
    students = Student.objects.all()
    return render(request, "accounts/all_students.html", {"students": students})
