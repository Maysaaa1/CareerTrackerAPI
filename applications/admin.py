from django.contrib import admin

from .models import (
    ApplicationStatusHistory,
    Company,
    Interview,
    JobApplication,
)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "owner",
        "industry",
        "location",
        "created_at",
    )
    search_fields = (
        "name",
        "industry",
        "location",
        "owner__username",
        "owner__email",
    )
    list_filter = (
        "industry",
        "created_at",
    )
    ordering = ("name",)


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "position_title",
        "company",
        "owner",
        "status",
        "applied_date",
        "created_at",
    )
    search_fields = (
        "position_title",
        "company__name",
        "owner__username",
        "owner__email",
    )
    list_filter = (
        "status",
        "source",
        "applied_date",
        "created_at",
    )
    ordering = ("-created_at",)


@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display = (
        "job_application",
        "interview_type",
        "scheduled_at",
        "result",
    )
    search_fields = (
        "job_application__position_title",
        "job_application__company__name",
        "interviewer_name",
    )
    list_filter = (
        "interview_type",
        "result",
        "scheduled_at",
    )
    ordering = ("scheduled_at",)


@admin.register(ApplicationStatusHistory)
class ApplicationStatusHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "job_application",
        "old_status",
        "new_status",
        "changed_at",
    )
    search_fields = (
        "job_application__position_title",
        "job_application__company__name",
    )
    list_filter = (
        "old_status",
        "new_status",
        "changed_at",
    )
    ordering = ("-changed_at",)