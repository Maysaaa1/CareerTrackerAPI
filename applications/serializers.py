from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    ApplicationStatusHistory,
    Company,
    Interview,
    JobApplication,
)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8,
    )

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "password",
        )
        read_only_fields = ("id",)

    def validate_email(self, email):
        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError(
                "A user with this email already exists."
            )

        return email

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
        )

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = (
            "id",
            "owner",
            "name",
            "website",
            "location",
            "industry",
            "description",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "owner",
            "created_at",
            "updated_at",
        )


class JobApplicationSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(
        source="company.name",
        read_only=True,
    )

    class Meta:
        model = JobApplication
        fields = (
            "id",
            "owner",
            "company",
            "company_name",
            "position_title",
            "job_description",
            "status",
            "source",
            "job_url",
            "applied_date",
            "salary_min",
            "salary_max",
            "notes",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "owner",
            "company_name",
            "created_at",
            "updated_at",
        )

    def validate_company(self, company):
        request = self.context.get("request")

        if request and company.owner != request.user:
            raise serializers.ValidationError(
                "You cannot use a company that belongs to another user."
            )

        return company

    def validate(self, attrs):
        salary_min = attrs.get(
            "salary_min",
            getattr(self.instance, "salary_min", None),
        )
        salary_max = attrs.get(
            "salary_max",
            getattr(self.instance, "salary_max", None),
        )

        if (
            salary_min is not None
            and salary_max is not None
            and salary_max < salary_min
        ):
            raise serializers.ValidationError(
                {
                    "salary_max": (
                        "Maximum salary must be greater than or equal "
                        "to minimum salary."
                    )
                }
            )

        return attrs


class InterviewSerializer(serializers.ModelSerializer):
    application_title = serializers.CharField(
        source="job_application.position_title",
        read_only=True,
    )
    company_name = serializers.CharField(
        source="job_application.company.name",
        read_only=True,
    )

    class Meta:
        model = Interview
        fields = (
            "id",
            "job_application",
            "application_title",
            "company_name",
            "interview_type",
            "scheduled_at",
            "location_or_link",
            "interviewer_name",
            "notes",
            "result",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "application_title",
            "company_name",
            "created_at",
            "updated_at",
        )

    def validate_job_application(self, job_application):
        request = self.context.get("request")

        if request and job_application.owner != request.user:
            raise serializers.ValidationError(
                "You cannot add an interview to another user's application."
            )

        return job_application


class ApplicationStatusHistorySerializer(
    serializers.ModelSerializer
):
    application_title = serializers.CharField(
        source="job_application.position_title",
        read_only=True,
    )
    company_name = serializers.CharField(
        source="job_application.company.name",
        read_only=True,
    )

    class Meta:
        model = ApplicationStatusHistory
        fields = (
            "id",
            "job_application",
            "application_title",
            "company_name",
            "old_status",
            "new_status",
            "changed_at",
        )
        read_only_fields = (
            "id",
            "application_title",
            "company_name",
            "changed_at",
        )

    def validate_job_application(self, job_application):
        request = self.context.get("request")

        if request and job_application.owner != request.user:
            raise serializers.ValidationError(
                "You cannot access another user's application."
            )

        return job_application