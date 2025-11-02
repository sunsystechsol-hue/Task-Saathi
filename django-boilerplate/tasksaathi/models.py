from django.db import models
from django.utils.translation import gettext_lazy as _
from atomicloops.models import AtomicBaseModel
from users.models import Users


class Company(AtomicBaseModel):
    name = models.CharField(verbose_name=_("Company Name"), max_length=255, db_column="name")
    userId = models.ForeignKey(
        Users,
        verbose_name=_("Company User Id"),
        related_name="company_user",
        db_column="user_id",
        on_delete=models.CASCADE,
    )
    registrationDocument = models.URLField(
        verbose_name=_("Registration Document"),
        max_length=512,
        db_column="registration_document",
        null=True,
        blank=True
    )
    contactNumber = models.CharField(
        verbose_name=_("Contact Number"),
        max_length=20,
        db_column="contact_number",
        null=True,
        blank=True
    )
    isVerified = models.BooleanField(verbose_name=_("Is Verified"), default=False, db_column="is_verified")
    
    class Meta:
        db_table = "company"
        verbose_name_plural = "companies"
        managed = True
        
    def __str__(self):
        return self.name


class Task(AtomicBaseModel):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )
    
    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    )
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    dueDate = models.DateField(null=True, blank=True)
    assignedTo = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='assigned_tasks')
    createdBy = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='created_tasks')
    companyId = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='tasks')
    
    class Meta:
        db_table = "task"
        verbose_name_plural = "tasks"
        managed = True
        
    def __str__(self):
        return self.title