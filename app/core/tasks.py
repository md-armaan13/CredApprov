"""Celery tasks for the core app."""

import pandas as pd
import os

from django.db import transaction
from django.utils import timezone
from django.conf import settings

from core.models import Loan , Customer
from celery import shared_task





customer_file_path = os.path.join(settings.MEDIA_ROOT, 'customer_data.xlsx')
loan_file_path = os.path.join(settings.MEDIA_ROOT, 'loan_data.xlsx')

@shared_task
def import_excel_data():
    """Populating the database with the data from the excel files."""
    if Customer.objects.exists() or Loan.objects.exists():
        print('Data already exists in the database. Skipping import.')
        return 

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
            end_date_naive = row['End Date']
            date_approve_naive = row['Date of Approval']
            date_approve_aware = timezone.make_aware(date_approve_naive)
            end_date_aware = timezone.make_aware(end_date_naive)
            Loan.objects.create(
                customer_id=row['Customer ID'],
                loan_amount=row['Loan Amount'],
                tenure=row['Tenure'],
                interest_rate=row['Interest Rate'],
                monthly_payment=row['Monthly payment'],
                emi_paid_on_time=row['EMIs paid on Time'],
                date_of_approval=date_approve_aware,
                end_date=end_date_aware,
            )
    print('Data imported successfully.')
