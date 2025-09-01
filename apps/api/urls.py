from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import (
    UserViewSet, ClientViewSet, ClientContactViewSet,
    ProjectViewSet, ProjectRequirementViewSet,
    PaymentViewSet, InvoiceViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'clients', ClientViewSet)
router.register(r'client-contacts', ClientContactViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'project-requirements', ProjectRequirementViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'invoices', InvoiceViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/', obtain_auth_token, name='api_token_auth'),
]
