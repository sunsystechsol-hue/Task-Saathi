from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from atomicloops.viewsets import AtomicViewSet
from .models import Company, Task
from .serializers import CompanySerializer, TaskSerializer
from .filters import CompanyFilter, TaskFilter
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated


class CompanyViewSet(AtomicViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filterset_class = CompanyFilter
    permission_classes = [IsAuthenticated]
    search_fields = ["name"]
    ordering_fields = ("createdAt", "updatedAt", "name")
    
    @action(detail=False, methods=["get"], url_path='my-company')
    def my_company(self, request):
        """Get the company associated with the current user"""
        company = self.queryset.filter(userId=request.user).first()
        if company:
            serializer = self.get_serializer(company)
            return Response(serializer.data)
        return Response({"message": "No company found for this user"}, status=status.HTTP_404_NOT_FOUND)


class TaskViewSet(AtomicViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filterset_class = TaskFilter
    permission_classes = [IsAuthenticated]
    search_fields = ["title", "description"]
    ordering_fields = ("createdAt", "updatedAt", "title", "dueDate", "status", "priority")
    
    def get_queryset(self):
        """Filter tasks based on user role"""
        user = self.request.user
        
        # If user is an employer, show all tasks in their company
        if user.userRole == "EMPLOYER":
            company = Company.objects.filter(userId=user).first()
            if company:
                return self.queryset.filter(companyId=company)
        
        # If user is an employee, show only tasks assigned to them
        elif user.userRole == "EMPLOYEE":
            return self.queryset.filter(assignedTo=user)
            
        return self.queryset.none()
    
    @action(detail=False, methods=["get"], url_path='my-tasks')
    def my_tasks(self, request):
        """Get tasks assigned to the current user"""
        tasks = self.queryset.filter(assignedTo=request.user)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=["get"], url_path='company-tasks')
    def company_tasks(self, request):
        """Get all tasks for the user's company"""
        company = Company.objects.filter(userId=request.user).first()
        if not company:
            return Response({"message": "No company found for this user"}, status=status.HTTP_404_NOT_FOUND)
            
        tasks = self.queryset.filter(companyId=company)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=["patch"], url_path='update-status')
    def update_status(self, request, pk=None):
        """Update the status of a task"""
        task = self.get_object()
        status_value = request.data.get('status')
        
        if not status_value or status_value not in dict(Task.STATUS_CHOICES):
            return Response({"message": "Invalid status value"}, status=status.HTTP_400_BAD_REQUEST)
            
        task.status = status_value
        task.save()
        
        serializer = self.get_serializer(task)
        return Response(serializer.data)