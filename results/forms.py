from django.contrib import admin
from .models import Result
from django import forms

class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['student', 'subject', 'marks'] 


