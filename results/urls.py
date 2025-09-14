# results/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('subject/add/', views.add_subject, name='add_subject'),
    path('result/add/', views.add_result, name='add_result'),
    path("add/", views.add_result, name="add_result"),
    path('my_results/', views.my_results, name='my_results'),
    path('student/<int:student_pk>/results/', views.result_detail, name='result_detail'),
]
