from rest_framework import serializers
from atomicloops.serializers import AtomicSerializer
from .models import Company, Task
from users.models import Users
from users.serializers import UsersSerializer


class CompanySerializer(AtomicSerializer):
    userName = serializers.CharField(source='userId.username', read_only=True)
    userEmail = serializers.CharField(source='userId.email', read_only=True)
    
    class Meta:
        model = Company
        fields = (
            "id",
            "createdAt",
            "updatedAt",
            "name",
            "userId",
            "userName",
            "userEmail",
            "registrationDocument",
            "isVerified",
        )
        get_fields = fields
        list_fields = [
            "id",
            "name",
            "userId",
            "userName",
            "userEmail",
            "isVerified",
        ]


class TaskSerializer(AtomicSerializer):
    assignedToName = serializers.SerializerMethodField(read_only=True)
    assignedToEmail = serializers.CharField(source='assignedTo.email', read_only=True)
    createdByName = serializers.SerializerMethodField(read_only=True)
    companyName = serializers.CharField(source='companyId.name', read_only=True)
    
    class Meta:
        model = Task
        fields = (
            "id",
            "createdAt",
            "updatedAt",
            "title",
            "description",
            "dueDate",
            "status",
            "priority",
            "assignedTo",
            "assignedToName",
            "assignedToEmail",
            "createdBy",
            "createdByName",
            "companyId",
            "companyName",
        )
        get_fields = fields
        list_fields = [
            "id",
            "title",
            "dueDate",
            "status",
            "priority",
            "assignedToName",
            "companyName",
        ]
    
    def get_assignedToName(self, obj):
        if obj.assignedTo:
            return f"{obj.assignedTo.firstName} {obj.assignedTo.lastName}"
        return "N/A"
    
    def get_createdByName(self, obj):
        if obj.createdBy:
            return f"{obj.createdBy.firstName} {obj.createdBy.lastName}"
        return "N/A"