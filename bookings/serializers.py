
from rest_framework import serializers
from .models import DanceClass, Enrollment


class DanceClassSerializer(serializers.ModelSerializer):
    enrolled_count = serializers.SerializerMethodField()
    available_spots = serializers.SerializerMethodField()

    class Meta:
        model = DanceClass
        fields = [
            "id",
            "title",
            "instructor",
            "level",
            "capacity",
            "date",
            "start_time",
            "enrolled_count",
            "available_spots",
        ]

    def get_enrolled_count(self, obj):
        return obj.enrollments.count()

    def get_available_spots(self, obj):
        return obj.capacity - obj.enrollments.count()

    def validate_capacity(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Capacity must be greater than zero."
            )

        if (
            self.instance
            and value < self.instance.enrollments.count()
        ):
            raise serializers.ValidationError(
                "Capacity cannot be lower than current enrollment."
            )

        return value


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ["id", "student_name", "student_email"]
