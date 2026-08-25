from django.urls import path

from .views import (
    ApplicationStatusHistoryDetailView,
    ApplicationStatusHistoryListView,
    CompanyDetailView,
    CompanyListCreateView,
    InterviewDetailView,
    InterviewListCreateView,
    JobApplicationDetailView,
    JobApplicationListCreateView,
    RegisterView
)


urlpatterns = [
    path(
        "companies/",
        CompanyListCreateView.as_view(),
        name="company-list-create",
    ),
    path(
        "companies/<int:pk>/",
        CompanyDetailView.as_view(),
        name="company-detail",
    ),
    path(
        "job-applications/",
        JobApplicationListCreateView.as_view(),
        name="job-application-list-create",
    ),
    path(
        "job-applications/<int:pk>/",
        JobApplicationDetailView.as_view(),
        name="job-application-detail",
    ),
    path(
        "interviews/",
        InterviewListCreateView.as_view(),
        name="interview-list-create",
    ),
    path(
        "interviews/<int:pk>/",
        InterviewDetailView.as_view(),
        name="interview-detail",
    ),
    path(
        "status-history/",
        ApplicationStatusHistoryListView.as_view(),
        name="status-history-list",
    ),
    path(
        "status-history/<int:pk>/",
        ApplicationStatusHistoryDetailView.as_view(),
        name="status-history-detail",
    ),
    path(
    "auth/register/",
    RegisterView.as_view(),
    name="register",
),
]