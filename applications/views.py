
from rest_framework import filters, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import (
    ApplicationStatusHistory,
    Company,
    Interview,
    JobApplication,
)
from .serializers import (
    ApplicationStatusHistorySerializer,
    CompanySerializer,
    RegisterSerializer,
    InterviewSerializer,
    JobApplicationSerializer,
)

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    
class CompanyListCreateView(generics.ListCreateAPIView):
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Company.objects.filter(
            owner=self.request.user
        ).order_by("name")

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CompanyDetailView(
    generics.RetrieveUpdateDestroyAPIView
):
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Company.objects.filter(
            owner=self.request.user
        )


class JobApplicationListCreateView(
    generics.ListCreateAPIView
):
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = [
        "position_title",
        "company__name",
        "status",
        "source",
    ]
    ordering_fields = [
        "applied_date",
        "created_at",
        "salary_min",
        "salary_max",
    ]
    ordering = ["-created_at"]

    def get_queryset(self):
        queryset = (
            JobApplication.objects
            .filter(owner=self.request.user)
            .select_related("company", "owner")
        )

        status_value = self.request.query_params.get("status")
        company_id = self.request.query_params.get("company")

        if status_value:
            queryset = queryset.filter(status=status_value)

        if company_id:
            queryset = queryset.filter(company_id=company_id)

        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class JobApplicationDetailView(
    generics.RetrieveUpdateDestroyAPIView
):
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            JobApplication.objects
            .filter(owner=self.request.user)
            .select_related("company", "owner")
        )

    def perform_update(self, serializer):
        application = self.get_object()
        old_status = application.status

        updated_application = serializer.save(
            owner=self.request.user
        )

        new_status = updated_application.status

        if old_status != new_status:
            ApplicationStatusHistory.objects.create(
                job_application=updated_application,
                old_status=old_status,
                new_status=new_status,
            )


class InterviewListCreateView(generics.ListCreateAPIView):
    serializer_class = InterviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Interview.objects
            .filter(job_application__owner=self.request.user)
            .select_related(
                "job_application",
                "job_application__company",
            )
            .order_by("scheduled_at")
        )


class InterviewDetailView(
    generics.RetrieveUpdateDestroyAPIView
):
    serializer_class = InterviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Interview.objects
            .filter(job_application__owner=self.request.user)
            .select_related(
                "job_application",
                "job_application__company",
            )
        )


class ApplicationStatusHistoryListView(
    generics.ListAPIView
):
    serializer_class = ApplicationStatusHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            ApplicationStatusHistory.objects
            .filter(job_application__owner=self.request.user)
            .select_related(
                "job_application",
                "job_application__company",
            )
            .order_by("-changed_at")
        )


class ApplicationStatusHistoryDetailView(
    generics.RetrieveAPIView
):
    serializer_class = ApplicationStatusHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            ApplicationStatusHistory.objects
            .filter(job_application__owner=self.request.user)
            .select_related(
                "job_application",
                "job_application__company",
            )
        )