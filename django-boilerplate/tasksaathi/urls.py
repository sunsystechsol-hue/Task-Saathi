from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CompanyViewSet, TaskViewSet

router = DefaultRouter()
router.register(r'companies', CompanyViewSet)
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('', include(router.urls)),
]