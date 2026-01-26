from datetime import datetime, date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User 
from django.core.exceptions import PermissionDenied
from django.contrib.auth import login as auth_login, logout
from django.db import IntegrityError
from django.db.models import Count, Q
from datetime import date
from .models import Attendance, Student, Teacher, UserProfile
from .forms import StudentForm, TeacherCreateForm, AttendanceForm, TeacherEditForm
import csv
from django.http import HttpResponse

def home(request):
    if not request.user.is_authenticated:
        return render(request, "home.html")

    role = request.user.userprofile.role
    if role == "ADMIN":
        return redirect("admin_dashboard")
    return redirect("teacher_dashboard")

def login_view(request):
    if request.user.is_authenticated:
        return redirect("attendance_report")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)

            role = user.userprofile.role
            if role == "ADMIN":
                return redirect("admin_dashboard")
            return redirect("teacher_dashboard")

    else:
        form = AuthenticationForm()

    return render(request, "login.html", {"form": form})

@login_required
def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def admin_dashboard(request):
    if request.user.userprofile.role != "ADMIN":
        raise PermissionDenied

    from datetime import date
    today = date.today()

    context = {
        "total_students": Student.objects.count(),
        "total_teachers": Teacher.objects.count(),
        "total_attendance": Attendance.objects.count(),
        "today_present": Attendance.objects.filter(
            date=today, status="PRESENT"
        ).count(),
        "today_absent": Attendance.objects.filter(
            date=today, status="ABSENT"
        ).count(),
    }

    return render(request, "admin_dashboard.html", context)

@login_required
def attendance_report(request):
    selected_date = request.GET.get("date")

    if selected_date:
        filter_date = selected_date
    else:
        filter_date = date.today()

    if request.user.userprofile.role == "ADMIN":
        students = Student.objects.all()

    else:
        teacher = Teacher.objects.get(user=request.user)
        students = Student.objects.filter(assigned_teacher=teacher)

    report_data = []

    for student in students:
        attendance = Attendance.objects.filter(
            student=student,
            date=filter_date
        ).first()

        report_data.append({
            "student": student,
            "status": attendance.status if attendance else "Not Marked"
        })

    return render(
        request,
        "report.html",
        {
            "report_data": report_data,
            "selected_date": filter_date
        }
    )

@login_required
def student_list(request):
    if request.user.userprofile.role != "ADMIN":
        raise PermissionDenied

    students = Student.objects.all()
    return render(request, "student_list.html", {"students": students})

@login_required
def student_create(request):
    if request.user.userprofile.role != "ADMIN":
        raise PermissionDenied

    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("student_list")
    else:
        form = StudentForm()

    return render(request, "student_form.html", {"form": form})

@login_required
def student_edit(request, pk):
    if request.user.userprofile.role != "ADMIN":
        raise PermissionDenied

    student = get_object_or_404(Student, pk=pk)

    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect("student_list")
    else:
        form = StudentForm(instance=student)

    return render(request, "student_form.html", {"form": form})

@login_required
def student_delete(request, pk):
    if request.user.userprofile.role != "ADMIN":
        raise PermissionDenied

    student = get_object_or_404(Student, pk=pk)
    student.delete()
    return redirect("student_list")

@login_required
def teacher_create(request):
    if request.user.userprofile.role != "ADMIN":
        raise PermissionDenied

    if request.method == "POST":
        form = TeacherCreateForm(request.POST)

        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"]
            )

            UserProfile.objects.create(
                user=user,
                role="TEACHER"
            )

            Teacher.objects.create(
                user=user,
                employee_id=form.cleaned_data["employee_id"]
            )

            return redirect("teacher_list")

    else:
        form = TeacherCreateForm()

    return render(
        request,
        "teacher_form.html",
        {"form": form}
    )

@login_required
def teacher_list(request):
    if request.user.userprofile.role != "ADMIN":
        raise PermissionDenied

    teachers = Teacher.objects.all()
    return render(request, "teacher_list.html", {"teachers": teachers})

@login_required
def teacher_edit(request, pk):
    if request.user.userprofile.role != "ADMIN":
        raise PermissionDenied

    teacher = get_object_or_404(Teacher, pk=pk)

    if request.method == "POST":
        form = TeacherEditForm(request.POST, teacher=teacher)
        if form.is_valid():
            teacher.user.username = form.cleaned_data["username"]
            teacher.user.save()

            teacher.employee_id = form.cleaned_data["employee_id"]
            teacher.save()

            return redirect("teacher_list")
    else:
        form = TeacherEditForm(teacher=teacher)

    return render(request, "teacher_form.html", {"form": form})

@login_required
def teacher_delete(request, pk):
    if request.user.userprofile.role != "ADMIN":
        raise PermissionDenied

    teacher = get_object_or_404(Teacher, pk=pk)
    teacher.user.delete()  
    return redirect("teacher_list")

@login_required
def teacher_dashboard(request):

    if request.user.userprofile.role != "TEACHER":
        return render(request, "403.html")

    teacher = Teacher.objects.get(user=request.user)
    today = date.today()

    context = {
        "total_students": Student.objects.filter(
            assigned_teacher=teacher
        ).count(),

        "today_present": Attendance.objects.filter(
            marked_by=teacher,
            date=today,
            status="PRESENT"
        ).count(),

        "today_absent": Attendance.objects.filter(
            marked_by=teacher,
            date=today,
            status="ABSENT"
        ).count(),
    }

    return render(
        request,
        "teacher_dashboard.html",
        context
    )

