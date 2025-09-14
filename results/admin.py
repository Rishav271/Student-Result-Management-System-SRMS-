# results/admin.py
from django.contrib import admin
from .models import Subject, Result

admin.site.register(Subject)
from django.contrib import admin
from .models import Result

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ("student", "subject", "marks", "grade")
    search_fields = ("student__username", "subject")
