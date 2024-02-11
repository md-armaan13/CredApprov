"""
Serializers for the Loan API

"""
from rest_framework import serializers

from core.models import Loan, Customer
from django.core.validators import MinValueValidator


class CustomerEligibilitySerializer(serializers.ModelSerializer):
    """
    Customer eligibility serializer
    """

    approval = serializers.BooleanField(read_only=True)
    corrected_interest_rate = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True)
    monthly_installment = serializers.IntegerField(read_only=True)
    customer_id = serializers.IntegerField()

    class Meta:
        model = Loan
        fields = ['id', 'customer_id', 'tenure', 'loan_amount', 'interest_rate',
                  'approval', 'corrected_interest_rate', 'monthly_installment']
        read_only_fields = ['monthly_installment',
                            'corrected_interest_rate', 'approval']


class CustomerEligibilityResponseSerializer(serializers.ModelSerializer):
    """
    Customer eligibility Resposnse serializer
    """

    approval = serializers.BooleanField()
    corrected_interest_rate = serializers.DecimalField(
        max_digits=12, decimal_places=2)
    monthly_installment = serializers.IntegerField()
    customer_id = serializers.IntegerField()

    class Meta:
        model = Loan
        fields = ['customer_id', 'tenure', 'interest_rate',
                  'approval', 'corrected_interest_rate', 'monthly_installment']


class LoanCreateSerializer(serializers.ModelSerializer):
    """
    Loan create serializer
    """

    class Meta:
        model = Loan
        fields = ['customer_id', 'tenure', 'loan_amount', 'interest_rate']
        read_only_fields = ['id']


class CustomerSerializer(serializers.ModelSerializer):
    """
    Customer serializer
    """

    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'age',
                  'phone_number']


class LoanViewSerializer(serializers.ModelSerializer):
    """
    Loan view serializer
    """
    customer = CustomerSerializer(read_only=True)

    class Meta:
        model = Loan
        fields = ['id', 'customer', 'tenure', 'loan_amount', 'interest_rate',
                  'monthly_payment']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Change 'id' to 'customer_id'
        representation['loan_id'] = representation.pop('id')
        return representation


class CustomerLoanSerializer(serializers.ModelSerializer):
    """
    Loan serializer
    """
    repayments_left = serializers.IntegerField(read_only=True ,default=0)

    class Meta:
        model = Loan
        fields = ['id', 'loan_amount', 'interest_rate',
                  'monthly_payment','repayments_left']
        read_only_fields = ['repayments_left']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Change 'id' to 'customer_id'
        representation['loan_id'] = representation.pop('id')
        return representation
    
