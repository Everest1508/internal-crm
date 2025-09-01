from rest_framework import serializers
from django.contrib.auth.models import User
from apps.clients.models import Client, ClientContact
from apps.projects.models import Project, ProjectRequirement
from apps.payments.models import Payment, Invoice


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff']
        read_only_fields = ['id', 'is_staff']


class ClientContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientContact
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
    contacts = ClientContactSerializer(many=True, read_only=True)
    assigned_to = UserSerializer(read_only=True)
    assigned_to_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = Client
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class ProjectRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectRequirement
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    project_requirements = ProjectRequirementSerializer(many=True, read_only=True)
    client = ClientSerializer(read_only=True)
    client_id = serializers.IntegerField(write_only=True)
    assigned_to = UserSerializer(read_only=True)
    assigned_to_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class PaymentSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)
    project_id = serializers.IntegerField(write_only=True)
    client = ClientSerializer(read_only=True)
    client_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class InvoiceSerializer(serializers.ModelSerializer):
    payment = PaymentSerializer(read_only=True)
    
    class Meta:
        model = Invoice
        fields = '__all__'


class ProjectDetailSerializer(ProjectSerializer):
    payments = PaymentSerializer(many=True, read_only=True)
    total_payments = serializers.SerializerMethodField()
    remaining_budget = serializers.SerializerMethodField()
    
    def get_total_payments(self, obj):
        return sum(payment.amount_paid for payment in obj.payments.all())
    
    def get_remaining_budget(self, obj):
        if obj.budget:
            total_paid = sum(payment.amount_paid for payment in obj.payments.all())
            return obj.budget - total_paid
        return None


class ClientDetailSerializer(ClientSerializer):
    projects = ProjectSerializer(many=True, read_only=True)
    total_projects = serializers.SerializerMethodField()
    active_projects = serializers.SerializerMethodField()
    
    def get_total_projects(self, obj):
        return obj.projects.count()
    
    def get_active_projects(self, obj):
        return obj.projects.filter(status__in=['planning', 'in_progress']).count()
