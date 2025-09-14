from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200, default='Unknown Student')
    roll_no = models.CharField(max_length=50, unique=True)
    enrollment_no = models.CharField(max_length=20, default='ENR001', unique=True)
    course = models.CharField(max_length=100)
    duration = models.PositiveSmallIntegerField(default=4)
    semester = models.PositiveSmallIntegerField(default=1)
    image = models.ImageField(upload_to='student_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.full_name} ({self.roll_no})"
