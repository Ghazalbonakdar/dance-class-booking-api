
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import DanceClass, Enrollment
from .serializers import DanceClassSerializer, EnrollmentSerializer


@api_view(["GET", "POST"])
def class_list_create(request):
    if request.method == "GET":
        classes = DanceClass.objects.all().order_by("date", "start_time")
        serializer = DanceClassSerializer(classes, many=True)
        return Response(serializer.data)

    serializer = DanceClassSerializer(data=request.data)
    if serializer.is_valid():
        dance_class = serializer.save()
        return Response(
            DanceClassSerializer(dance_class).data,
            status=status.HTTP_201_CREATED,
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(["GET", "PATCH", "DELETE"])
def class_detail(request, pk):
    dance_class = get_object_or_404(DanceClass, pk=pk)

    if request.method == "GET":
        return Response(DanceClassSerializer(dance_class).data)

    if request.method == "PATCH":
        serializer = DanceClassSerializer(
            dance_class,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            dance_class = serializer.save()
            return Response(DanceClassSerializer(dance_class).data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    dance_class.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
def enroll_student(request, pk):
    dance_class = get_object_or_404(DanceClass, pk=pk)

    serializer = EnrollmentSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    email = serializer.validated_data["student_email"]

    if Enrollment.objects.filter(
        dance_class=dance_class,
        student_email__iexact=email,
    ).exists():
        return Response(
            {"error": "This student is already enrolled."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if dance_class.enrollments.count() >= dance_class.capacity:
        return Response(
            {"error": "This class is full."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    enrollment = serializer.save(dance_class=dance_class)
    return Response(
        EnrollmentSerializer(enrollment).data,
        status=status.HTTP_201_CREATED,
    )


@api_view(["POST"])
def cancel_enrollment(request, pk):
    dance_class = get_object_or_404(DanceClass, pk=pk)
    email = request.data.get("student_email")

    if not email:
        return Response(
            {"error": "student_email is required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    enrollment = Enrollment.objects.filter(
        dance_class=dance_class,
        student_email__iexact=email,
    ).first()

    if enrollment is None:
        return Response(
            {"error": "Enrollment not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    enrollment.delete()
    return Response(
        {"message": "Enrollment cancelled successfully."},
        status=status.HTTP_200_OK,
    )