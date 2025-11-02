from django.contrib import admin
from .models import Company, Task

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'userId', 'isVerified', 'createdAt', 'updatedAt')
    list_filter = ('isVerified',)
    search_fields = ('name',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'priority', 'dueDate', 'assignedTo', 'createdBy', 'companyId')
    list_filter = ('status', 'priority')
    search_fields = ('title', 'description')
    date_hierarchy = 'createdAt'