import django_filters
from atomicloops.filters import AtomicDateFilter
from .models import Company, Task


class CompanyFilter(AtomicDateFilter):
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    isVerified = django_filters.BooleanFilter(field_name="isVerified")
    
    class Meta:
        model = Company
        fields = ["name", "userId", "isVerified"]


class TaskFilter(AtomicDateFilter):
    title = django_filters.CharFilter(field_name="title", lookup_expr="icontains")
    description = django_filters.CharFilter(field_name="description", lookup_expr="icontains")
    status = django_filters.CharFilter(field_name="status")
    priority = django_filters.CharFilter(field_name="priority")
    dueDateFrom = django_filters.DateFilter(field_name="dueDate", lookup_expr="gte")
    dueDateTo = django_filters.DateFilter(field_name="dueDate", lookup_expr="lte")
    
    class Meta:
        model = Task
        fields = [
            "title", 
            "status", 
            "priority", 
            "assignedTo", 
            "createdBy", 
            "companyId",
            "dueDateFrom",
            "dueDateTo"
        ]