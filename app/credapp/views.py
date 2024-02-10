from django.http import JsonResponse
from core.tasks import import_excel_data
import pandas as pd
from django.conf import settings
import os
from core.models import Loan , Customer
from django.db import transaction

customer_file_path = os.path.join(settings.MEDIA_ROOT, 'customer_data.xlsx')
loan_file_path = os.path.join(settings.MEDIA_ROOT, 'loan_data.xlsx')


def health_check(request):
    """Health Check endpoint"""
    if Loan.objects.exists():
        print('Data already exists in the database. Skipping import.')
        return JsonResponse({'status': 'ok'})

    # If no data exists, proceed with importing

    customer_data = pd.read_excel(customer_file_path)
    loan_data = pd.read_excel(loan_file_path)

    with transaction.atomic():
        for index, row in customer_data.iterrows():
            Customer.objects.create(
                first_name=row['First Name'],
                last_name=row['Last Name'],
                age=row['Age'],
                phone_number=row['Phone Number'],
                monthly_salary=row['Monthly Salary'],
                approved_limit=row['Approved Limit'],
            )
        for index, row in loan_data.iterrows():

            Loan.objects.create(
                customer_id=row['Customer ID'],
                loan_amount=row['Loan Amount'],
                tenure=row['Tenure'],
                interest_rate=row['Interest Rate'],
                monthly_payment=row['Monthly payment'],
                emi_paid_on_time=row['EMIs paid on Time'],
                date_of_approval=row['Date of Approval'],
                end_date=row['End Date'],
            )
    print('Data imported successfully.')
    return JsonResponse({'status': 'ok'})
