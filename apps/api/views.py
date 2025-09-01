from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from apps.clients.models import Client, ClientContact
from apps.projects.models import Project, ProjectRequirement
from apps.payments.models import Payment, Invoice
from .serializers import (
    UserSerializer, ClientSerializer, ClientDetailSerializer, ClientContactSerializer,
    ProjectSerializer, ProjectDetailSerializer, ProjectRequirementSerializer,
    PaymentSerializer, InvoiceSerializer
)


class IsOwnerOrStaff(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or staff members.
    """
    def has_object_permission(self, request, view, obj):
        # Staff members can access everything
        if request.user.is_staff:
            return True
        
        # Check if user is assigned to the object
        if hasattr(obj, 'assigned_to'):
            return obj.assigned_to == request.user
        elif hasattr(obj, 'client') and hasattr(obj.client, 'assigned_to'):
            return obj.client.assigned_to == request.user
        
        return False


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'first_name', 'last_name', 'email']


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrStaff]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'client_type', 'industry', 'assigned_to']
    search_fields = ['name', 'company_name', 'email', 'phone', 'address']
    ordering_fields = ['name', 'company_name', 'created_at', 'updated_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Client.objects.all()
        return Client.objects.filter(assigned_to=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ClientDetailSerializer
        return ClientSerializer
    
    @action(detail=True, methods=['get'])
    def projects(self, request, pk=None):
        client = self.get_object()
        projects = client.projects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def payments(self, request, pk=None):
        client = self.get_object()
        payments = client.payments.all()
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)


class ClientContactViewSet(viewsets.ModelViewSet):
    queryset = ClientContact.objects.all()
    serializer_class = ClientContactSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrStaff]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['client', 'is_primary']
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return ClientContact.objects.all()
        return ClientContact.objects.filter(client__assigned_to=self.request.user)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrStaff]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'priority', 'client', 'assigned_to']
    search_fields = ['title', 'description', 'client__name']
    ordering_fields = ['title', 'start_date', 'due_date', 'created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Project.objects.all()
        return Project.objects.filter(assigned_to=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProjectDetailSerializer
        return ProjectSerializer
    
    @action(detail=True, methods=['get'])
    def payments(self, request, pk=None):
        project = self.get_object()
        payments = project.payments.all()
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def requirements(self, request, pk=None):
        project = self.get_object()
        requirements = project.project_requirements.all()
        serializer = ProjectRequirementSerializer(requirements, many=True)
        return Response(serializer.data)


class ProjectRequirementViewSet(viewsets.ModelViewSet):
    queryset = ProjectRequirement.objects.all()
    serializer_class = ProjectRequirementSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrStaff]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['project', 'is_completed']
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return ProjectRequirement.objects.all()
        return ProjectRequirement.objects.filter(project__assigned_to=self.request.user)


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrStaff]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'payment_method', 'client', 'project']
    search_fields = ['invoice_number', 'description', 'project__title', 'client__name']
    ordering_fields = ['payment_date', 'due_date', 'amount', 'created_at']
    ordering = ['-payment_date']
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Payment.objects.all()
        return Payment.objects.filter(project__assigned_to=self.request.user)
    
    @action(detail=True, methods=['get'])
    def invoice(self, request, pk=None):
        payment = self.get_object()
        try:
            invoice = payment.invoice
            serializer = InvoiceSerializer(invoice)
            return Response(serializer.data)
        except Invoice.DoesNotExist:
            return Response({'detail': 'No invoice found for this payment'}, status=404)


class InvoiceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrStaff]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['issue_date', 'due_date']
    search_fields = ['invoice_number']
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Invoice.objects.all()
        return Invoice.objects.filter(payment__project__assigned_to=self.request.user)
