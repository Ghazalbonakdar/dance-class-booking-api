
from django.urls import path
from . import views

urlpatterns = [
    path("classes/", views.class_list_create, name="class-list-create"),
    path("classes/<int:pk>/", views.class_detail, name="class-detail"),
    path(
        "classes/<int:pk>/enroll/",
        views.enroll_student,
        name="enroll-student",
    ),
    path(
        "classes/<int:pk>/cancel/",
        views.cancel_enrollment,
        name="cancel-enrollment",
    ),
]