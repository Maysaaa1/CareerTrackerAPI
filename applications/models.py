from django.contrib.auth.models import User
from django.db import models


class Company(models.Model):
    """
    Represents a company saved by a user for tracking job applications.
    """

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="companies",
    )
    name = models.CharField(max_length=150)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=150, blank=True)
    industry = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "companies"
        constraints = [
            models.UniqueConstraint(
                fields=["owner", "name"],
                name="unique_company_name_per_owner",
            )
        ]

    def __str__(self) -> str:
        return self.name


class JobApplication(models.Model):
    """
    Represents a job application submitted by a user to a company.
    """

    class Status(models.TextChoices):
        SAVED = "saved", "Saved"
        APPLIED = "applied", "Applied"
        SCREENING = "screening", "Screening"
        INTERVIEW = "interview", "Interview"
        OFFER = "offer", "Offer"
        REJECTED = "rejected", "Rejected"
        WITHDRAWN = "withdrawn", "Withdrawn"

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="job_applications",
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="job_applications",
    )
    position_title = models.CharField(max_length=150)
    job_description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SAVED,
    )
    source = models.CharField(max_length=100, blank=True)
    job_url = models.URLField(blank=True)
    applied_date = models.DateField(null=True, blank=True)
    salary_min = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    salary_max = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.CheckConstraint(
                condition=(
                    models.Q(salary_min__isnull=True)
                    | models.Q(salary_max__isnull=True)
                    | models.Q(salary_max__gte=models.F("salary_min"))
                ),
                name="salary_max_greater_than_or_equal_to_salary_min",
            )
        ]

    def __str__(self) -> str:
        return f"{self.position_title} at {self.company.name}"


class Interview(models.Model):
    """
    Represents an interview related to a job application.
    """

    class InterviewType(models.TextChoices):
        PHONE = "phone", "Phone"
        HR = "hr", "HR"
        TECHNICAL = "technical", "Technical"
        MANAGERIAL = "managerial", "Managerial"
        FINAL = "final", "Final"
        OTHER = "other", "Other"

    class Result(models.TextChoices):
        PENDING = "pending", "Pending"
        PASSED = "passed", "Passed"
        FAILED = "failed", "Failed"
        CANCELLED = "cancelled", "Cancelled"

    job_application = models.ForeignKey(
        JobApplication,
        on_delete=models.CASCADE,
        related_name="interviews",
    )
    interview_type = models.CharField(
        max_length=20,
        choices=InterviewType.choices,
    )
    scheduled_at = models.DateTimeField()
    location_or_link = models.CharField(max_length=255, blank=True)
    interviewer_name = models.CharField(max_length=150, blank=True)
    notes = models.TextField(blank=True)
    result = models.CharField(
        max_length=20,
        choices=Result.choices,
        default=Result.PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["scheduled_at"]

    def __str__(self) -> str:
        return (
            f"{self.get_interview_type_display()} interview - "
            f"{self.job_application}"
        )


class ApplicationStatusHistory(models.Model):
    """
    Stores the status changes made to a job application.
    """

    job_application = models.ForeignKey(
        JobApplication,
        on_delete=models.CASCADE,
        related_name="status_history",
    )
    old_status = models.CharField(
        max_length=20,
        choices=JobApplication.Status.choices,
        blank=True,
    )
    new_status = models.CharField(
        max_length=20,
        choices=JobApplication.Status.choices,
    )
    changed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-changed_at"]
        verbose_name_plural = "application status history"

    def __str__(self) -> str:
        return (
            f"{self.job_application}: "
            f"{self.old_status or 'None'} → {self.new_status}"
        )
    