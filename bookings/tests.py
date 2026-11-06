
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from bookings.models import DanceClass


class DanceClassAPITests(APITestCase):

    def setUp(self):
        """Create a dance class before each test."""
        self.dance_class = DanceClass.objects.create(
            title="Ballet Basics",
            instructor="Anna",
            level="beginner",
            capacity=2,
            date="2026-11-10",
            start_time="15:30:00",
        )

        self.classes_url = reverse("class-list-create")
        self.enroll_url = reverse(
            "enroll-student",
            args=[self.dance_class.id]
        )
        self.cancel_url = reverse(
            "cancel-enrollment",
            args=[self.dance_class.id]
        )

    # 1. A valid dance class can be created
    def test_create_dance_class(self):
        data = {
            "title": "Advanced Ballet",
            "instructor": "Maria",
            "level": "advanced",
            "capacity": 15,
            "date": "2026-12-01",
            "start_time": "17:00:00",
        }

        response = self.client.post(
            self.classes_url,
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(DanceClass.objects.count(), 2)

    # 2. Invalid dance class data is rejected
    def test_create_dance_class_with_invalid_data(self):
        data = {
            "title": "Invalid Class",
            "instructor": "Anna",
            "level": "expert",  # Not an allowed level
            "capacity": 10,
            "date": "2026-12-01",
            "start_time": "17:00:00",
        }

        response = self.client.post(
            self.classes_url,
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(DanceClass.objects.count(), 1)

    # 3. A student can successfully enroll
    def test_student_can_enroll(self):
        data = {
            "student_name": "Sara",
            "student_email": "sara@example.com",
        }

        response = self.client.post(
            self.enroll_url,
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            self.dance_class.enrollments.count(),
            1
        )

    # 4. A student cannot enroll in a full class
    def test_cannot_enroll_in_full_class(self):
        self.dance_class.capacity = 1
        self.dance_class.save()

        self.client.post(
            self.enroll_url,
            {
                "student_name": "Sara",
                "student_email": "sara@example.com",
            },
            format="json"
        )

        response = self.client.post(
            self.enroll_url,
            {
                "student_name": "Ali",
                "student_email": "ali@example.com",
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            self.dance_class.enrollments.count(),
            1
        )

    # 5. A student cannot enroll twice in the same class
    def test_student_cannot_enroll_twice(self):
        data = {
            "student_name": "Sara",
            "student_email": "sara@example.com",
        }

        self.client.post(
            self.enroll_url,
            data,
            format="json"
        )

        response = self.client.post(
            self.enroll_url,
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            self.dance_class.enrollments.count(),
            1
        )

    # 6. Cancelling an enrollment frees a spot
    def test_cancelling_enrollment_frees_spot(self):
        self.client.post(
            self.enroll_url,
            {
                "student_name": "Sara",
                "student_email": "sara@example.com",
            },
            format="json"
        )

        response = self.client.post(
            self.cancel_url,
            {"student_email": "sara@example.com"},
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            self.dance_class.enrollments.count(),
            0
        )

        # Another student should now be able to enroll.
        new_response = self.client.post(
            self.enroll_url,
            {
                "student_name": "Ali",
                "student_email": "ali@example.com",
            },
            format="json"
        )

        self.assertEqual(
            new_response.status_code,
            status.HTTP_201_CREATED
        )

    # 7. Capacity cannot be reduced below current enrollment
    def test_cannot_reduce_capacity_below_enrollment(self):
        # Enroll two students first.
        self.client.post(
            self.enroll_url,
            {
                "student_name": "Sara",
                "student_email": "sara@example.com",
            },
            format="json"
        )

        self.client.post(
            self.enroll_url,
            {
                "student_name": "Ali",
                "student_email": "ali@example.com",
            },
            format="json"
        )

        # Try to reduce capacity from 2 to 1.
        response = self.client.patch(
            reverse("class-detail", args=[self.dance_class.id]),
            {"capacity": 1},
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.dance_class.refresh_from_db()
        self.assertEqual(self.dance_class.capacity, 2)

    def test_student_cannot_enroll_with_email_different_case(self):
        first_response = self.client.post(
            self.enroll_url,
            {
                "student_name": "Sara",
                "student_email": "sara@example.com",
            },
            format="json",
        )

        second_response = self.client.post(
            self.enroll_url,
            {
                "student_name": "Sara",
                "student_email": "SARA@EXAMPLE.COM",
            },
            format="json",
        )

        self.assertEqual(
            first_response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertEqual(
            second_response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertEqual(self.dance_class.enrollments.count(), 1)

    # 9. Cancelling an enrollment that doesn't exist
    def test_cannot_cancel_nonexistent_enrollment(self):
        response = self.client.post(
            self.cancel_url,
            {"student_email": "unknown@example.com"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )


    # 10. Cancelling without an email is rejected
    def test_cannot_cancel_without_email(self):
        response = self.client.post(
            self.cancel_url,
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )