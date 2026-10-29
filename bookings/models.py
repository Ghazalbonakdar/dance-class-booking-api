from django.db import models


class DanceClass(models.Model):
    LEVEL_CHOICES = [
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
    ]

    title = models.CharField(max_length=200)
    instructor = models.CharField(max_length=100)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    capacity = models.PositiveIntegerField()
    date = models.DateField()
    start_time = models.TimeField()

    def __str__(self):
        return self.title


class Enrollment(models.Model):
    dance_class = models.ForeignKey(
        DanceClass,
        on_delete=models.CASCADE,
        related_name="enrollments",
    )
    student_name = models.CharField(max_length=100)
    student_email = models.EmailField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["dance_class", "student_email"],
                name="unique_student_per_dance_class",
            )
        ]

    def __str__(self):
        return f"{self.student_name} - {self.dance_class.title}"