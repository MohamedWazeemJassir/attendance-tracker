from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # Admin dashboard
    path("dashboard/admin/", views.admin_dashboard, name="admin_dashboard"),

    # Teacher management
    path("dashboard/admin/teachers/", views.teacher_list, name="teacher_list"),
    path("dashboard/admin/teachers/add/", views.teacher_create, name="teacher_create"),
    path("dashboard/admin/teachers/edit/<int:pk>/", views.teacher_edit, name="teacher_edit"),
    path("dashboard/admin/teachers/delete/<int:pk>/", views.teacher_delete, name="teacher_delete"),

    # Student management
    path("dashboard/admin/students/", views.student_list, name="student_list"),
    path("dashboard/admin/students/add/", views.student_create, name="student_create"),
    path("dashboard/admin/students/edit/<int:pk>/", views.student_edit, name="student_edit"),
    path("dashboard/admin/students/delete/<int:pk>/", views.student_delete, name="student_delete"),

    # Teacher Dashboard
    path("dashboard/teacher/", views.teacher_dashboard, name="teacher_dashboard"),
    path("dashboard/teacher/attendance/mark/", views.mark_attendance, name="mark_attendance"),
    path("dashboard/teacher/students/", views.assigned_students, name="assigned_students"),
    path("dashboard/teacher/attendance/edit/<int:pk>/", views.edit_attendance, name="edit_attendance"),

    # Reports
    path('reports/', views.attendance_report, name='attendance_report'),
    path("reports/student/<int:student_id>/", views.student_attendance_report, name="student_attendance_report"),
    path("reports/student/<int:student_id>/monthly/", views.monthly_summary, name="monthly_summary"),
    path("reports/student/<int:student_id>/export/", views.export_student_attendance_csv, name="export_student_attendance_csv"),

    # Auth
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
