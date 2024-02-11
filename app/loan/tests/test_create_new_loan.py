import json
from django.test import TestCase
from django.urls import reverse
from requests import patch
from rest_framework import status
from rest_framework.test import APIClient
from loan.serializers import LoanViewSerializer
from core.models import Customer, Loan 
from datetime import datetime

class LoanCreateViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('create-loan')  

    def test_loan_create_success(self):
       
        customer = Customer.objects.create(
            first_name="Md Armaan",
            last_name="Ansari",
            age=22,
            monthly_salary=1500000,
            phone_number=8726183214,
            approved_limit=1000000
        )

        data = {
            'customer_id': customer.id,
            'loan_amount': 4000,
            'interest_rate': 4,
            'tenure': 12
        }

        response = self.client.post(self.url, data, format='json')
        response_content = json.loads(response.content)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertTrue(Loan.objects.filter(customer=customer).exists())

        expected_data = {
            "loan_id": Loan.objects.get(customer=customer).id,
            "customer_id": customer.id,
            "loan_approved": True,
            "message": 'Loan approved',
            "monthly_installment": 347
        }
        self.assertEqual(response_content, expected_data)

    def test_loan_create_exceeds_approved_limit(self):
        customer = Customer.objects.create(
            first_name="Md Armaan",
            last_name="Ansari",
            age=22,
            monthly_salary=1500000,
            phone_number=8726183214,
            approved_limit=10000
        )

        data = {
            'customer_id': customer.id,
            'loan_amount': 15000,
            'interest_rate': 4,
            'tenure': 12
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        expected_error_message = {"error": "Loan amount exceeds the approved limit."}
        response_content = json.loads(response.content)
        self.assertEqual(response_content, expected_error_message)


class CustomerEligibleViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        self.url = reverse('customer-eligibility')

    def test_customer_eligible_success(self):
        
        customer = Customer.objects.create(
            first_name="Md Armaan",
            last_name="Ansari",
            age=22,
            monthly_salary=1500000,
            phone_number=8726183214,
            approved_limit=1000000
        )

       

        loan = Loan.objects.create(
            customer_id=customer.id,
            loan_amount=5000,
            tenure=12,
            interest_rate=5,
            date_of_approval=datetime.now(),
            monthly_payment=2000,
            emi_paid_on_time=0,
            end_date=datetime.now()
        )
      
        
        data = {
            'customer_id': customer.id,
            'loan_amount': 4000,
            'interest_rate': 4,
            'tenure': 12
        }

        
        response = self.client.post(self.url, data, format='json')
        response_content = json.loads(response.content)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        
        expected_data = {
            "customer_id": customer.id,
            "tenure": 12,
            "interest_rate": '4.00',
            "approval": True,
            "corrected_interest_rate": '4.00',
            "monthly_installment": 347
        }
        response_content = json.loads(response.content)
        self.assertEqual(response_content, expected_data)

    def test_customer_eligible_exceeds_approved_limit(self):
        
        customer = Customer.objects.create(
            first_name="Md Armaan",
            last_name="Ansari",
            age=22,
            monthly_salary=150000,
            phone_number=8726183213,
            approved_limit=10000
        )
        
        loan = Loan.objects.create(
            customer_id=customer.id,
            loan_amount=15000,
            tenure=12,
            interest_rate=5,
            date_of_approval=datetime.now(),
            monthly_payment=2000,
            emi_paid_on_time=0,
            end_date=datetime.now()
        )
        
        
        data = {
            'customer_id': customer.id,
            'loan_amount': 15000,
            'interest_rate': 4,
            'tenure': 12
        }

       
        response = self.client.post(self.url, data, format='json')

       
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

       
        expected_error_message = {
            "error": "Loan amount exceeds the approved limit."}
        response_content = json.loads(response.content)
        self.assertEqual(response_content, expected_error_message)


class LoanDetailViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('loan-detail', kwargs={'loan_id': 1}) 
        
    def test_loan_detail_success(self):

        customer = Customer.objects.create(
            first_name="Md Armaan",
            last_name="Ansari",
            age=22,
            monthly_salary=150000,
            phone_number=8726183213,
            approved_limit=10000
        )

        loan = Loan.objects.create(
            customer_id=customer.id,
            loan_amount=15000,
            tenure=12,
            interest_rate=5,
            date_of_approval=datetime.now(),
            monthly_payment=2000,
            emi_paid_on_time=0,
            end_date=datetime.now()
        )
        url  = reverse('loan-detail', kwargs={'loan_id': loan.id})
        response = self.client.get(url,format='json')
        response_content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = LoanViewSerializer(loan).data
        self.assertEqual(response_content, expected_data)

    def test_loan_detail_not_found(self):
        
            
            url  = reverse('loan-detail', kwargs={'loan_id': 1})
            response = self.client.get(url,format='json')
            response_content = json.loads(response.content)
            
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

            expected_error_message = {"error": "Loan does not exist."}
            self.assertEqual(response_content, expected_error_message)
