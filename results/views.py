# results/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Subject, Result
from students.models import Student
from django.shortcuts import render
from .models import Result
from students.models import Student
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import ResultForm


@login_required
def teacher_dashboard(request):
    subjects = Subject.objects.all()
    students = Student.objects.all()
    return render(request, 'teacher_dashboard.html', {'subjects': subjects, 'students': students})

@login_required
def add_subject(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        code = request.POST.get('code')
        semester = request.POST.get('semester', 1)
        Subject.objects.create(name=name, code=code, semester=int(semester))
        return redirect('teacher_dashboard')
    return render(request, 'add_subject.html')

@login_required
def add_result(request):
    if request.method == 'POST':
        student_id = request.POST.get('student')
        subject_id = request.POST.get('subject')
        marks = int(request.POST.get('marks'))
        student = Student.objects.get(pk=student_id)
        subject = Subject.objects.get(pk=subject_id)

        result, created = Result.objects.update_or_create(student=student, subject=subject, defaults={'marks': marks})
        return redirect('teacher_dashboard')
    students = Student.objects.all()
    subjects = Subject.objects.all()
    return render(request, 'add_result.html', {'students': students, 'subjects': subjects})

@login_required
def result_detail(request, student_pk):
    student = get_object_or_404(Student, pk=student_pk)
    results = student.results.select_related('subject').all()
    total = sum([r.marks for r in results]) if results else 0
    avg = total / results.count() if results.count() else 0
    return render(request, 'result_detail.html', {'student': student, 'results': results, 'total': total, 'avg': avg})

@login_required
def add_result(request):
    if not request.user.is_staff: 
        return redirect("my_results")

    if request.method == "POST":
        form = ResultForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("my_results")
    else:
        form = ResultForm()
    
    return render(request, "results/add_result.html", {"form": form})


def my_results(request):
    try:
        student = request.user.student
    except Student.DoesNotExist:
        return render(request, "results/no_student.html")

    semester = request.GET.get("semester")
    results = []
    total_marks = 0
    percentage = 0
    status = "N/A"

    if semester:
        results = Result.objects.filter(student=student, subject__semester=semester)
        if results.exists():
            total_marks = sum(r.marks for r in results)
            max_total = results.count() * 100 
            percentage = (total_marks / max_total) * 100
            status = "Pass" if all(r.marks >= 50 for r in results) else "Fail"

    context = {
        "student": student,
        "results": results,
        "semester": semester,
        "total_marks": total_marks,
        "percentage": percentage,
        "status": status
    }
    return render(request, "results/my_results.html", context)



