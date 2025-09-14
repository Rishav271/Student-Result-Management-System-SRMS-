# students/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required
def student_dashboard(request):
    student = None
    if hasattr(request.user, 'student_profile'):
        student = request.user.student_profile
    return render(request, 'student_dashboard.html', {'student': student})

@login_required
def add_student(request):
    if not request.user.is_staff and (not request.user.is_authenticated or request.user.profile.role != 'teacher'):
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password', 'password123')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        roll_no = request.POST.get('roll_no')
        department = request.POST.get('department')
        semester = request.POST.get('semester') or 1

        user = User.objects.create_user(username=username, password=password, email=email,
                                        first_name=first_name, last_name=last_name)
        from accounts.models import Profile
        Profile.objects.create(user=user, role='student')
        Student.objects.create(user=user, roll_no=roll_no, department=department, semester=int(semester))
        return redirect('teacher_dashboard')
    return render(request, 'add_student.html')

@login_required
def student_detail(request, pk):
    s = get_object_or_404(Student, pk=pk)
    return render(request, 'student_detail.html', {'student': s})