@login_required
def mark_attendance(request):
    if request.user.userprofile.role != "TEACHER":
        raise PermissionDenied

    teacher = Teacher.objects.get(user=request.user)

    if request.method == "POST":
        form = AttendanceForm(request.POST)

        form.fields["student"].queryset = Student.objects.filter(
            assigned_teacher=teacher
        )

        if form.is_valid():
            attendance = form.save(commit=False)
            attendance.marked_by = teacher

            try:
                attendance.save()
                return redirect("teacher_dashboard")
            except IntegrityError:
                form.add_error(
                    None,
                    "Attendance for this student on this date is already marked."
                )

    else:
        form = AttendanceForm()
        form.fields["student"].queryset = Student.objects.filter(
            assigned_teacher=teacher
        )

    return render(
        request,
        "mark_attendance.html",
        {"form": form}
    )

@login_required
def assigned_students(request):

    if request.user.userprofile.role != "TEACHER":
        raise PermissionDenied

    teacher = Teacher.objects.get(user=request.user)
    students = Student.objects.filter(assigned_teacher=teacher)

    return render(
        request,
        "assigned_students.html",
        {"students": students}
    )

@login_required
def edit_attendance(request, pk):
    if request.user.userprofile.role != "TEACHER":
        raise PermissionDenied

    teacher = Teacher.objects.get(user=request.user)

    attendance = get_object_or_404(
        Attendance,
        pk=pk,
        marked_by=teacher
    )

    if attendance.date > date.today():
        raise PermissionDenied("Cannot edit future attendance.")

    if request.method == "POST":
        form = AttendanceForm(request.POST, instance=attendance)
        if form.is_valid():
            form.save()
            return redirect("attendance_report")
    else:
        form = AttendanceForm(instance=attendance)

    return render(
        request,
        "edit_attendance.html",
        {"form": form, "attendance": attendance}
    )

from datetime import date, datetime

@login_required
def attendance_report(request):
    role = request.user.userprofile.role

    date_str = request.GET.get("date")
    student_query = request.GET.get("student")
    class_query = request.GET.get("class")

    if role == "ADMIN":
        students = Student.objects.all()
        teacher = None
    else:
        teacher = Teacher.objects.get(user=request.user)
        students = Student.objects.filter(assigned_teacher=teacher)

    if student_query:
        students = students.filter(name__icontains=student_query)

    if class_query:
        students = students.filter(class_name__icontains=class_query)

    report_data = []

    if not date_str and not student_query and not class_query:
        selected_date = date.today()
        mode = "date"

    elif date_str:
        selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        mode = "date"

    else:
        mode = "search"

    if mode == "date":
        for student in students:
            attendance = Attendance.objects.filter(
                student=student,
                date=selected_date
            ).first()

            report_data.append({
                "student": student,
                "date": selected_date,
                "attendance": attendance,
                "can_edit": (
                    role == "TEACHER"
                    and attendance is not None
                    and attendance.marked_by == teacher
                )
            })

        report_title = f"Attendance Report for {selected_date.strftime('%d-%m-%Y')}"
        date_value = selected_date.strftime("%Y-%m-%d")

    else:
        records = Attendance.objects.filter(student__in=students).order_by("-date")

        report_data = [{
            "student": a.student,
            "date": a.date,
            "attendance": a,
            "can_edit": (
                role == "TEACHER"
                and a.marked_by == teacher
            )
        } for a in records]

        report_title = "Attendance Report (Filtered Results)"
        date_value = ""

    return render(
        request,
        "report.html",
        {
            "report_data": report_data,
            "report_title": report_title,
            "role": role,
            "student_query": student_query or "",
            "class_query": class_query or "",
            "date_value": date_value,
        }
    )


@login_required
def student_attendance_report(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    if request.user.userprofile.role == "TEACHER":
        teacher = Teacher.objects.get(user=request.user)
        if student.assigned_teacher != teacher:
            raise PermissionDenied

    attendance_records = Attendance.objects.filter(
        student=student
    ).order_by("-date")

    return render(
        request,
        "student_attendance_report.html",
        {
            "student": student,
            "attendance_records": attendance_records,
        }
    )

@login_required
def monthly_summary(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    if request.user.userprofile.role == "TEACHER":
        teacher = Teacher.objects.get(user=request.user)
        if student.assigned_teacher != teacher:
            raise PermissionDenied

    month_str = request.GET.get("month")

    if month_str:
        year, month = map(int, month_str.split("-"))
    else:
        today = datetime.today()
        year, month = today.year, today.month

    total = Attendance.objects.filter(
        student=student,
        date__year=year,
        date__month=month
    ).count()

    present = Attendance.objects.filter(
        student=student,
        date__year=year,
        date__month=month,
        status="PRESENT"
    ).count()

    absent = Attendance.objects.filter(
        student=student,
        date__year=year,
        date__month=month,
        status="ABSENT"
    ).count()

    present_percent = (present / total * 100) if total else 0
    absent_percent = (absent / total * 100) if total else 0

    return render(
        request,
        "monthly_summary.html",
        {
            "student": student,
            "year": year,
            "month": month,
            "total": total,
            "present": present,
            "absent": absent,
            "present_percent": round(present_percent, 2),
            "absent_percent": round(absent_percent, 2),
        }
    )

@login_required
def export_student_attendance_csv(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    if request.user.userprofile.role == "TEACHER":
        teacher = Teacher.objects.get(user=request.user)
        if student.assigned_teacher != teacher:
            raise PermissionDenied

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = (
        f'attachment; filename="{student.name}_attendance.csv"'
    )

    writer = csv.writer(response)
    writer.writerow(["Date", "Status"])

    for a in Attendance.objects.filter(student=student).order_by("date"):
        writer.writerow([a.date, a.status])

    return response
