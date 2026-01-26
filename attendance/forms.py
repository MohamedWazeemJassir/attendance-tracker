from django import forms
from datetime import date
from .models import Student, Teacher, Attendance
from django.contrib.auth.models import User

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["name", "roll_number", "class_name", "assigned_teacher"]

class TeacherCreateForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    employee_id = forms.CharField()

class TeacherEditForm(forms.Form):
    username = forms.CharField()
    employee_id = forms.CharField()

    def __init__(self, *args, **kwargs):
        teacher = kwargs.pop("teacher")
        super().__init__(*args, **kwargs)

        self.fields["username"].initial = teacher.user.username
        self.fields["employee_id"].initial = teacher.employee_id


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ["student", "date", "status"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["date"].initial = date.today()