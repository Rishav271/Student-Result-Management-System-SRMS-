# results/models.py
from django.db import models
from students.models import Student

class Subject(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True)
    semester = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return f"{self.name} ({self.code})"

class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='results')
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    marks = models.PositiveSmallIntegerField()
    total_marks = models.PositiveSmallIntegerField(default=100)

    class Meta:
        unique_together = ('student', 'subject')

    def grade(self):
        m = self.marks
        if m >= 90: return 'A+'
        if m >= 80: return 'A'
        if m >= 70: return 'B+'
        if m >= 60: return 'B'
        if m >= 50: return 'C'
        return 'F'

    @property
    def percentage(self):
        return (self.marks / self.total_marks) * 100

    @property
    def status(self):
        return "Pass" if self.marks >= 50 else "Fail"

    def __str__(self):
        return f"{self.student.roll_no} - {self.subject.name}: {self.marks}"
