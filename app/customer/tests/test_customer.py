from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Customer 
from customer.serializers import CustomerSerializer  


class CustomerViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
       
        self.url = reverse('customer-register')

    def test_create_customer_success(self):
       
        data = {
            "first_name": "Md Armaan",
            "last_name": "Ansari",
            "age": 22,
            "monthly_salary": 150000,
            "phone_number": 8726183219
        }

        
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

       
        self.assertTrue(Customer.objects.filter(
            phone_number='8726183219').exists())

        
        created_customer = Customer.objects.get(phone_number='8726183219')
        expected_data = CustomerSerializer(created_customer).data
    
        self.assertEqual(
            expected_data["phone_number"], str(data["phone_number"]))

    def test_create_customer_existing_phone_number(self):
        
        existing_customer = Customer.objects.create(first_name="Md Armaan",
                                                    last_name="Ansari",
                                                    age=22,
                                                    monthly_salary=150000,
                                                    phone_number=8726183219,
                                                    approved_limit=1000000
                                                    )

        
        data = {
            "first_name": "Md Armaan",
            "last_name": "Ansari",
            "age": 22,
            "monthly_salary": 150000,
            "phone_number": 8726183219
        }

        
        response = self.client.post(self.url, data, format='json')

        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
