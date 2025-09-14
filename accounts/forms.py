# accounts/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=Profile._meta.get_field('role').choices)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'role']

# accounts/forms.py
from django import forms
from django.contrib.auth.models import User
from students.models import Student

class StudentRegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Email'}))

    class Meta:
        model = Student
        fields = ['full_name', 'roll_no', 'enrollment_no', 'course', 'duration', 'semester', 'image']
        widgets = {
            'full_name': forms.TextInput(attrs={'class':'form-control','placeholder':'Full Name'}),
            'roll_no': forms.TextInput(attrs={'class':'form-control','placeholder':'Roll Number'}),
            'enrollment_no': forms.TextInput(attrs={'class':'form-control','placeholder':'Enrollment Number'}),
            'course': forms.TextInput(attrs={'class':'form-control','placeholder':'Course'}),
            'duration': forms.TextInput(attrs={'class':'form-control','placeholder':'Duration'}),
            'semester': forms.NumberInput(attrs={'class':'form-control','placeholder':'Semester'}),
        }

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
            email=self.cleaned_data['email']
        )
        student = super().save(commit=False)
        student.user = user
        if commit:
            student.save()
        return student
