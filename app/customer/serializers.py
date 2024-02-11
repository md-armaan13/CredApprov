"""
Serializers for the customer API

"""
from rest_framework import serializers

from core.models import Customer
from django.core.validators import MinValueValidator


class CustomerSerializer(serializers.ModelSerializer):
    """
    Customer serializer
    """
    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'age',
                  'phone_number', 'monthly_salary', 'approved_limit']
        read_only_fields = ['approved_limit']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Change 'id' to 'customer_id'
        representation['customer_id'] = representation.pop('id')
        # Combine 'first_name' and 'last_name' into 'name'
        representation['name'] = f"{representation.pop('first_name')} {representation.pop('last_name')}"
        return representation

    def create(self, validated_data):
        monthly_salary = validated_data.get('monthly_salary')
        approved_limit = round((36 * monthly_salary) / 100000) * 100000
        validated_data['approved_limit'] = approved_limit
        return Customer.objects.create(**validated_data)


class CustomerEligibilitySerializer(serializers.ModelSerializer):
    """
    Customer eligibility serializer
    """
    loan_amount = serializers.IntegerField(validators=[
        MinValueValidator(0, message='Loan Amount should be positive')])
    interest_rate = serializers.DecimalField(max_digits=12, decimal_places=2, validators=[
        MinValueValidator(0, message='Interst Rate should be positive')])
    tenure = serializers.IntegerField(validators=[
        MinValueValidator(0, message='Interst Rate should be positive')])
    approval = serializers.BooleanField(read_only=True)
    corrected_interest_rate = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True)
    monthly_installment = serializers.IntegerField(read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'age',
                  'phone_number', 'monthly_salary', 'approved_limit']
        read_only_fields = ['monthly_installment',
                            'corrected_interest_rate', 'approval']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Change 'id' to 'customer_id'
        representation['customer_id'] = representation.pop('id')
        # Combine 'first_name' and 'last_name' into 'name'
        representation['name'] = f"{representation.pop('first_name')} {representation.pop('last_name')}"
        return representation
