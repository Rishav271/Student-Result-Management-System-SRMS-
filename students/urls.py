# students/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('add/', views.add_student, name='add_student'),
    path('<int:pk>/', views.student_detail, name='student_detail'),
]
